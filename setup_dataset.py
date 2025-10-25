"""
Helper script to download and organize FER-2013 dataset
Run this script to automatically set up the dataset structure
"""

import os
import zipfile
import requests
from pathlib import Path


def download_file(url, destination):
    """Download a file from URL with progress bar"""
    print(f"📥 Downloading: {destination}")
    
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    downloaded = 0
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r  Progress: {percent:.1f}%", end='', flush=True)
    
    print("\n✓ Download complete!")


def extract_zip(zip_path, extract_to):
    """Extract zip file"""
    print(f"📦 Extracting: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("✓ Extraction complete!")


def organize_dataset(dataset_dir):
    """Organize dataset into train/val/test structure"""
    print("\n📁 Organizing dataset structure...")
    
    # Create directories
    for split in ['train', 'val', 'test']:
        for emotion in ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']:
            os.makedirs(f'data/{split}/{emotion}', exist_ok=True)
    
    print("✓ Directory structure created!")
    print("\n" + "="*60)
    print("📋 Manual Steps Required:")
    print("="*60)
    print("1. Download FER-2013 dataset from:")
    print("   https://www.kaggle.com/datasets/msambare/fer2013")
    print("\n2. Extract the dataset")
    print("\n3. Organize images into:")
    print("   data/train/[emotion]/")
    print("   data/val/[emotion]/")
    print("   data/test/[emotion]/")
    print("\n4. Run: python train.py")
    print("="*60)


if __name__ == '__main__':
    print("="*60)
    print("🎭 FER-2013 Dataset Setup Helper")
    print("="*60)
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Organize dataset
    organize_dataset('data')
    
    print("\n💡 Tip: You can also manually download the dataset")
    print("   and organize it following the structure shown above.")

