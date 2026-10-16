from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import model
from routes.grievance import router as grievance_router
from schemes.router import router as scheme_router





Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Multilingual Assistant",
    description="Backend API for Multilingual Grievance & AI Assistant System",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grievance_router)
app.include_router(scheme_router)
@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Multilingual Grievance & AI Assistant API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

