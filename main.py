# Railway entry point
import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set default environment variables if not provided
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'railway-default-secret-key-12345'
    logger.info("Using default SECRET_KEY")

if not os.environ.get('DB_NAME'):
    os.environ['DB_NAME'] = 'gestion_db'
    logger.info("Using default DB_NAME")

logger.info(f"Starting server with PORT: {os.environ.get('PORT', 8000)}")
logger.info(f"MONGO_URL present: {'MONGO_URL' in os.environ}")
logger.info("MongoDB connection check completed")

try:
    from backend.server import app
    logger.info("Successfully imported FastAPI app")
except Exception as e:
    logger.error(f"Failed to import app: {e}")
    raise

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting uvicorn on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
