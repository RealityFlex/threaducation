from fastapi import FastAPI
from routers import auth
from database.database import engine
from models import models

from fastapi.middleware.cors import CORSMiddleware

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Auth API",
    description="API for authentication and user management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Welcome to the Auth API"}