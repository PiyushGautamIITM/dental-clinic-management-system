# simple_ngrok.py - Simple Ngrok tunnel for the robust app
from pyngrok import ngrok
import time

# Set your Ngrok auth token
ngrok.set_auth_token("316jwPa6yl5RvmjWAEuBqe543QH_2aWxnmevneHN7wk7zhzHQ")

def create_tunnel():
    try:
        # Create tunnel to localhost:5000
        print("🌐 Creating Ngrok tunnel to localhost:5000...")
        public_url = ngrok.connect(5000)
        
        print("\n" + "="*60)
        print("✅ NGROK TUNNEL CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"🌍 Public URL: {public_url}")
        print(f"💻 Local URL:  http://127.0.0.1:5000")
        print("="*60)
        print("\n🚀 Demo Accounts:")
        print("   Login: CITY001, Password: pass123")
        print("   Login: SMIL001, Password: pass123") 
        print("   Login: DENT001, Password: pass123")
        print("\n✨ Your dental clinic app is now accessible worldwide!")
        print("📱 Test the registration feature - it should work without errors now!")
        print("\n⚠️  Press Ctrl+C to stop the tunnel")
        print("="*60)
        
        # Keep tunnel alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down tunnel...")
            ngrok.disconnect(public_url)
            ngrok.kill()
            print("✅ Tunnel closed.")
            
    except Exception as e:
        print(f"❌ Error creating tunnel: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_tunnel()
