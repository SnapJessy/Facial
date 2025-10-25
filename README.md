# 🎭 AI-Powered Facial Expression Recognition Web App

A Python-based web application that detects human facial expressions in images or live video streams and predicts emotions using deep learning.

## 🎯 Features

- **Real-time Emotion Detection**: Detect emotions from live webcam feed
- **Image Upload**: Upload images and get instant emotion predictions
- **7 Emotion Classes**: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
- **Modern UI**: Beautiful, responsive web interface
- **Detailed Analysis**: View probability scores for all emotions
- **Face Detection**: Automatic face detection using OpenCV

## 📋 Requirements

- Python 3.8 or higher
- Webcam (for real-time detection)
- Modern web browser

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd ImageRecog
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download Dataset

You need to download the FER-2013 dataset:

1. Go to [Kaggle FER-2013](https://www.kaggle.com/datasets/msambare/fer2013)
2. Download the dataset
3. Extract and organize as follows:

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
│   ├── Angry/
│   ├── Disgust/
│   ├── Fear/
│   ├── Happy/
│   ├── Sad/
│   ├── Surprise/
│   └── Neutral/
└── test/
    ├── Angry/
    ├── Disgust/
    ├── Fear/
    ├── Happy/
    ├── Sad/
    ├── Surprise/
    └── Neutral/
```

### 4. Train the Model

```bash
python train.py
```

This will train the CNN model and save it to `models/fer_model.pth`.

**Note**: Training can take 30-60 minutes depending on your hardware. For CPU-only systems, consider training overnight.

### 5. Run the Web Application

```bash
python app.py
```

Open your browser and navigate to: **http://localhost:5000**

## 📁 Project Structure

```
ImageRecog/
├── app.py                  # Flask web application
├── train.py               # Model training script
├── requirements.txt       # Python dependencies
├── models/
│   └── fer_model.py      # CNN model architecture
├── templates/
│   ├── index.html        # Original web interface
│   └── healthsphere.html # New Healthsphere interface
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend logic
└── data/
    ├── train/            # Training images
    ├── val/              # Validation images
    └── test/             # Test images
```

## 🎮 How to Use

### Healthsphere Interface (New!)

Access the beautiful new Healthsphere interface at: **http://localhost:5000/healthsphere**

Features:
- **Oval Scanner**: Live camera feed in a futuristic circular scanner
- **Real-time Analysis**: Automatic emotion detection every 2 seconds
- **Modern UI**: Gradient backgrounds, animations, and responsive design
- **Health Analytics**: Mood tracking and health insights

### Original Interface

Access the original interface at: **http://localhost:5000**

### Webcam Mode

1. Click **"Start Camera"** button (Healthsphere) or **"Start Webcam"** (Original)
2. Allow browser access to your webcam
3. Look at the camera and make different expressions
4. The app will automatically detect your emotion every 2 seconds

### Upload Mode

1. Click **"Upload Image"** button
2. Select an image file from your computer
3. The app will detect faces and predict emotions

### Results

- **Main Prediction**: Shows the most likely emotion with confidence percentage
- **All Emotions**: Displays probability bars for all 7 emotions

## 🧠 Model Architecture

The CNN model consists of:

- **3 Convolutional Blocks**: Each with Conv2D, BatchNorm, ReLU, MaxPool
- **3 Fully Connected Layers**: With dropout for regularization
- **Input Size**: 48×48 grayscale images
- **Output**: 7 emotion classes

## 🎓 Training Tips

### For Better Accuracy

1. **Data Augmentation**: The training script includes:
   - Random horizontal flips
   - Random rotations (±10 degrees)
   - Brightness and contrast adjustments

2. **Hyperparameters**: Adjust these in `train.py`:
   - `epochs`: Increase for longer training (default: 50)
   - `batch_size`: Adjust based on GPU memory (default: 64)
   - `learning_rate`: Reduce for fine-tuning (default: 0.001)

3. **GPU Training**: If you have CUDA GPU:
   ```bash
   # Install CUDA-enabled PyTorch
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Expected Results

- Training on FER-2013 dataset: ~60-70% validation accuracy
- Training time: 30-60 minutes on GPU, 2-4 hours on CPU

## 🔧 Troubleshooting

### "Model not loaded" Error

- Make sure you've trained the model first: `python train.py`
- Ensure `models/fer_model.pth` exists

### Webcam Not Working

- Check browser permissions for camera access
- Try Chrome or Firefox (most reliable)
- Ensure no other application is using the webcam

### No Face Detected

- Ensure your face is clearly visible
- Try different lighting conditions
- Make sure you're looking directly at the camera

### Low Accuracy

- Train for more epochs
- Use GPU if available
- Add more training data
- Fine-tune hyperparameters

## 📝 Customization

### Add More Emotions

1. Add emotion folders to data directories
2. Update `EMOTION_LABELS` in `models/fer_model.py`
3. Update `num_classes` in model initialization
4. Retrain the model

### Change UI Colors

Edit `static/css/style.css` and modify the gradient colors:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adjust Prediction Frequency

In `static/js/app.js`, change the interval:

```javascript
setTimeout(() => predictFromVideo(), 2000); // Change 2000 to desired milliseconds
```

## 🎉 Features in Detail

### Emotion Detection

- **Happy** 😊: Smiles, raised cheeks
- **Sad** 😢: Drooping corners of mouth, downturned eyes
- **Angry** 😠: Furrowed brows, tight mouth
- **Surprise** 😲: Wide eyes, raised eyebrows
- **Fear** 😨: Wide eyes, tense mouth
- **Disgust** 🤢: Wrinkled nose, downturned mouth
- **Neutral** 😐: No strong emotion

### Technical Details

- **Face Detection**: Haar Cascade (OpenCV)
- **Model**: Custom CNN (PyTorch)
- **Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript

## 📚 Learn More

- [FER-2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Documentation](https://docs.opencv.org/)

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- FER-2013 dataset creators
- OpenCV community
- PyTorch team
- Flask developers

---

**Made with ❤️ using PyTorch, Flask, and OpenCV**

If you find this project helpful, please give it a ⭐!

