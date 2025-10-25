"""
Kaggle Dataset Download Helper
Automatically downloads FER-2013 dataset if Kaggle API is configured
"""

import os
import zipfile
import subprocess
import sys


def check_kaggle_installed():
    """Check if Kaggle API is installed"""
    try:
        import kaggle
        return True
    except ImportError:
        return False


def download_dataset():
    """Download FER-2013 dataset using Kaggle API"""
    
    print("="*60)
    print("📥 FER-2013 Dataset Downloader")
    print("="*60)
    
    # Check if Kaggle is installed
    if not check_kaggle_installed():
        print("\n⚠️  Kaggle API not installed!")
        print("\n📦 To install Kaggle API:")
        print("   pip install kaggle")
        print("\n🔑 Then configure your credentials:")
        print("   1. Go to: https://www.kaggle.com/account")
        print("   2. Click 'Create New API Token'")
        print("   3. Save kaggle.json to C:/Users/YourName/.kaggle/")
        print("\n🔄 Or download manually from:")
        print("   https://www.kaggle.com/datasets/msambare/fer2013")
        return False
    
    print("\n✓ Kaggle API found!")
    
    # Check if dataset already exists
    if os.path.exists('fer2013.zip'):
        print("\n⚠️  Dataset already downloaded!")
        response = input("Re-download? (y/n): ")
        if response.lower() != 'y':
            return True
    
    try:
        print("\n📥 Downloading FER-2013 dataset...")
        print("   This may take a few minutes...")
        
        # Download using Kaggle CLI
        subprocess.run(['kaggle', 'datasets', 'download', '-d', 'msambare/fer2013'], check=True)
        
        print("\n✓ Download complete!")
        
        # Extract dataset
        print("\n📦 Extracting dataset...")
        extract_dataset()
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\n💡 Try downloading manually from:")
        print("   https://www.kaggle.com/datasets/msambare/fer2013")
        return False


def extract_dataset():
    """Extract the downloaded dataset"""
    
    if not os.path.exists('fer2013.zip'):
        print("❌ Dataset zip file not found!")
        return
    
    print("📂 Extracting files...")
    
    with zipfile.ZipFile('fer2013.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    
    print("✓ Extraction complete!")
    print("\n📋 Next steps:")
    print("   1. Organize images into data/train/, data/val/, data/test/")
    print("   2. Run: python train.py")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 FER-2013 Dataset Setup")
    print("="*60)
    
    # Check if kaggle is installed
    if not check_kaggle_installed():
        print("\n💡 Manual Download Instructions:")
        print("="*60)
        print("1. Go to: https://www.kaggle.com/datasets/msambare/fer2013")
        print("2. Click 'Download' button")
        print("3. Sign in with Kaggle account")
        print("4. Extract the zip file")
        print("5. Organize images into data/train/, data/val/, data/test/")
        print("="*60)
        
        install = input("\n📦 Install Kaggle API? (y/n): ")
        if install.lower() == 'y':
            print("\n📥 Installing Kaggle API...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'kaggle'])
            print("\n✓ Kaggle API installed!")
            print("\n🔑 Configure credentials:")
            print("   1. Go to: https://www.kaggle.com/account")
            print("   2. Click 'Create New API Token'")
            print("   3. Save kaggle.json to:")
            print("      C:/Users/YourName/.kaggle/kaggle.json")
            print("\nThen run this script again!")
        else:
            print("\n👍 You can download manually and organize the files.")
    else:
        # Try to download
        download_dataset()

