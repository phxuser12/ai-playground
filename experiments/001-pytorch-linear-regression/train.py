"""Teach a tiny neural network to learn y = 2*x + 1."""

import torch
from torch import nn

torch.manual_seed(42)

# Training data: x values and their correct answers y = 2*x + 1
x = torch.linspace(-10, 10, 100).unsqueeze(1)  # shape (100, 1)
y = 2 * x + 1

# The "network": one neuron with one weight and one bias -> y = w*x + b
model = nn.Linear(in_features=1, out_features=1)

loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

for epoch in range(1, 501):
    prediction = model(x)            # forward pass
    loss = loss_fn(prediction, y)    # how wrong are we?

    optimizer.zero_grad()            # reset old gradients
    loss.backward()                  # compute gradients
    optimizer.step()                 # nudge w and b to reduce loss

    if epoch % 50 == 0:
        print(f"epoch {epoch:3d}  loss {loss.item():.6f}")

w = model.weight.item()
b = model.bias.item()
print(f"\nLearned: y = {w:.4f} * x + {b:.4f}   (target: y = 2 * x + 1)")

# Try it on values the model has never seen
test_x = torch.tensor([[15.0], [-20.0], [100.0]])
with torch.no_grad():
    for xi, yi in zip(test_x, model(test_x)):
        print(f"x = {xi.item():6.1f}  ->  predicted {yi.item():8.3f}  (expected {2 * xi.item() + 1:.1f})")
