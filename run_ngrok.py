# run_ngrok.py
import os
from app import create_app, db
from pyngrok import ngrok, conf
import threading
import time

# Set your ngrok auth token
ngrok.set_auth_token("316jwPa6yl5RvmjWAEuBqe543QH_2aWxnmevneHN7wk7zhzHQ")

app = create_app()

def start_flask():
    """Start Flask app"""
    with app.app_context():
        db.create_all()
    print("🚀 Starting Flask application...")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def create_ngrok_tunnel():
    """Create ngrok tunnel"""
    time.sleep(3)  # Wait for Flask to start
    
    try:
        # Create tunnel
        public_url = ngrok.connect(5000)
        print(f"\n✅ SUCCESS! Your app is now live at:")
        print(f"🌐 PUBLIC URL: {public_url}")
        print(f"🔗 Share this link with anyone!")
        print(f"📱 Mobile friendly and secure HTTPS")
        print(f"🔧 Local URL: http://127.0.0.1:5000")
        print(f"\n📋 Demo Credentials:")
        print(f"   Login ID: COMP001, TECH002, etc.")
        print(f"   Password: pass123")
        print(f"\n⚡ Press Ctrl+C to stop the server")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Ngrok tunnel failed: {e}")
        print("🔧 Check your internet connection and try again")

if __name__ == "__main__":
    print("🔧 Setting up ngrok tunnel...")
    
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Create ngrok tunnel
    create_ngrok_tunnel()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
        ngrok.kill()
