# run_with_ngrok.py
import os
from app import create_app, db
from pyngrok import ngrok
import threading

app = create_app()

# Create DB tables if missing (safe for dev)
with app.app_context():
    db.create_all()

def start_ngrok():
    # Start ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"\n🌐 Your app is now accessible at: {public_url}")
    print(f"📱 Share this link with anyone: {public_url}")
    print(f"🔧 Local URL: http://127.0.0.1:5000")
    print(f"⚡ To stop, press Ctrl+C\n")

if __name__ == "__main__":
    # Start ngrok in background
    ngrok_thread = threading.Thread(target=start_ngrok)
    ngrok_thread.daemon = True
    ngrok_thread.start()
    
    # Give ngrok a moment to start
    import time
    time.sleep(2)
    
    # Start Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # Set debug=False for ngrok
