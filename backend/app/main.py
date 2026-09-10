from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, students, schools, applications, favorites

# Schema is owned exclusively by Alembic; never create tables at import time.

app = FastAPI(
    title="ApplyCM API",
    description="Backend API for ApplyCM school search and unified application platform",
    version="1.0.0"
)

# CORS middleware configuration for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.CORS_ORIGINS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including API routers under /api namespace
app.include_router(auth.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(schools.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(favorites.router, prefix="/api")




@app.get("/")
def read_root():
    return {"message": "Welcome to the ApplyCM API"}
