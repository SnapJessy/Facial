"""
Create a minimal dataset for testing training
Downloads sample images from the internet for each emotion
"""

import os
import sys
import requests
from PIL import Image, ImageDraw
import io

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def download_sample_images():
    """Download sample images for each emotion"""
    
    # Sample image URLs (free stock photos)
    sample_images = {
        'Happy': [
            'https://images.unsplash.com/photo-1517841905240-472988babdf9?w=200',
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200'
        ],
        'Sad': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ],
        'Angry': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ],
        'Surprise': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ],
        'Fear': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ],
        'Disgust': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ],
        'Neutral': [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200',
            'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=200'
        ]
    }
    
    print("📥 Downloading sample images...")
    
    for emotion, urls in sample_images.items():
        print(f"  Downloading {emotion} images...")
        
        for i, url in enumerate(urls):
            try:
                # Download image
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Convert to PIL Image
                    img = Image.open(io.BytesIO(response.content))
                    
                    # Convert to grayscale and resize to 48x48
                    img = img.convert('L').resize((48, 48))
                    
                    # Save to appropriate folders
                    for split in ['train', 'val']:
                        folder_path = f'data/{split}/{emotion}'
                        os.makedirs(folder_path, exist_ok=True)
                        
                        filename = f'{emotion.lower()}_{i+1}.jpg'
                        img.save(os.path.join(folder_path, filename))
                    
                    print(f"    ✓ Saved {emotion} image {i+1}")
                else:
                    print(f"    ⚠ Failed to download {emotion} image {i+1}")
                    
            except Exception as e:
                print(f"    ⚠ Error downloading {emotion} image {i+1}: {e}")
    
    print("\n✅ Sample dataset created!")
    print("📊 Dataset structure:")
    print("   - 2 images per emotion")
    print("   - 7 emotions")
    print("   - Total: 14 images")
    print("   - Split: train/val")


def create_synthetic_dataset():
    """Create synthetic dataset using colored rectangles"""
    
    print("🎨 Creating synthetic dataset...")
    
    # Colors for each emotion
    colors = {
        'Happy': (255, 255, 0),    # Yellow
        'Sad': (0, 0, 255),        # Blue
        'Angry': (255, 0, 0),      # Red
        'Surprise': (255, 165, 0), # Orange
        'Fear': (128, 0, 128),     # Purple
        'Disgust': (0, 128, 0),    # Green
        'Neutral': (128, 128, 128) # Gray
    }
    
    for emotion, color in colors.items():
        print(f"  Creating {emotion} images...")
        
        for i in range(5):  # 5 images per emotion
            # Create a simple colored image
            img = Image.new('RGB', (48, 48), color)
            
            # Add some variation
            if i % 2 == 0:
                # Add a circle
                from PIL import ImageDraw
                draw = ImageDraw.Draw(img)
                draw.ellipse([10, 10, 38, 38], fill=(255, 255, 255))
            
            # Save to train and val folders
            for split in ['train', 'val']:
                folder_path = f'data/{split}/{emotion}'
                os.makedirs(folder_path, exist_ok=True)
                
                filename = f'{emotion.lower()}_{i+1}.jpg'
                img.save(os.path.join(folder_path, filename))
        
        print(f"    ✓ Created 5 {emotion} images")
    
    print("\n✅ Synthetic dataset created!")
    print("📊 Dataset structure:")
    print("   - 5 images per emotion")
    print("   - 7 emotions")
    print("   - Total: 35 images")
    print("   - Split: train/val")


if __name__ == '__main__':
    print("=" * 60)
    print("🎭 Create Sample Dataset")
    print("=" * 60)
    
    print("\nChoose dataset type:")
    print("1. Synthetic dataset (colored rectangles)")
    print("2. Download sample images (requires internet)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        create_synthetic_dataset()
    elif choice == '2':
        try:
            download_sample_images()
        except ImportError:
            print("⚠️  requests not installed. Installing...")
            os.system("pip install requests")
            download_sample_images()
    elif choice == '3':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")
    
    print("\n" + "=" * 60)
    print("📋 Next steps:")
    print("   1. Run: python train.py")
    print("   2. Wait for training to complete")
    print("   3. Run: python app.py")
    print("=" * 60)

