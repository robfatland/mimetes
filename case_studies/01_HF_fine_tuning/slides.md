---
marp: true
theme: default
paginate: true
header: "![w:135](../03_research_mechanics/cloudbank_logo.png)&nbsp; Fine-Tuning a Pre-Trained Model with PyTorch"
---

<!-- _header: "" -->
<!-- _paginate: false -->
<!-- _footer: "" -->

![w:500](../03_research_mechanics/cloudbank_logo.png)

# Fine-Tuning a Pre-Trained Model with PyTorch

**CloudBank Cloud Clinic July 2026**

Using: PyTorch, torchvision, transfer learning

---

## What Is Fine-Tuning?

Someone else trained a model on millions of images (ImageNet).

We take that model, **keep its learned features**, and retrain
only the final layer for our specific task.

- No need for massive data
- No need for massive compute
- Works surprisingly well

---

## The Idea: Transfer Learning

```
Pre-trained model (ResNet-18):
  [edges] → [textures] → [shapes] → [objects] → [1000 ImageNet classes]
                                                         ↓
                                            Replace with: [our 10 classes]
```

The early layers already know how to "see." We just teach it what to look *for*.

---

## Step 1: Load a Pre-Trained Model

```python
import torchvision.models as models

model = models.resnet18(pretrained=True)
```

This downloads ~44MB of weights trained on 1.2 million images.

---

## Step 2: Replace the Classification Head

```python
import torch.nn as nn

# ResNet-18's final layer: 512 features → 1000 classes
# Replace with: 512 features → 10 classes (CIFAR-10)
model.fc = nn.Linear(512, 10)
```

---

## Step 3: Freeze the Base Layers

```python
for param in model.parameters():
    param.requires_grad = False

# Only the new head trains
for param in model.fc.parameters():
    param.requires_grad = True
```

---

## Step 4: Train

```python
for epoch in range(5):
    for images, labels in train_loader:
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
```

The same 5-line loop that drives all of deep learning.

---

## Results

- Training: ~5 minutes on a laptop CPU
- Accuracy: ~85–92% on CIFAR-10 (from scratch would take hours for comparable)
- Key insight: pre-trained features transfer across tasks

---

## What We Learned

| Concept | Where |
|---------|-------|
| Pre-trained weights | Step 1 |
| Transfer learning | Steps 2–3 |
| The training loop | Step 4 |
| Freezing layers | Step 3 |
| Loss and backpropagation | Step 4 |

Next: Case Study 02 — build and train from scratch (no shortcuts).

---

## Questions? Compliments?

**Repository:** github.com/robfatland/mimetes
**Contact:** help@cloudbank.org
