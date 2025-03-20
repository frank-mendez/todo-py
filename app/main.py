from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import router as api_router
from app.core.logging import setup_logging, get_logger
from app.db.init_db import init_db
from app.db.session import SessionLocal

# Setup logging
setup_logging(settings.DEBUG)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    from scripts.create_db import create_database
    
    try:
        # Ensure database exists
        create_database()
        
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import socket
    from app.core.logging import logger

    port = settings.SERVER_PORT
    while port < settings.SERVER_PORT + 10:  # Try up to 10 ports
        try:
            # Test if port is available
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((settings.SERVER_HOST, port))
                break
        except OSError:
            logger.warning(f"Port {port} is in use, trying {port + 1}")
            port += 1
    else:
        logger.error("Could not find an available port")
        raise SystemExit(1)

    logger.info(f"Starting server on {settings.SERVER_HOST}:{port}")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=port,
        reload=settings.SERVER_RELOAD
    )
