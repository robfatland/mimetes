"""
fine_tune.py — Fine-tune a pre-trained ResNet-18 on CIFAR-10.

This is Case Study 01: The gentlest on-ramp to PyTorch.
We take a model that already knows how to "see" (trained on ImageNet)
and teach it to classify 10 new categories with minimal training.

Usage:
    python fine_tune.py

What happens:
    1. Downloads CIFAR-10 (~170 MB on first run, cached thereafter)
    2. Loads ResNet-18 with pre-trained ImageNet weights
    3. Replaces the final classification layer (1000 → 10 classes)
    4. Freezes all layers except the new head
    5. Trains for 5 epochs (~2-5 min on GPU, ~15 min on CPU)
    6. Reports accuracy on test set
    7. Saves loss curve and sample predictions to images/

Output:
    images/loss_curve.png
    images/sample_predictions.png
    Prints accuracy to console
"""

import matplotlib
matplotlib.use('Agg')

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Configuration ---
BATCH_SIZE = 64
NUM_EPOCHS = 5
LEARNING_RATE = 0.001
NUM_CLASSES = 10

CIFAR10_CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']

# Detect GPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")


def get_data_loaders():
    """Set up CIFAR-10 with transforms appropriate for ResNet."""
    transform = transforms.Compose([
        transforms.Resize(64),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    train_data = datasets.CIFAR10(root="./data", train=True,
                                   download=True, transform=transform)
    test_data = datasets.CIFAR10(root="./data", train=False,
                                  download=True, transform=transform)

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE,
                              shuffle=True, num_workers=2)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE,
                             shuffle=False, num_workers=2)

    print(f"Training samples: {len(train_data):,}")
    print(f"Test samples:     {len(test_data):,}")

    return train_loader, test_loader


def extract_features(loader, model):
    """Run all images through the frozen backbone ONCE, cache the 512-d features."""
    model.eval()
    features_list = []
    labels_list = []

    print("  Extracting features (one-time pass through frozen backbone)...")
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(DEVICE)
            # Run through everything except the final FC layer
            x = model.conv1(images)
            x = model.bn1(x)
            x = model.relu(x)
            x = model.maxpool(x)
            x = model.layer1(x)
            x = model.layer2(x)
            x = model.layer3(x)
            x = model.layer4(x)
            x = model.avgpool(x)
            x = torch.flatten(x, 1)  # shape: (batch, 512)
            features_list.append(x.cpu())
            labels_list.append(labels)

    all_features = torch.cat(features_list, dim=0)
    all_labels = torch.cat(labels_list, dim=0)
    print(f"  Features shape: {all_features.shape}")
    return all_features, all_labels


def build_model():
    """Load pre-trained ResNet-18 and replace the classification head."""
    # Load with ImageNet weights
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    # Freeze all existing layers
    for param in model.parameters():
        param.requires_grad = False

    # Replace the final fully-connected layer
    # Original: 512 features → 1000 ImageNet classes
    # New:      512 features → 10 CIFAR-10 classes
    model.fc = nn.Linear(512, NUM_CLASSES)
    # The new layer's parameters have requires_grad=True by default

    model = model.to(DEVICE)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nTotal parameters:     {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,} "
          f"({100*trainable_params/total_params:.1f}%)")

    return model


def train_one_epoch(model, loader, criterion, optimizer):
    """Run one training epoch. Returns average loss."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward pass
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Track metrics
        running_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    avg_loss = running_loss / total
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


def evaluate(model, loader):
    """Evaluate model on test set. Returns accuracy."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return 100.0 * correct / total


def plot_loss_curve(losses, accuracies):
    """Plot training loss and accuracy over epochs."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(range(1, len(losses)+1), losses, 'b-o')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training Loss')
    ax1.grid(True, alpha=0.3)

    ax2.plot(range(1, len(accuracies)+1), accuracies, 'g-o')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Training Accuracy')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "loss_curve.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    plt.close()


def plot_sample_predictions(model, test_loader):
    """Show a grid of test images with predictions."""
    model.eval()

    # Get one batch
    images, labels = next(iter(test_loader))
    images_device = images.to(DEVICE)

    with torch.no_grad():
        outputs = model(images_device)
        _, predicted = outputs.max(1)

    # Denormalize for display
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])

    fig, axes = plt.subplots(4, 8, figsize=(16, 8))
    for i, ax in enumerate(axes.flat):
        if i >= 32:
            break
        img = images[i].numpy().transpose(1, 2, 0)  # CHW → HWC
        img = std * img + mean  # denormalize
        img = np.clip(img, 0, 1)

        pred = predicted[i].item()
        true = labels[i].item()
        color = 'green' if pred == true else 'red'

        ax.imshow(img)
        ax.set_title(f"{CIFAR10_CLASSES[pred]}", color=color, fontsize=8)
        ax.axis('off')

    plt.suptitle("Sample Predictions (green=correct, red=wrong)", fontsize=12)
    plt.tight_layout()
    out_path = OUTPUT_DIR / "sample_predictions.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Saved: {out_path}")
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Case Study 01: Fine-Tuning ResNet-18 on CIFAR-10")
    print("=" * 60)

    # Step 1: Data
    print("\n--- Loading data ---")
    train_loader, test_loader = get_data_loaders()

    # Step 2: Model (full ResNet for feature extraction)
    print("\n--- Building model ---")
    model = build_model()

    # Step 3: Extract features ONCE through the frozen backbone
    print("\n--- Caching features (this is the slow part, happens once) ---")
    train_features, train_labels = extract_features(train_loader, model)
    test_features, test_labels = extract_features(test_loader, model)

    # Step 4: Train ONLY the head on cached features (fast!)
    print(f"\n--- Training head for {NUM_EPOCHS} epochs ---")
    head = model.fc.to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(head.parameters(), lr=LEARNING_RATE)

    # Create simple data loaders from cached features
    from torch.utils.data import TensorDataset
    train_feat_loader = DataLoader(
        TensorDataset(train_features, train_labels),
        batch_size=256, shuffle=True)
    test_feat_loader = DataLoader(
        TensorDataset(test_features, test_labels),
        batch_size=256, shuffle=False)

    losses = []
    accuracies = []

    for epoch in range(1, NUM_EPOCHS + 1):
        head.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for feats, labels in train_feat_loader:
            feats, labels = feats.to(DEVICE), labels.to(DEVICE)
            outputs = head(feats)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            running_loss += loss.item() * feats.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        avg_loss = running_loss / total
        acc = 100.0 * correct / total
        losses.append(avg_loss)
        accuracies.append(acc)
        print(f"  Epoch {epoch}/{NUM_EPOCHS}: loss={avg_loss:.4f}, train_acc={acc:.1f}%")

    # Step 5: Evaluate
    print("\n--- Evaluating on test set ---")
    head.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for feats, labels in test_feat_loader:
            feats, labels = feats.to(DEVICE), labels.to(DEVICE)
            outputs = head(feats)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    test_acc = 100.0 * correct / total
    print(f"  Test accuracy: {test_acc:.1f}%")

    # Step 6: Visualize
    print("\n--- Generating plots ---")
    plot_loss_curve(losses, accuracies)
    plot_sample_predictions(model, test_loader)

    print("\n" + "=" * 60)
    print("Done!")
    print(f"  Model: ResNet-18 (frozen) + new head ({NUM_CLASSES} classes)")
    print(f"  Trainable params: {sum(p.numel() for p in head.parameters()):,}")
    print(f"  Final test accuracy: {test_acc:.1f}%")
    print("=" * 60)
