# Financial Document Management System with Semantic Search (RAG)

A professional FastAPI-based backend for managing financial documents, featuring Role-Based Access Control (RBAC) and high-precision semantic retrieval using a two-stage RAG pipeline (Vector Search + Reranking).

## 🚀 Features

-   **FastAPI Framework**: High-performance, asynchronous API.
-   **JWT Authentication**: Secure user management with persistent token-based sessions.
-   **Role-Based Access Control (RBAC)**: Fine-grained permissions for `Admin`, `Analyst`, `Auditor`, and `Client`.
-   **AI-Powered Semantic Search (RAG)**:
    -   **Document Processing**: Automatic PDF text extraction and recursive chunking.
    -   **Vector Database**: Integrated with **Qdrant** (local storage mode).
    -   **Embeddings**: Local HuggingFace embeddings (`all-MiniLM-L6-v2`)—no external API keys required.
    -   **Reranking**: Advanced two-stage retrieval with a **Cross-Encoder reranker** (`ms-marco-MiniLM-L-6-v2`) for superior precision.
-   **Relational Storage**: SQLAlchemy-managed SQLite database for metadata and user records.

## 🛠 Tech Stack

-   **Language**: Python 3.10+
-   **Framework**: FastAPI
-   **ORM**: SQLAlchemy
-   **Vector DB**: Qdrant
-   **AI Stack**: LangChain, HuggingFace, Sentence-Transformers
-   **Auth**: PyJWT, Passlib (Bcrypt)

## 🏗 Setup & Installation

1.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Running the Application

Start the local development server:

```bash
.\venv\Scripts\uvicorn app.main:app --reload
```

-   **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **Root Endpoint**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🧪 Testing Flow

To test the system from the Swagger UI (`/docs`), follow these steps:

1.  **Register**: Create a user account via `POST /auth/register`.
2.  **Login**: Authenticate via `POST /auth/login` and copy the `access_token`.
3.  **Authorize**: Click the green "Authorize" button at the top and paste your token.
4.  **Roles**:
    -   Create a role (e.g., "Admin") via `POST /roles/create`.
    -   Assign the role to your user via `POST /users/{id}/assign-role`.
5.  **Upload**: Upload a financial PDF via `POST /documents/upload`.
6.  **Search**: Perform a semantic search via `POST /rag/search`. The system will retrieve relevant chunks and rerank them for the best context match.

## 📁 Project Structure

```text
├── app/
│   ├── api/          # Route handlers (auth, documents, rag, roles, users)
│   ├── core/         # Security, config, and dependencies
│   ├── models/       # SQLAlchemy ORM models
│   ├── schemas/      # Pydantic validation schemas
│   ├── services/     # Document extraction and RAG logic
│   └── main.py       # FastAPI entry point
├── uploaded_docs/    # physical PDF storage (auto-created)
├── qdrant_data/     # Vector database storage (auto-created)
├── requirements.txt  # Project dependencies
└── financial_docs.db # SQLite database (auto-created)
```
