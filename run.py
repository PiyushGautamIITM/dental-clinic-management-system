# run.py
import os
from app import create_app, db

app = create_app()

# Create DB tables if missing (safe for dev)
with app.app_context():
    db.create_all()

# For Vercel deployment
def handler(event, context):
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
