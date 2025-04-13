# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import users, tags, education_programs, subjects, change_requests
from database import engine, Base

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academic Platform API",
    description="API for an academic platform with students and educational institutions",
    version="1.0.0",
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
app.include_router(users.router)
app.include_router(tags.router)
app.include_router(education_programs.router)
app.include_router(subjects.router)
app.include_router(change_requests.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Academic Platform API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)