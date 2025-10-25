#!/usr/bin/env python3
"""
Get your computer's IP address for mobile device access
"""

import socket

def get_local_ip():
    """Get the local IP address of this computer"""
    try:
        # Connect to a remote server to get local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_local_ip()
    print("=" * 60)
    print("🌐 Your Computer's IP Address for Mobile Access")
    print("=" * 60)
    print(f"📍 IP Address: {ip}")
    print(f"📍 Healthsphere URL: http://{ip}:5000/healthsphere")
    print(f"📍 Original URL: http://{ip}:5000")
    print("\n📱 Mobile Instructions:")
    print("1. Make sure your phone is on the same WiFi network")
    print("2. Open the URL above in your phone's browser")
    print("3. If camera doesn't work, try the 'Upload Image' option")
    print("4. Camera access requires HTTPS on some mobile browsers")
    print("=" * 60)
