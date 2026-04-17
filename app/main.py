from fastapi import FastAPI
from app.models.database import engine, Base
from app.api import auth, roles, users, documents, rag

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Management API", version="1.0.0")

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(rag.router)

@app.get("/")
def root():
    return {"message": "Welcome to Financial Document Management API"}
