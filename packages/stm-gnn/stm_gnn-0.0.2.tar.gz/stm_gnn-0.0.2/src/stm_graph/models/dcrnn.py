import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import DCRNN
from .base_model import BaseGNN


class RecurrentGCN_DCRNN(BaseGNN):
    """
    Diffusion Convolutional Recurrent Neural Network for Traffic Forecasting.
    Supports both 3D and 4D input formats.
    """

    def __init__(self, in_channels, out_channels, hidden_dim=64, K=3, dropout=0.2):
        """
        Initialize DCRNN model.

        Args:
            in_channels: Number of input features
            out_channels: Number of output features
            hidden_dim: Size of hidden layer
            K: Filter size for diffusion convolution
            dropout: Dropout rate
        """
        super(RecurrentGCN_DCRNN, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.hidden_dim = hidden_dim
        self.K = K
        self.dcrnn = DCRNN(in_channels=in_channels, out_channels=hidden_dim, K=K)
        self.linear = nn.Linear(hidden_dim, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, edge_index, edge_weight=None, h=None):
        """
        Forward pass through the DCRNN model.

        Args:
            x: Input features [batch_size, num_nodes, in_channels] or
               [batch_size, num_nodes, time_steps, in_channels]
            edge_index: Edge indices
            edge_weight: Optional edge weights
            h: Hidden state from previous step

        Returns:
            (h, out): Updated hidden state and output
        """
        # Handle 4D input (with temporal dimension)
        if x.dim() == 4:  # [batch_size, num_nodes, time_steps, in_channels]
            batch_size, num_nodes, time_steps, _ = x.shape

            if h is None:
                h = torch.zeros(batch_size, num_nodes, self.hidden_dim, device=x.device)

            new_hidden_states = []
            outputs = []

            for b in range(batch_size):
                batch_h = h[b] if h is not None else None

                for t in range(time_steps):
                    x_t = x[b, :, t, :]  # [num_nodes, in_channels]

                    batch_h = self.dcrnn(x_t, edge_index, edge_weight, batch_h)

                h_out = F.relu(batch_h)
                h_out = self.dropout(h_out)
                y = self.linear(h_out)

                new_hidden_states.append(batch_h)
                outputs.append(y)

            h_new = torch.stack(
                new_hidden_states
            )  # [batch_size, num_nodes, hidden_dim]
            y_out = torch.stack(outputs)  # [batch_size, num_nodes, out_channels]

            return h_new, y_out

        # Handle 3D input (batch dimension but no temporal dimension)
        elif x.dim() == 3:  # [batch_size, num_nodes, in_channels]
            batch_size, num_nodes, _ = x.shape
            hidden_states = []
            outputs = []

            for i in range(batch_size):
                batch_x = x[i]  # [num_nodes, in_channels]

                batch_h = None
                if h is not None:
                    if h.dim() == 3:  # [batch_size, num_nodes, hidden_dim]
                        batch_h = h[i]
                    else:
                        batch_h = h

                new_h = self.dcrnn(batch_x, edge_index, edge_weight, batch_h)
                h_out = F.relu(new_h)
                h_out = self.dropout(h_out)
                y = self.linear(h_out)

                hidden_states.append(new_h)
                outputs.append(y)

            h_stacked = torch.stack(
                hidden_states
            )  # [batch_size, num_nodes, hidden_dim]
            y_stacked = torch.stack(outputs)  # [batch_size, num_nodes, out_channels]

            return h_stacked, y_stacked

        # Handle 2D input (single sample, no batch dimension)
        else:  # [num_nodes, in_channels]
            h_new = self.dcrnn(x, edge_index, edge_weight, h)
            h_out = F.relu(h_new)
            h_out = self.dropout(h_out)
            y = self.linear(h_out)

            return h_new.unsqueeze(0), y.unsqueeze(0)  # [1, num_nodes, out_channels]
