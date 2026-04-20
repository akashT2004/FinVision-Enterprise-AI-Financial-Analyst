from fastapi import FastAPI
from app.models.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, roles, users, documents, rag

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Management API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, specify frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "Welcome to Financial Document Management API"}
