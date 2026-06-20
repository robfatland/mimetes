# Case Study 01 — Fine-Tuning a Pre-Trained Model

## Objective

Take a pre-trained image classifier from HuggingFace/torchvision and fine-tune
it on a small custom dataset. Learn transfer learning, the PyTorch training loop,
and how pre-trained weights accelerate learning.

## What We'll Use

| Component | Choice |
|-----------|--------|
| Base model | ResNet-18 (torchvision, pre-trained on ImageNet) |
| Dataset | CIFAR-10 (60k tiny images, 10 classes) or a custom glacier/non-glacier set |
| Framework | PyTorch + torchvision |
| Visualization | matplotlib (loss curves, predictions) |

## Key Concepts

1. **Pre-trained weights** — a model already trained on millions of images
   has learned generic visual features (edges, textures, shapes)
2. **Transfer learning** — reuse those features, retrain only the final
   classification layer for your specific task
3. **Freezing layers** — lock early layers so they don't change; only
   train the layers relevant to your new classes
4. **The training loop** — forward pass → loss → backward → optimizer step
5. **Evaluation** — accuracy on held-out test set, confusion matrix

## Steps

1. Load a pre-trained ResNet-18
2. Replace the final fully-connected layer to match new class count
3. Freeze all layers except the new head
4. Set up DataLoaders for train/test splits
5. Train for a few epochs, tracking loss and accuracy
6. Evaluate on the test set
7. Visualize: loss curve, sample predictions, confusion matrix
8. (Optional) Unfreeze more layers and fine-tune deeper

## Presentation Context

CloudBank Cloud Clinic — demonstrating PyTorch fundamentals via transfer learning.
This is the gentlest on-ramp: most of the hard work (feature learning) was done
by someone else; we just adapt it.

## Status

🔲 Not started
