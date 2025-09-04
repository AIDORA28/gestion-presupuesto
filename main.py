# Railway entry point
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set default environment variables if not provided
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'railway-default-secret-key-12345'
if not os.environ.get('DB_NAME'):
    os.environ['DB_NAME'] = 'gestion_db'

from backend.server import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
