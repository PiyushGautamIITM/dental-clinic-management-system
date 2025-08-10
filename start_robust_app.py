# start_robust_app.py - Start the robust app with Ngrok tunnel
import subprocess
import time
import sys
import os
from pyngrok import ngrok

# Set your Ngrok auth token
ngrok.set_auth_token("316jwPa6yl5RvmjWAEuBqe543QH_2aWxnmevneHN7wk7zhzHQ")

def start_app():
    print("🚀 Starting Robust Dental Clinic Management System...")
    
    # Start Flask app in background
    print("📱 Starting Flask application...")
    flask_process = subprocess.Popen(
        [sys.executable, "robust_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask to initialize...")
    time.sleep(3)
    
    try:
        # Create Ngrok tunnel
        print("🌐 Creating Ngrok tunnel...")
        public_url = ngrok.connect(5000)
        
        print("\n" + "="*60)
        print("✅ DENTAL CLINIC SYSTEM IS LIVE!")
        print("="*60)
        print(f"🌍 Public URL: {public_url}")
        print(f"💻 Local URL:  http://127.0.0.1:5000")
        print("="*60)
        print("\n🚀 Demo Accounts Ready:")
        print("   Login: CITY001, Password: pass123")
        print("   Login: SMIL001, Password: pass123") 
        print("   Login: DENT001, Password: pass123")
        print("\n✨ Features Available:")
        print("   • Register new clinics")
        print("   • Secure login system")
        print("   • Add & manage patients") 
        print("   • View patient records")
        print("   • Error-free database handling")
        print("\n⚠️  Press Ctrl+C to stop the server")
        print("="*60)
        
        # Keep running
        try:
            flask_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            flask_process.terminate()
            ngrok.disconnect(public_url)
            ngrok.kill()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        flask_process.terminate()
        return False
    
    return True

if __name__ == "__main__":
    start_app()
