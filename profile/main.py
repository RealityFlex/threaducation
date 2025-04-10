from fastapi import FastAPI

from api.routers import profile_type_router, user_router
from core.config import settings

# Create FastAPI application
app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(profile_type_router, prefix=settings.API_V1_STR)
app.include_router(user_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to the Education DB API. Go to /docs for documentation."}