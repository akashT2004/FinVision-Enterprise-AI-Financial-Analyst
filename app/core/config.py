from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkey_for_financial_app"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    UPLOAD_DIR: str = "./uploaded_docs"
    QDRANT_PATH: str = "./qdrant_data"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    GOOGLE_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
