"""
Flask Web Application for Facial Expression Recognition
Supports image upload and webcam detection
"""

import os
import io
import base64
import numpy as np
import sys
from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
import torch.nn.functional as F
from torchvision import transforms
import cv2

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import the model
from models.fer_model import get_model, load_trained_model, EMOTION_LABELS, EMOTION_EMOJIS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model
MODEL_PATH = 'models/fer_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize model
try:
    model = load_trained_model(MODEL_PATH, device=device)
    print(f"✓ Model loaded successfully on {device}")
except FileNotFoundError:
    print("⚠ Model file not found. Please train the model first.")
    model = None


# Image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((48, 48)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])


def detect_face(image):
    """
    Detect face in image using OpenCV's Haar Cascade
    
    Args:
        image: PIL Image or numpy array
    
    Returns:
        cropped face image or None if no face detected
    """
    # Convert to OpenCV format
    if isinstance(image, Image.Image):
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        img_cv = image.copy()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Load face cascade (using OpenCV's default)
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(48, 48)
    )
    
    if len(faces) == 0:
        return None
    
    # Get the largest face
    largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
    x, y, w, h = largest_face
    
    # Crop face
    face_roi = gray[y:y+h, x:x+w]
    
    # Resize to 48x48
    face_resized = cv2.resize(face_roi, (48, 48))
    
    # Convert to PIL Image
    face_pil = Image.fromarray(face_resized)
    
    return face_pil


def predict_emotion(image):
    """
    Predict emotion from facial image
    
    Args:
        image: PIL Image of face
    
    Returns:
        dict with emotion labels and probabilities
    """
    if model is None:
        # Demo mode: Generate mock predictions for testing
        print("⚠️  Running in DEMO MODE - Using mock predictions")
        print("   Train a model for real predictions!")
        
        # Generate random but realistic probabilities
        np.random.seed(hash(image.tobytes()) % 1000)  # Deterministic based on image
        probs = np.random.dirichlet([1.5, 1.5, 1.5, 2.5, 1.5, 1.5, 2.0])  # Bias towards Happy/Neutral
        
        # Create results dictionary
        results = {}
        for idx, emotion in EMOTION_LABELS.items():
            results[emotion] = {
                'probability': float(probs[idx]),
                'percentage': float(probs[idx] * 100),
                'emoji': EMOTION_EMOJIS[emotion]
            }
        
        # Get predicted emotion
        predicted_idx = np.argmax(probs)
        predicted_emotion = EMOTION_LABELS[predicted_idx]
        
        return {
            'predicted_emotion': predicted_emotion,
            'confidence': float(probs[predicted_idx]),
            'confidence_percentage': float(probs[predicted_idx] * 100),
            'emoji': EMOTION_EMOJIS[predicted_emotion],
            'all_emotions': results,
            'demo_mode': True
        }
    
    # Real model predictions
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    # Predict
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = F.softmax(outputs, dim=1)
    
    # Get probabilities
    probs = probabilities[0].cpu().numpy()
    
    # Create results dictionary
    results = {}
    for idx, emotion in EMOTION_LABELS.items():
        results[emotion] = {
            'probability': float(probs[idx]),
            'percentage': float(probs[idx] * 100),
            'emoji': EMOTION_EMOJIS[emotion]
        }
    
    # Get predicted emotion
    predicted_idx = np.argmax(probs)
    predicted_emotion = EMOTION_LABELS[predicted_idx]
    
    return {
        'predicted_emotion': predicted_emotion,
        'confidence': float(probs[predicted_idx]),
        'confidence_percentage': float(probs[predicted_idx] * 100),
        'emoji': EMOTION_EMOJIS[predicted_emotion],
        'all_emotions': results
    }


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/healthsphere')
def healthsphere():
    """Render Healthsphere interface"""
    return render_template('healthsphere.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for emotion prediction"""
    try:
        # Get image from request
        if 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
        
        # Decode base64 image
        image_data = request.json['image']
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Detect face
        face = detect_face(image)
        
        if face is None:
            return jsonify({
                'error': 'No face detected in the image. Please try another image.'
            }), 400
        
        # Predict emotion
        result = predict_emotion(face)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload():
    """API endpoint for file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read image
        image = Image.open(io.BytesIO(file.read()))
        
        # Convert RGBA to RGB if needed
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        # Detect face
        face = detect_face(image)
        
        if face is None:
            return jsonify({
                'error': 'No face detected in the image. Please try another image.'
            }), 400
        
        # Predict emotion
        result = predict_emotion(face)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'device': str(device)
    })


@app.route('/mobile-info')
def mobile_info():
    """Mobile access information"""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    
    return f"""
    <html>
    <head>
        <title>Mobile Access Info</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; background: #f0f0f0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            .url {{ background: #e8f4fd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
            .warning {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Mobile Access Information</h1>
            <p><strong>Your Computer's IP:</strong> {local_ip}</p>
            
            <div class="url">
                <h3>Healthsphere UI:</h3>
                <a href="http://{local_ip}:5000/healthsphere">http://{local_ip}:5000/healthsphere</a>
            </div>
            
            <div class="url">
                <h3>Original UI:</h3>
                <a href="http://{local_ip}:5000">http://{local_ip}:5000</a>
            </div>
            
            <div class="warning">
                <h3>⚠️ Mobile Camera Issues:</h3>
                <ul>
                    <li>Camera access requires HTTPS on mobile browsers</li>
                    <li>Use Chrome or Safari for best compatibility</li>
                    <li>Allow camera permissions when prompted</li>
                    <li>Try "Upload Image" option if camera doesn't work</li>
                </ul>
            </div>
            
            <p><a href="/healthsphere">← Back to Healthsphere</a></p>
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Facial Expression Recognition Web App")
    print("=" * 60)
    print(f"📱 Device: {device}")
    print(f"🤖 Model loaded: {model is not None}")
    
    if model is None:
        print("\n⚠️  DEMO MODE ACTIVE")
        print("   Running with mock predictions for testing")
        print("   Train a model for real emotion detection!")
        print("   Run: python train.py")
    
    print("\n🌐 Starting Flask server...")
    print("📍 Open your browser at: http://localhost:5000")
    print("📍 Healthsphere UI: http://localhost:5000/healthsphere")
    print("\n📱 For Mobile Devices:")
    print("   • Use your computer's IP address instead of localhost")
    print("   • Example: http://192.168.29.78:5000/healthsphere")
    print("   • Camera access requires HTTPS on mobile browsers")
    print("   • Try the 'Upload Image' option if camera doesn't work")
    print("\n🔒 For HTTPS (Mobile Camera Access):")
    print("   • Run: python generate_cert.py")
    print("   • Then: python run_https.py")
    print("   • Or use: setup_https.bat (Windows)")
    print("   • Access: https://192.168.29.78:5000 on mobile")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

