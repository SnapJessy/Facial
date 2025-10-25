# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Download Dataset

### Option A: Using Kaggle (Recommended)

1. Create a Kaggle account at https://www.kaggle.com
2. Go to https://www.kaggle.com/datasets/msambare/fer2013
3. Click "Download" button
4. Extract the zip file

### Option B: Using Kaggle API

```bash
# Install Kaggle API
pip install kaggle

# Set up credentials (download from Kaggle Account settings)
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle datasets download -d msambare/fer2013

# Extract
unzip fer2013.zip
```

## Step 3: Organize Dataset

Create the following structure:

```
data/
├── train/
│   ├── Angry/
│   ├── Disgust/
│   ├── Fear/
│   ├── Happy/
│   ├── Sad/
│   ├── Surprise/
│   └── Neutral/
├── val/
│   ├── (same structure as train)
└── test/
    └── (same structure as train)
```

**Tips:**
- Use 80% of data for training, 10% for validation, 10% for testing
- Or use the predefined splits if available in the dataset

## Step 4: Train the Model

```bash
python train.py
```

**Expected Output:**
- Training will take 30-60 minutes on GPU
- 2-4 hours on CPU
- Model will be saved to `models/fer_model.pth`

## Step 5: Run the Web App

```bash
python app.py
```

Open browser: **http://localhost:5000**

## 🎮 Test the App

1. **Webcam Mode**: Click "Start Webcam" and make faces
2. **Upload Mode**: Click "Upload Image" and select a photo

## 📊 Expected Results

After training, you should see:
- Training accuracy: ~70-80%
- Validation accuracy: ~60-70%
- Test accuracy: ~55-65%

## 🐛 Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### CUDA Not Available
- Install CUDA-enabled PyTorch from https://pytorch.org
- Or use CPU (will be slower)

### Webcam Not Working
- Use Chrome or Firefox
- Check browser permissions
- Try restarting the browser

## 💡 Next Steps

- Experiment with different model architectures
- Try different hyperparameters
- Add more emotions to the dataset
- Deploy to cloud (Heroku, AWS, etc.)

Happy coding! 🎉

