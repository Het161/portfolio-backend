# ============================================
# FASTAPI MAIN APPLICATION
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Het Patel Portfolio API",
    description="Backend API for Het Patel's portfolio website",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Het Patel's Portfolio API",
        "status": "running",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Portfolio API started successfully!")
    print("📝 API Docs: http://127.0.0.1:8000/docs")
