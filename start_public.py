import subprocess
import time
import requests
from pyngrok import ngrok, conf
import threading
from working_app import app

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        print("🌐 Creating Ngrok tunnel to localhost:5000...")
        public_tunnel = ngrok.connect(5000)
        ngrok_url = public_tunnel.public_url
        print(f"✅ Ngrok tunnel created: {ngrok_url}")
        print(f"🦷 Dental Clinic Management System is now publicly accessible!")
        print(f"🔗 Public URL: {ngrok_url}")
        print(f"📋 Test credentials: admin@smile.com / admin123")
        return ngrok_url
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        return None

def run_flask():
    """Run Flask app"""
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(3)
    
    # Start ngrok
    ngrok_url = start_ngrok()
    
    if ngrok_url:
        print("\n" + "="*60)
        print("🎉 DENTAL CLINIC MANAGEMENT SYSTEM IS LIVE!")
        print("="*60)
        print(f"🌐 Public URL: {ngrok_url}")
        print(f"📱 Local URL: http://localhost:5000")
        print(f"👨‍⚕️ Test Login: admin@smile.com / admin123")
        print(f"📊 Features: Advanced Analytics, Patient Management, Reports")
        print("="*60)
        print("Press Ctrl+C to stop the server")
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            ngrok.disconnect(ngrok_url)
            ngrok.kill()
    else:
        print("❌ Failed to create public tunnel. App running locally at http://localhost:5000")
