# create_public_link.py
import subprocess
import threading
import time
import requests
from app import create_app, db

def start_flask():
    """Start Flask app"""
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def create_tunnel():
    """Create public tunnel using serveo"""
    time.sleep(3)  # Wait for Flask to start
    
    print("\n🌐 Creating public tunnel...")
    print("📱 Your app will be available at a public URL in a moment...")
    
    # Using serveo.net for tunneling
    try:
        result = subprocess.run([
            "ssh", "-o", "StrictHostKeyChecking=no", 
            "-R", "80:localhost:5000", "serveo.net"
        ], capture_output=True, text=True, timeout=30)
        
        if "https://" in result.stdout:
            url = result.stdout.split("https://")[1].split()[0]
            print(f"\n✅ Your app is live at: https://{url}")
        else:
            print("❌ Could not create tunnel. Try manual deployment.")
            
    except Exception as e:
        print(f"❌ Tunnel creation failed: {e}")
        print("\n🔧 Alternative: Your app is running locally at http://127.0.0.1:5000")
        print("📋 To share it, you can:")
        print("   1. Use ngrok: Download from https://ngrok.com/")
        print("   2. Deploy to Vercel: Push to GitHub and connect to Vercel")
        print("   3. Use GitHub Codespaces for instant cloud development")

if __name__ == "__main__":
    # Start Flask in background
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Create tunnel
    create_tunnel()
