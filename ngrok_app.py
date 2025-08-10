# ngrok_app.py - Working version with ngrok
from pyngrok import ngrok
import threading
import time

# Set your ngrok auth token
ngrok.set_auth_token("316jwPa6yl5RvmjWAEuBqe543QH_2aWxnmevneHN7wk7zhzHQ")

def start_flask():
    """Start the simple Flask app"""
    from simple_app import app
    print("🚀 Starting Flask application...")
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

def create_ngrok_tunnel():
    """Create ngrok tunnel"""
    time.sleep(3)  # Wait for Flask to start
    
    try:
        # Create tunnel
        public_url = ngrok.connect(5000)
        print(f"\n🎉 SUCCESS! Your Dental Clinic App is LIVE!")
        print(f"🌐 PUBLIC URL: {public_url}")
        print(f"🔗 Share this link with anyone!")
        print(f"📱 Mobile friendly and secure HTTPS")
        print(f"🔧 Local URL: http://127.0.0.1:5000")
        print(f"\n📋 Demo Credentials:")
        print(f"   Login ID: COMP001, TECH002, etc.")
        print(f"   Password: pass123")
        print(f"\n🏥 Features Available:")
        print(f"   • Register new clinics")
        print(f"   • Add patients")
        print(f"   • View patient records")
        print(f"   • Secure login system")
        print(f"\n⚡ Press Ctrl+C to stop the server")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Ngrok tunnel failed: {e}")
        print("🔧 Check your internet connection and try again")

if __name__ == "__main__":
    print("🔧 Setting up ngrok tunnel...")
    print("🦷 Dental Clinic Management System")
    print("-" * 40)
    
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
        try:
            ngrok.disconnect(ngrok.get_tunnels()[0].public_url)
            ngrok.kill()
        except:
            pass
