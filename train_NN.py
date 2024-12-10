import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

########
# Import data
HA_freq = pd.read_csv('/Users/kuankuan/Documents/BMC/Fall2024/CompMethods/HA_freq.csv', delimiter=',', header=None)
HA_freq = HA_freq.to_numpy()
null_freq = pd.read_csv('/Users/kuankuan/Documents/BMC/Fall2024/CompMethods/null_freq.csv', delimiter=',', header=None)
null_freq = null_freq.to_numpy()

# Prepare data and tags in tensor format
fullData = np.vstack((HA_freq, null_freq))
tags = np.repeat([1, 0], [200, 200], axis = 0)
tags = tags.reshape([400, 1])

sampleSize = 400
train_size = int(sampleSize*0.8)

np.random.seed(42)
random_idx = np.random.permutation(sampleSize)
bls_train = fullData[random_idx[0:train_size]]
bls_test = fullData[random_idx[train_size:]]
bls_label_train = tags[random_idx[0:train_size]]
bls_label_test = tags[random_idx[train_size:]]

BLSDataTrain = torch.tensor(bls_train, dtype = torch.float32)
BLSDataTest = torch.tensor(bls_test, dtype = torch.float32)
BLSLabelsTrain = torch.tensor(bls_label_train, dtype = torch.float32)
BLSLabelsTest = torch.tensor(bls_label_test, dtype = torch.float32)

# Build model
BLS_model = nn.Sequential(
    nn.Linear(3000, 100),
    nn.ReLU(),
    nn.Linear(100, 20),
    nn.ReLU(),
    nn.Linear(20, 10),
    nn.ReLU(),
    nn.Linear(10, 1),
    nn.Sigmoid())

# Loss fn and optimizer
loss_fn = nn.MSELoss()  # mean squared error
optimizer = optim.Adam(BLS_model.parameters(), lr=0.001)

# Train model
nIts = 1000                 # number of iterations to run optimization
for it in range(nIts):      # for each iteration of optimization
    bls_pred = BLS_model(BLSDataTrain)          # predict model outputs based on current weights ('forward step')
    loss = loss_fn(bls_pred, BLSLabelsTrain)  # calculate the loss, based on model current predictions (y_pred) and desired outputs (y)
    optimizer.zero_grad()      # reset all gradient values to 0
    loss.backward()            # calculate new gradient values for each weight based on current loss ('backward step')
    optimizer.step()
