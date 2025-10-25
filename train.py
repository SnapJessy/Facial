"""
Training script for Facial Expression Recognition Model
Train on FER-2013 dataset or custom dataset
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
import os
import sys
from models.fer_model import get_model, EMOTION_LABELS

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def train_model(data_dir='data', epochs=50, batch_size=64, learning_rate=0.001):
    """
    Train the facial expression recognition model
    
    Args:
        data_dir: Directory containing train/val/test folders
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate for optimizer
    """
    
    # Check if CUDA is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"🚀 Using device: {device}")
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((48, 48)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    val_transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize((48, 48)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    
    # Check if directories exist
    train_path = os.path.join(data_dir, 'train')
    val_path = os.path.join(data_dir, 'val')
    
    if not os.path.exists(train_path):
        print(f"\n❌ Error: Training directory not found: {train_path}")
        print("\n📥 Please download the FER-2013 dataset:")
        print("   1. Go to: https://www.kaggle.com/datasets/msambare/fer2013")
        print("   2. Download the dataset")
        print("   3. Extract and organize images into the folder structure shown above")
        print("\n💡 The directory structure has been created for you.")
        print("   You just need to add the images to each emotion folder.")
        return
    
    # Load datasets
    train_dataset = datasets.ImageFolder(
        train_path,
        transform=train_transform
    )
    
    val_dataset = datasets.ImageFolder(
        val_path,
        transform=val_transform
    )
    
    print(f"✓ Training samples: {len(train_dataset)}")
    print(f"✓ Validation samples: {len(val_dataset)}")
    print(f"✓ Number of classes: {len(train_dataset.classes)}")
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=2
    )
    
    # Initialize model
    model = get_model(num_classes=len(train_dataset.classes))
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=15, gamma=0.5)
    
    # Training loop
    print("\n" + "="*60)
    print("🎯 Starting Training")
    print("="*60)
    
    best_val_acc = 0
    
    for epoch in range(epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            train_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
        
        train_acc = 100 * train_correct / train_total
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                
                outputs = model(images)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_acc = 100 * val_correct / val_total
        avg_val_loss = val_loss / len(val_loader)
        
        # Print statistics
        print(f"Epoch [{epoch+1}/{epochs}]")
        print(f"  Train Loss: {avg_train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), 'models/fer_model.pth')
            print(f"  ✓ Saved best model (Val Acc: {val_acc:.2f}%)")
        
        scheduler.step()
        print()
    
    print("="*60)
    print(f"✅ Training Complete! Best Validation Accuracy: {best_val_acc:.2f}%")
    print("="*60)


if __name__ == '__main__':
    print("=" * 60)
    print("🎭 Facial Expression Recognition - Training")
    print("=" * 60)
    print("\n📋 Instructions:")
    print("1. Download FER-2013 dataset from Kaggle")
    print("2. Organize data in following structure:")
    print("   data/")
    print("   ├── train/")
    print("   │   ├── Angry/")
    print("   │   ├── Disgust/")
    print("   │   ├── Fear/")
    print("   │   ├── Happy/")
    print("   │   ├── Sad/")
    print("   │   ├── Surprise/")
    print("   │   └── Neutral/")
    print("   ├── val/")
    print("   │   ├── (same structure as train)")
    print("   └── test/")
    print("       └── (same structure as train)")
    print("\n" + "=" * 60)
    
    # Check if data directory exists
    if not os.path.exists('data'):
        print("\n⚠️  Error: 'data' directory not found!")
        print("Please create the data directory structure as shown above.")
        exit(1)
    
    # Start training
    train_model(
        data_dir='data',
        epochs=10,  # Reduced for faster training
        batch_size=32,  # Smaller batch size
        learning_rate=0.001
    )

