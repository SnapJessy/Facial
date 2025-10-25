@echo off
echo ============================================================
echo 🔐 Setting up HTTPS for Mobile Camera Access
echo ============================================================
echo.

echo 📋 This will generate SSL certificates for HTTPS access
echo 📱 This allows mobile devices to access the camera
echo.

pause

echo 🔐 Generating SSL certificates...
python generate_cert.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Certificate generation failed
    echo 💡 Try installing cryptography: pip install cryptography
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ SSL certificates generated successfully!
echo.
echo 🚀 Starting HTTPS server...
echo 📱 Use the HTTPS URL shown below on your mobile device
echo.

python run_https.py

pause
