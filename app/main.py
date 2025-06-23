from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app.routers import auth, claims, reports
from app.core.config import settings

# Defining our table structure
Base.metadata.create_all(bind=engine)

# Rate limiting for preventing spam attacks
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title=settings.app_name,description="Healthcare Claims Processing API")

# Add CORS middleware
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(auth.router)
app.include_router(claims.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Healthcare Claims Processing API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}