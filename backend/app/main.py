"""FastAPI Application Factory"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.config import get_settings
from app.database import init_db
from app.api import auth, devices, tests, reports, alerts, health
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Network Test Automation Framework API",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*"]
    )
    
    # Initialize database
    init_db()
    
    # Include routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(devices.router)
    app.include_router(tests.router)
    app.include_router(reports.router)
    app.include_router(alerts.router)
    
    # Root endpoint
    @app.get("/")
    def read_root():
        return {
            "message": "Network Test Automation Framework API",
            "version": settings.APP_VERSION,
            "docs": "/api/docs"
        }
    
    @app.on_event("startup")
    def startup_event():
        logger.info(f"Starting {settings.APP_NAME}")
        logger.info(f"Environment: {settings.PYTHON_ENV}")
        logger.info(f"Debug: {settings.DEBUG}")
    
    @app.on_event("shutdown")
    def shutdown_event():
        logger.info(f"Shutting down {settings.APP_NAME}")
    
    return app


app = create_app()
