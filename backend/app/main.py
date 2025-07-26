from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import connect_to_database, close_database_connection, check_database_health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_database()
    yield
    # Shutdown
    await close_database_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Job Application Automation API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return JSONResponse(
        content={
            "message": "Job Application Automation API",
            "version": settings.VERSION,
            "status": "healthy"
        }
    )

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    db_healthy = await check_database_health()
    
    return JSONResponse(
        content={
            "status": "healthy" if db_healthy else "unhealthy",
            "service": "job-application-automation-api",
            "version": settings.VERSION,
            "database": "connected" if db_healthy else "disconnected"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )