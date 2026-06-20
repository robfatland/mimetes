# Learning PyTorch

A conceptual deep-dive, built incrementally. This document grows alongside the
case studies.

---

## 1. What PyTorch Is

PyTorch is a Python library that provides two things:

1. **Tensors** — like NumPy arrays, but they can run on GPUs and they track
   the math you do with them
2. **Automatic differentiation** — given any computation, PyTorch can compute
   how to adjust inputs to change the output (gradients)

Everything else — layers, networks, optimizers, data loaders — is built on top
of these two primitives.

---

## 2. Tensors

A tensor is a multi-dimensional array of numbers. That's all.

| Shape | What it represents |
|-------|-------------------|
| `()` | A scalar (one number) |
| `(5,)` | A vector (5 numbers) |
| `(3, 4)` | A matrix (3 rows × 4 columns) |
| `(64, 1, 28, 28)` | A batch of 64 grayscale 28×28 images |
| `(16, 3, 224, 224)` | A batch of 16 RGB 224×224 images |

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0])       # shape (3,)
m = torch.randn(3, 4)                     # shape (3, 4), random values
batch = torch.randn(64, 1, 28, 28)        # a batch of MNIST images
```

### Why not just use NumPy?

- Tensors can live on GPU (`x.to("cuda")`) for massive parallelism
- Tensors track their computational history for automatic differentiation
- The API is nearly identical to NumPy — easy transition

### Key operations

```python
# Element-wise
y = x * 2        # multiply every element by 2
z = x + y        # add element-wise

# Matrix multiply
a = torch.randn(3, 4)
b = torch.randn(4, 5)
c = a @ b        # shape (3, 5)

# Reshaping
flat = batch.view(64, 784)  # flatten 28×28 images to 784-length vectors
```

---

## 3. What a Neural Network Actually Is

A neural network is a **function** — it takes input numbers and produces output
numbers. The function is defined by **parameters** (weights and biases) that
start random and are adjusted during training.

The simplest possible network (one layer):

```
output = input @ weights + bias
```

That's a linear transformation (matrix multiply + add). By itself, this can only
learn linear relationships. To learn complex patterns, we stack multiple layers
with **nonlinearities** (activation functions) between them:

```
layer1 = relu(input @ W1 + b1)
layer2 = relu(layer1 @ W2 + b2)
output = layer2 @ W3 + b3
```

### Why ReLU?

ReLU (Rectified Linear Unit) is the simplest nonlinearity: `max(0, x)`. It
zeroes out negative values. Without it, stacking linear layers just produces
another linear layer — no matter how many you stack. The nonlinearity is what
gives the network its power to approximate complex functions.

### The Universal Approximation Theorem

A neural network with at least one hidden layer and a nonlinear activation can
approximate **any continuous function** to arbitrary precision, given enough
neurons. This is the theoretical justification for why neural networks work at all.

---

## 4. The Training Loop

Training a neural network means finding parameter values that make the outputs
correct. This is an optimization problem:

1. **Forward pass** — feed data through the network, get a prediction
2. **Loss** — measure how wrong the prediction is
3. **Backward pass** — compute gradients (how should each weight change to
   reduce the loss?)
4. **Update** — nudge weights in the direction that reduces loss
5. **Repeat** — thousands or millions of times

```python
for epoch in range(num_epochs):
    for batch_inputs, batch_labels in dataloader:
        # Forward
        predictions = model(batch_inputs)
        loss = loss_function(predictions, batch_labels)

        # Backward
        loss.backward()  # computes gradients for every parameter

        # Update
        optimizer.step()       # applies gradients to parameters
        optimizer.zero_grad()  # resets gradients for next iteration
```

This loop is **the same for every neural network ever trained** — from a 3-layer
digit classifier to GPT-4. The only things that change are the model architecture,
the data, and the loss function.

---

## 5. Backpropagation and Automatic Differentiation

The magic of `loss.backward()`: PyTorch records every operation you perform on
tensors (multiply, add, relu, etc.) in a computational graph. When you call
`.backward()`, it traverses that graph in reverse, applying the chain rule to
compute ∂loss/∂parameter for every parameter.

You never write derivative code. You write the forward pass; PyTorch handles
the backward pass automatically.

### Intuition

Imagine a river flowing downhill. The loss is your altitude. Gradients tell you
which direction is downhill from where you are. The optimizer takes a step in
that direction. Repeat until you reach a valley (minimum loss).

The catch: the landscape has many valleys (local minima), ridges, saddle points,
and plateaus. Optimizers like Adam are designed to navigate this terrain robustly.

---

## 6. Layers in PyTorch

PyTorch provides building blocks in `torch.nn`:

| Layer | What it does |
|-------|-------------|
| `nn.Linear(in, out)` | Matrix multiply + bias (fully connected) |
| `nn.Conv2d(in_ch, out_ch, kernel)` | 2D convolution (spatial patterns in images) |
| `nn.ReLU()` | Zero out negatives |
| `nn.Sigmoid()` | Squash to [0, 1] (probabilities) |
| `nn.Softmax(dim)` | Squash to probabilities that sum to 1 |
| `nn.Dropout(p)` | Randomly zero out neurons (prevents overfitting) |
| `nn.BatchNorm2d(ch)` | Normalize activations (stabilizes training) |
| `nn.LSTM(in, hidden)` | Recurrent layer for sequences |

You compose them into a network by subclassing `nn.Module`:

```python
class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(784, 128)
        self.layer2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = x.view(-1, 784)     # flatten
        x = self.relu(self.layer1(x))
        x = self.layer2(x)
        return x
```

---

## 7. Loss Functions

The loss function measures how wrong the prediction is. Common choices:

| Loss | Used for | Formula (intuition) |
|------|---------|-------------------|
| `nn.CrossEntropyLoss` | Classification (pick one of N classes) | How surprised are we by the wrong answer? |
| `nn.MSELoss` | Regression (predict a number) | Average squared error |
| `nn.BCELoss` | Binary classification (yes/no) | Log probability of correct answer |

The loss is a single number. Smaller = better. The entire training process is
just minimizing this number.

---

## 8. Optimizers

An optimizer uses gradients to update weights. The simplest:

**SGD (Stochastic Gradient Descent):**
```
weight = weight - learning_rate * gradient
```

**Adam** (the default choice for most work):
- Maintains a running average of gradients and squared gradients
- Adapts the learning rate per-parameter
- Handles noisy gradients and sparse features well

```python
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

The **learning rate** is the most important hyperparameter. Too high: training
diverges. Too low: training takes forever. Typical starting point: 0.001.

---

## 9. Data Loading

PyTorch's `DataLoader` handles batching, shuffling, and parallel data loading:

```python
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_data = datasets.MNIST(root="./data", train=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
```

Each iteration of the DataLoader yields one batch: a tensor of images and a
tensor of labels, ready for the forward pass.

---

## 10. GPU Acceleration

Moving computation to GPU is one line:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# In the training loop:
inputs = inputs.to(device)
labels = labels.to(device)
```

For MNIST on a laptop CPU: training takes ~2 minutes.
On a GPU: ~10 seconds. The difference grows enormously for larger models.

---

## 11. The Logistics Map as a Learning Metaphor

The logistics map x_{n+1} = r · x_n · (1 - x_n) is the simplest system that
transitions from predictable to chaotic behavior as a parameter changes.

| r value | Behavior | Neural network analog |
|---------|----------|----------------------|
| 1–3 | Stable fixed point | Convergent training (good LR) |
| 3–3.45 | Period-2 oscillation | Loss oscillating (LR slightly high) |
| 3.45–3.57 | Period doubling cascade | Increasing instability |
| > 3.57 | Chaos | Divergent training (LR too high) |
| Periodic windows | Brief order within chaos | Sudden improvements after plateaus |

The spiderweb diagram (cobweb plot) shows convergence to a fixed point — directly
analogous to how gradient descent spirals toward a loss minimum. When the system
bifurcates, the optimizer oscillates between two values instead of settling.

This isn't just an analogy. Neural network training IS a discrete dynamical system:
the weight update rule `w_{n+1} = w_n - η·∇L(w_n)` is an iterated map, just like
the logistics map. The learning rate η plays the role of r.

---

## What's Next

- **Case Study 01:** Apply this knowledge — fine-tune a pre-trained model
- **Case Study 02:** Build everything from scratch — implement the training loop by hand
- **Case Study 04:** Two networks competing (GAN) — dynamical systems with two coupled maps

---

*This document is a living reference. It will be updated as understanding deepens
through hands-on work in the case studies.*
