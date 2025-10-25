#!/usr/bin/env python3
"""
Run Flask app with HTTPS for mobile camera access
"""

import ssl
import socket
from app import app

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    # Create self-signed certificate context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    
    local_ip = get_local_ip()
    
    print("=" * 60)
    print("🔒 Starting Flask app with HTTPS for mobile camera access")
    print("=" * 60)
    print(f"📍 HTTPS URL: https://{local_ip}:5000")
    print(f"📍 Healthsphere UI: https://{local_ip}:5000/healthsphere")
    print("\n📱 Mobile Instructions:")
    print("1. Open the HTTPS URL above on your phone")
    print("2. Accept the security warning (self-signed certificate)")
    print("3. Allow camera permissions when prompted")
    print("4. Camera should now work on mobile!")
    print("=" * 60)
    
    # Run with HTTPS
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
