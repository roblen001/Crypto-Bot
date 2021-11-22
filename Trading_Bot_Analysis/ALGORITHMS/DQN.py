'''DQN algorithm 3 convolution layers and 2 connected layers with ReLU seperation

    Source: https://github.com/PacktPublishing/Deep-Reinforcement-Learning-Hands-On-Second-Edition/blob/master/Chapter10/lib/data.py
    Modified: Roberto Lentini
'''
import torch
import torch.nn as nn
import numpy as np


class DQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super(DQN, self).__init__()

        self.conv = nn.Sequential(
            nn.Conv1d(input_shape[0], 128, 5),
            nn.ReLU(),
            nn.Conv1d(128, 128, 5),
            nn.ReLU(),
            # nn.Conv1d(64, 64, kernel_size=3, stride=1),
            # nn.ReLU()
        )

        conv_out_size = self._get_conv_out(input_shape)
        self.fc = nn.Sequential(
            nn.Linear(conv_out_size, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions)
        )

    def _get_conv_out(self, shape):
        '''Allows the code to remain generic and not require us to define
            the exact output from the convolution layer.
        '''
        o = self.conv(torch.zeros(1, *shape))
        return int(np.prod(o.size()))

    def forward(self, x):
        '''Allows to reshape 3D tensors into batch of 1D vectors.
        '''
        conv_out = self.conv(x).view(x.size()[0], -1)
        return self.fc(conv_out)
