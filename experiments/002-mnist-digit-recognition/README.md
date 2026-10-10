# 002 – MNIST Digit Recognition

A small neural network that learns to recognize handwritten digits (0–9) from 28×28 pixel images, using the classic [MNIST](https://en.wikipedia.org/wiki/MNIST_database) dataset.

## Goal

Move from experiment 001 (one neuron, one number in, one number out) to a real classification problem:

- Load a real dataset with `torchvision` and feed it in **mini-batches** with a `DataLoader`
- Use a **hidden layer** with a non-linear activation (`ReLU`)
- Predict one of **10 classes** with `CrossEntropyLoss`
- Measure **accuracy** on test images the model never saw during training

## The model

```
image (28x28) → flatten (784) → Linear → 128 → ReLU → Linear → 10 scores
```

Each of the 10 outputs is a score for one digit, and the highest score is the prediction.

## Run

```bash
uv run python train.py
```

The first run downloads MNIST (~64 MB) into `data/`, which is git-ignored.

## Results

Training takes about 25 s on a CPU and reaches **~96% test accuracy** after 3 epochs:

```
epoch 1  last batch loss 0.0949  test accuracy 94.38%
epoch 2  last batch loss 0.0911  test accuracy 96.17%
epoch 3  last batch loss 0.0465  test accuracy 96.43%
```

At the end, the script prints a few test images as ASCII art along with the model's prediction.

## Things to try

- Train for more epochs, or change the hidden layer size (32, 512, …)
- Add a second hidden layer
- Swap `Adam` for `SGD` and compare how fast each one learns
- Print the images the model gets **wrong**: they're often hard for humans to read too
- Replace the network with a small CNN (`nn.Conv2d`) to get to ~99%
