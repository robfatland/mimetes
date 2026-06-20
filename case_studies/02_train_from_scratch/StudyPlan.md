# Case Study 02 — Train a Neural Network from Scratch

## Objective

Build a small neural network from raw PyTorch components and train it on MNIST
(handwritten digits). Understand tensors, layers, backpropagation, and the full
training loop without any pre-trained shortcuts.

## What We'll Use

| Component | Choice |
|-----------|--------|
| Model | Custom 3–5 layer network (torch.nn) |
| Dataset | MNIST (70k handwritten digit images, 28×28 px) |
| Framework | PyTorch (no HuggingFace, no pre-trained anything) |
| Visualization | matplotlib (loss curves, weight evolution, live training) |

## Key Concepts

1. **Tensors** — multi-dimensional arrays; the fundamental data structure
2. **Layers** — linear (matrix multiply), activation (ReLU), etc.
3. **Forward pass** — data flows through layers to produce a prediction
4. **Loss function** — measures how wrong the prediction is (cross-entropy)
5. **Backpropagation** — loss.backward() computes gradients automatically
6. **Optimizer** — SGD or Adam uses gradients to update weights
7. **Epochs and batches** — how training data is cycled through the model
8. **Overfitting** — when the model memorizes training data instead of generalizing

## Steps

1. Load and explore MNIST with torchvision
2. Define a network class (subclass torch.nn.Module)
3. Implement forward() method
4. Choose loss function and optimizer
5. Write the training loop
6. Track and plot loss per epoch
7. Evaluate accuracy on test set
8. Visualize misclassified examples
9. Experiment: add layers, change learning rate, observe effects
10. (Optional) Live training visualization for PEARC demo

## PEARC Demo Potential

A live loss curve and accuracy tracker updating in real time as training
progresses. Side panel showing sample predictions improving over epochs.

## Status

🔲 Not started
