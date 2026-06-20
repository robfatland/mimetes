# Transfer Learning: Fine-Tuning a CNN

Case Study 01 reference document. Covers what we're doing, why, and what the
moving parts are.

---

## The Big Picture

We take a model that already knows how to "see" (ResNet-18, trained on 1.2 million
ImageNet photos) and teach it to classify a new set of categories (CIFAR-10: 10
classes of small images). This is **transfer learning**: reusing learned visual
features rather than training from scratch.

---

## ResNet-18: What's Inside

ResNet-18 is a convolutional neural network (CNN) with 18 weighted layers, organized
into stages that progressively extract higher-level visual features:

| Stage | Layers | What it detects | Output shape |
|-------|--------|----------------|-------------|
| Conv1 | 1 conv | Edges, simple gradients | 64 × 112 × 112 |
| Block 1 | 4 conv | Textures, corners | 64 × 56 × 56 |
| Block 2 | 4 conv | Parts (eyes, wheels) | 128 × 28 × 28 |
| Block 3 | 4 conv | Object parts | 256 × 14 × 14 |
| Block 4 | 4 conv | Whole object concepts | 512 × 7 × 7 |
| Global Avg Pool | — | Summarize each channel | 512 |
| FC (classification) | 1 linear | Map to class scores | 1000 (or 10) |

Total: ~11.2 million parameters. We train only the last 5,130.

### The "18" and the "Res"

- **18** = the count of layers with learnable weights (convolutions + FC)
- **Res** = residual. The network has skip-connections that add the input of a
  block directly to its output. This lets gradients flow unimpeded through deep
  networks, solving the vanishing gradient problem.

### What we replaced

The original final layer: 512 inputs → 1000 ImageNet classes.
Our replacement: 512 inputs → 10 CIFAR-10 classes.
Parameters added: 512×10 weights + 10 biases = 5,130.

---

## CNNs: Convolutional Neural Networks

Unlike the fully-connected (MLP) networks in LearnPyTorch.md, CNNs have **spatial
structure**. They process images as 2D grids, not flattened vectors.

### Convolution layers

A conv layer slides a small filter (say 3×3 pixels) across the image, computing
a dot product at each position. The filter detects a specific local pattern (edge,
corner, texture). Many filters per layer → many feature maps.

Key property: **translation invariance**. The same filter detects a cat ear whether
it's in the top-left or bottom-right of the image. This is why CNNs dominate vision.

### Pooling layers

Pooling shrinks spatial dimensions by summarizing local regions:

```
Max Pooling (2×2):

Input (4×4):          Output (2×2):
[1  3  2  4]
[5  6  1  2]    →    [6  4]
[7  2  3  1]         [7  3]
[4  1  5  3]
```

Each 2×2 block → keep the maximum. Resolution halves, strongest signal preserved.

**Why pool?**
- Reduces computation (fewer values in the next layer)
- Adds translation invariance (small shifts don't change the max)
- Forces abstraction (later layers see coarser, semantic information)

**Global Average Pooling** (at the end of ResNet): takes the entire 7×7 spatial map
for each feature channel and averages it into one number. 512×7×7 → 512 values.
This is what feeds into the final classification layer.

### ReLU in a CNN

Same as in an MLP: `max(0, x)` applied element-wise to every value. No parameters,
nothing to learn. Just decides which activations pass through (positive) and which
get zeroed out. One wire in, one wire out, per value.

---

## What "Frozen" Means

```python
for param in model.parameters():
    param.requires_grad = False  # don't compute gradients → don't update

model.fc = nn.Linear(512, 10)   # new layer: requires_grad=True by default
```

Frozen parameters:
- Still participate in the forward pass (their learned features are used)
- Do NOT get updated during training (no gradients computed for them)
- This makes training fast: only 5,130 params to update, not 11 million

The intuition: early layers already know generic visual features (edges, textures,
shapes). Those transfer well to any image task. Only the final mapping — "which
class does this collection of features correspond to?" — needs to be learned fresh.

---

## CIFAR-10: The Dataset

- 60,000 color images, 32×32 pixels
- 10 classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck
- 50,000 training / 10,000 test
- Standard benchmark — everyone uses it, results are comparable

We resize to 224×224 (what ResNet expects) and normalize to ImageNet statistics
(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) because ResNet was trained
with those normalization values.

---

## The Training Loop (in this case study)

```python
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

for epoch in range(5):
    for images, labels in train_loader:
        outputs = model(images)         # forward through ALL layers
        loss = criterion(outputs, labels)
        loss.backward()                 # gradients only for unfrozen params
        optimizer.step()                # update only the FC head
        optimizer.zero_grad()
```

Note: the forward pass goes through the entire network (frozen + unfrozen). But
`loss.backward()` only computes gradients for parameters with `requires_grad=True`,
and the optimizer only updates those.

---

## Expected Results

- **Accuracy after 5 epochs:** 85–92% on CIFAR-10 test set
- **Training time:** ~2-5 min on GPU, ~15 min on CPU
- **What this demonstrates:** you get strong results by training only 0.05% of the
  model's parameters. The pre-trained features do the heavy lifting.

---

## Script

`fine_tune.py` in this directory. Run with:

```bash
conda activate mimetes
python fine_tune.py
```

Produces:
- `images/loss_curve.png` — loss and accuracy over 5 epochs
- `images/sample_predictions.png` — grid of test images with predicted labels
