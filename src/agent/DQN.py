import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, input_shape, num_actions):
        """
        input_shape: tuple with (chanels, height, width) -> Optimized for (1, 8, 10)
        num_actions: 160 (80 clicks + 80 flags)
        """
        super().__init__()
        
        # Step 1: What will the AI check
        # kernel_size=3 3x3 blocks
        # padding=1 invisible border so no error
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        
        # We check the size result after processing the matrix
        # 64 channels * 8 height * 10 width = 5120
        linear_input_size = 64 * input_shape[1] * input_shape[2]
        
        # Step 2: The IA layers
        self.fc1 = nn.Linear(linear_input_size, 512)
        self.fc2 = nn.Linear(512, num_actions)

    def forward(self, x):
        # We transform the data in float as indicated by PyTorch
        x = x.float()
        
        # We use the ReLU activation function (Thanks "Sistemas inteligentes" ;)")
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        
        # From 3D to 1D for lineal layers
        x = torch.flatten(x, start_dim=1)
        
        # Last activation function usage
        x = F.relu(self.fc1(x))
        
        # We return the Q-Values (Thanks "Sistemas inteligentes x2") that gives a punctuation to each decision.
        return self.fc2(x)