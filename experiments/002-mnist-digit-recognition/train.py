"""Teach a small neural network to recognize handwritten digits (MNIST)."""

import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"using {device}: {torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU'}")

torch.manual_seed(42)

# MNIST: 28x28 grayscale images of digits 0-9 (60k for training, 10k for testing).
# ToTensor() turns each image into a (1, 28, 28) tensor with pixel values in [0, 1].
transform = transforms.ToTensor()
train_data = datasets.MNIST("data", train=True, download=True, transform=transform)
test_data = datasets.MNIST("data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=1000)

# The network: flatten the image into 784 numbers -> 128 hidden neurons -> 10 outputs.
# Each output is a score for one digit; the highest score is the prediction.
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28 * 28, 128),
    nn.ReLU(),
    nn.Linear(128, 10),
).to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

print(next(model.parameters()).device)

def evaluate() -> float:
    correct = 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            predictions = model(images).argmax(dim=1)
            correct += (predictions == labels).sum().item()
    return correct / len(test_data)


for epoch in range(1, 4):
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        scores = model(images)            # forward pass
        loss = loss_fn(scores, labels)    # how wrong are we?

        optimizer.zero_grad()             # reset old gradients
        loss.backward()                   # compute gradients
        optimizer.step()                  # nudge weights to reduce loss

    print(f"epoch {epoch}  last batch loss {loss.item():.4f}  test accuracy {evaluate():.2%}")


def show(image: torch.Tensor) -> None:
    """Print a 28x28 image as ASCII art."""
    for row in image.squeeze(0):
        print("".join("#" if p > 0.5 else "+" if p > 0.2 else " " for p in row))


# Look at a few test images and what the model thinks they are
for i in range(3):
    image, label = test_data[i]
    with torch.no_grad():
        prediction = model(image.unsqueeze(0).to(device)).argmax().item()
    print()
    show(image)
    print(f"actual: {label}  predicted: {prediction}")
