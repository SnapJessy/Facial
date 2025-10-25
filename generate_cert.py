#!/usr/bin/env python3
"""
Generate self-signed SSL certificate for HTTPS
"""

import os
import subprocess
import sys

def generate_certificate():
    """Generate self-signed certificate for HTTPS"""
    try:
        # Check if OpenSSL is available
        subprocess.run(['openssl', 'version'], check=True, capture_output=True)
        
        print("🔐 Generating self-signed SSL certificate...")
        
        # Generate private key
        subprocess.run([
            'openssl', 'genrsa', '-out', 'key.pem', '2048'
        ], check=True)
        
        # Generate certificate
        subprocess.run([
            'openssl', 'req', '-new', '-x509', '-key', 'key.pem', 
            '-out', 'cert.pem', '-days', '365', '-subj', 
            '/C=US/ST=State/L=City/O=Organization/CN=localhost'
        ], check=True)
        
        print("✅ Certificate generated successfully!")
        print("📁 Files created: cert.pem, key.pem")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ OpenSSL not found. Please install OpenSSL or use alternative method.")
        return False
    except Exception as e:
        print(f"❌ Error generating certificate: {e}")
        return False

def generate_certificate_alternative():
    """Alternative method using Python cryptography library"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        
        print("🔐 Generating self-signed SSL certificate using Python...")
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Organization"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write private key
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Write certificate
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✅ Certificate generated successfully!")
        print("📁 Files created: cert.pem, key.pem")
        return True
        
    except ImportError:
        print("❌ cryptography library not found.")
        print("💡 Install it with: pip install cryptography")
        return False
    except Exception as e:
        print(f"❌ Error generating certificate: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔐 SSL Certificate Generator for Mobile Camera Access")
    print("=" * 60)
    
    # Try OpenSSL first, then Python alternative
    if not generate_certificate():
        print("\n🔄 Trying alternative method...")
        if not generate_certificate_alternative():
            print("\n❌ Could not generate certificate.")
            print("💡 Manual steps:")
            print("1. Install OpenSSL: https://www.openssl.org/")
            print("2. Or install cryptography: pip install cryptography")
            print("3. Or use the Upload Image feature instead")
            sys.exit(1)
    
    print("\n🚀 Now you can run: python run_https.py")
    print("📱 Then access: https://YOUR_IP:5000 on your mobile device")
