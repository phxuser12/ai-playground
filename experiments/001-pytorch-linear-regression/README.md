# 001 – PyTorch Linear Regression

The simplest possible neural network: a single neuron that learns the function **y = 2x + 1** from examples.

## Goal

Understand the basic PyTorch training loop:

1. **Forward pass:** the model makes a prediction
2. **Loss:** measure how wrong the prediction is (mean squared error)
3. **Backward pass:** compute gradients with `loss.backward()`
4. **Optimizer step:** adjust the weight and bias to reduce the loss

## The model

`nn.Linear(1, 1)` is one neuron with a single weight `w` and bias `b`:

```
y = w * x + b
```

It starts with random `w` and `b`. After training, they should be close to `w = 2` and `b = 1`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python train.py
```

## Expected output

The loss falls toward 0, and the learned equation ends up close to `y = 2 * x + 1`. The script also predicts values outside the training range (e.g. `x = 100`) to show the model learned the rule itself, not just the examples it saw.

## Things to try

- Change the learning rate (`lr`): too high and training diverges, too low and it's slow
- Use fewer epochs and see how far from the target the result is
- Add noise to `y` (`y += torch.randn_like(y)`) to mimic real-world data
- Try a non-linear target (e.g. `y = x**2`) and see why one linear neuron isn't enough
