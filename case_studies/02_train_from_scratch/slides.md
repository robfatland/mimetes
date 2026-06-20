---
marp: true
theme: default
paginate: true
header: "![w:135](../03_research_mechanics/cloudbank_logo.png)&nbsp; Train a Neural Network from Scratch"
---

<!-- _header: "" -->
<!-- _paginate: false -->
<!-- _footer: "" -->

![w:500](../03_research_mechanics/cloudbank_logo.png)

# Train a Neural Network from Scratch

**CloudBank Cloud Clinic July 2026**

Using: PyTorch, MNIST, and nothing pre-trained

---

## What Is a Neural Network?

A function with adjustable parameters (weights).

```
Input (image pixels) → [layer] → [layer] → [layer] → Output (digit 0–9)
```

Each layer: multiply by a matrix, add a bias, apply a nonlinearity.

Training = adjusting those matrices until the output is correct.

---

## The Dataset: MNIST

![bg right:40% w:350](https://upload.wikimedia.org/wikipedia/commons/f/f7/MnistExamplesModified.png)

- 70,000 handwritten digits
- 28×28 pixels, grayscale
- 10 classes (0–9)
- The "hello world" of ML

---

## Step 1: Define the Network

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 10),
        )

    def forward(self, x):
        return self.layers(x)
```

---

## Step 2: The Training Loop

```python
model = SimpleNet()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for images, labels in train_loader:
        pred = model(images)
        loss = criterion(pred, labels)
        loss.backward()       # compute gradients
        optimizer.step()      # update weights
        optimizer.zero_grad() # reset
```

---

## What's Happening Inside

1. **Forward:** pixels → matrix multiply → ReLU → matrix multiply → prediction
2. **Loss:** how wrong is the prediction? (cross-entropy)
3. **Backward:** PyTorch traces the math backward, computing ∂loss/∂weight for every weight
4. **Step:** nudge each weight in the direction that reduces loss

Repeat ~60,000 times (once per training image × 10 epochs).

---

## Watching It Learn

- Epoch 1: ~85% accuracy (random → rough pattern matching)
- Epoch 3: ~95% accuracy (learned digit structure)
- Epoch 10: ~97–98% accuracy (diminishing returns)

The loss curve tells the story: steep descent, then plateau.

---

## What Can Go Wrong

- **Overfitting** — memorizes training data, fails on new data
- **Learning rate too high** — loss explodes, never converges
- **Learning rate too low** — loss decreases imperceptibly slowly
- **Vanishing gradients** — deep networks where early layers stop learning

---

## Key Takeaways

| Concept | What It Means |
|---------|--------------|
| Tensor | Multi-dimensional array (like a matrix but more general) |
| Layer | Matrix multiply + nonlinearity |
| Forward pass | Data flows through layers |
| Backward pass | Gradients flow back through layers |
| Optimizer | Uses gradients to update weights |
| Epoch | One full pass through all training data |

---

## Questions? Compliments?

**Repository:** github.com/robfatland/mimetes
**Contact:** help@cloudbank.org
