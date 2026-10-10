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

## Data source

`datasets.MNIST(..., download=True)` from `torchvision` downloads the four original MNIST files from PyTorch's mirror on AWS S3, `https://ossci-datasets.s3.amazonaws.com/mnist/`. Its listed fallback, Yann LeCun's original site `http://yann.lecun.com/exdb/mnist/`, no longer serves the files (it returns 404), so in practice the data comes from S3. Each file is checked against an MD5 checksum and then extracted into `data/MNIST/raw/`:

| File | Contents |
|---|---|
| `train-images-idx3-ubyte.gz` | 60,000 training images (28×28) |
| `train-labels-idx1-ubyte.gz` | 60,000 training labels (0–9) |
| `t10k-images-idx3-ubyte.gz` | 10,000 test images |
| `t10k-labels-idx1-ubyte.gz` | 10,000 test labels |

MNIST was created by Yann LeCun, Corinna Cortes, and Christopher J.C. Burges from handwriting samples collected by NIST (the US National Institute of Standards and Technology).

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
