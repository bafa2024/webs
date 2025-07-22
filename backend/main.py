from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .jobs import router as jobs_router
from .pages import router as pages_router
from .upload import router as upload_router

app = FastAPI(title="Web Scraper Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(pages_router, prefix="/api/v1/pages", tags=["pages"])
app.include_router(upload_router, prefix="/api/v1/upload", tags=["upload"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Web Scraper Pro API"} 