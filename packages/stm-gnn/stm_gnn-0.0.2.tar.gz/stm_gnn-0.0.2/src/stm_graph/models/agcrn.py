import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import AGCRN
from .base_model import BaseGNN


class RecurrentGCN_AGCRN(BaseGNN):
    """
    Adaptive Graph Convolutional Recurrent Network.
    Supports both 3D and 4D input formats.
    """

    def __init__(
        self,
        num_nodes,
        in_channels,
        hidden_dim=64,
        k=3,
        embedding_dimensions=8,
        out_channels=1,
    ):
        """
        Initialize AGCRN model.

        Args:
            num_nodes: Number of nodes in the graph
            node_features: Number of input features per node
            hidden_dim: Size of hidden layers
            k: Number of Chebyshev filter taps
            embedding_dimensions: Size of node embedding
            out_channels: Number of output features
        """
        super(RecurrentGCN_AGCRN, self).__init__()
        self.num_nodes = num_nodes
        self.in_channels = in_channels
        self.hidden_dim = hidden_dim
        self.out_channels = out_channels
        self.K = k
        self.embedding_dimensions = embedding_dimensions

        self.agcrn = AGCRN(
            number_of_nodes=self.num_nodes,
            in_channels=self.in_channels,
            out_channels=self.hidden_dim,
            K=self.K,
            embedding_dimensions=self.embedding_dimensions,
        )

        self.linear = nn.Linear(hidden_dim, out_channels)

        self.node_embeddings = nn.Parameter(
            torch.randn(num_nodes, embedding_dimensions)
        )

    def forward(self, x, edge_index, edge_weight=None, h=None):
        """
        Forward pass through the AGCRN model.

        Args:
            x: Input features [batch_size, num_nodes, in_channels] or
               [batch_size, num_nodes, time_steps, in_channels]
            edge_index: Edge indices (not used in AGCRN but kept for API consistency)
            edge_weight: Optional edge weights (not used in AGCRN but kept for API consistency)
            h: Hidden state from previous step

        Returns:
            (h, out): Updated hidden state and output
        """
        # Handle 4D input (with temporal dimension)
        if x.dim() == 4:
            batch_size, num_nodes, time_steps, _ = x.shape

            if num_nodes != self.num_nodes:
                raise ValueError(f"Expected {self.num_nodes} nodes, got {num_nodes}")

            if h is None:
                h = torch.zeros(batch_size, num_nodes, self.hidden_dim, device=x.device)

            new_hidden_states = []
            outputs = []

            for b in range(batch_size):
                batch_h = None
                if h is not None:
                    batch_h = h[b : b + 1]  # [1, num_nodes, hidden_dim]

                for t in range(time_steps):
                    x_t = x[b : b + 1, :, t, :]  # [1, num_nodes, in_channels]

                    batch_h = self.agcrn(x_t, self.node_embeddings, batch_h)

                h_out = batch_h.squeeze(0)

                h_out = F.relu(h_out)
                y = self.linear(h_out)

                new_hidden_states.append(h_out)
                outputs.append(y)

            h_new = torch.stack(
                new_hidden_states
            )  # [batch_size, num_nodes, hidden_dim]
            y_out = torch.stack(outputs)  # [batch_size, num_nodes, out_channels]

            return h_new, y_out

        # Handle 3D input (batch dimension but no temporal dimension)
        elif x.dim() == 3:  # [batch_size, num_nodes, in_channels]
            batch_size, num_nodes, _ = x.shape

            if num_nodes != self.num_nodes:
                raise ValueError(f"Expected {self.num_nodes} nodes, got {num_nodes}")

            hidden_states = []
            outputs = []

            for i in range(batch_size):
                batch_x = x[i : i + 1]  # [1, num_nodes, in_channels]

                batch_h = None
                if h is not None:
                    if h.dim() == 3:  # [batch_size, num_nodes, hidden_dim]
                        batch_h = h[i : i + 1]  # [1, num_nodes, hidden_dim]
                    else:
                        batch_h = h.unsqueeze(0) if h.dim() == 2 else h

                new_h = self.agcrn(batch_x, self.node_embeddings, batch_h)

                h_out = new_h.squeeze(0)
                h_out = F.relu(h_out)
                y = self.linear(h_out)

                hidden_states.append(h_out)
                outputs.append(y)

            h_stacked = torch.stack(
                hidden_states
            )  # [batch_size, num_nodes, hidden_dim]
            y_stacked = torch.stack(outputs)  # [batch_size, num_nodes, out_channels]

            return h_stacked, y_stacked

        # Handle 2D input (single sample, no batch dimension)
        else:  # [num_nodes, in_channels]
            x = x.unsqueeze(0)  # [1, num_nodes, in_channels]

            if h is not None and h.dim() == 2:
                h = h.unsqueeze(0)  # [1, num_nodes, hidden_dim]

            h_new = self.agcrn(x, self.node_embeddings, h)

            h_out = h_new.squeeze(0)  # Remove batch dimension
            h_out = F.relu(h_out)
            y = self.linear(h_out)

            return h_out.unsqueeze(0), y.unsqueeze(0)  # [1, num_nodes, out_channels]
