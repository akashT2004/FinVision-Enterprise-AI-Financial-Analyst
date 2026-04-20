# 💎 FinVision: Enterprise AI Financial Analyst

**FinVision** is a next-generation analytical platform designed to transform raw financial documents (Annual Reports, Balance Sheets, Invoices) into actionable, visualized intelligence. Using **Retrieval-Augmented Generation (RAG)** and **Agentic Reasoning**, FinVision moves beyond simple text-chat to provide deep computational analysis and professional data visualization.

---

## 🚀 Key Features

### 📊 Agentic Multi-Series Analytics
The core of FinVision is the **AI Analyst Agent**. Unlike standard LLM implementations, it doesn't just answer questions—it analyzes data patterns and generates structured JSON to power interactive **Multi-Series Charts**. 
*   *Example: Compare "Net Sales" vs "Operating Profit" side-by-side automatically.*

### 🔍 High-Precision RAG Pipeline
Utilizing **Qdrant Vector Database** and **Sentence-Transformers**, the system performs semantic search across large document repositories. By retrieving only the most relevant "financial chunks," it eliminates AI hallucinations and provides direct citations for every number.

### 🛡️ Enterprise-Grade Security (RBAC)
Built with professional security in mind, the platform features:
*   **JWT Authentication**: Secure session management.
*   **Role-Based Access Control (RBAC)**: Fine-grained permissions for **Admin**, **Analyst**, **Auditor**, and **Client** roles.

### 💎 Premium User Experience
A high-fidelity **Glassmorphic UI** built with **React** and **Framer Motion**, featuring:
*   Real-time financial metric cards.
*   Smart research hub with AI-driven prompt suggestions.
*   Responsive, animated visualization panels.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Artificial Intelligence** | Google Gemini 1.5 Flash (LLM), RAG Pipeline |
| **Vector Engine** | Qdrant (Vector Database) |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **Backend** | FastAPI (Python), SQLAlchemy, SQLite, JWT |
| **Frontend** | React (Vite), Recharts, Framer Motion, Lucide |
| **Styling** | Vanilla CSS3 (Custom Design System) |

---

## 📐 Architecture Overview

```mermaid
graph TD
    User((User)) -->|Query| React_UI[React Research Hub]
    React_UI -->|API Request| FastAPI[FastAPI Backend]
    FastAPI -->|Token Check| Auth[JWT/RBAC Layer]
    Auth -->|Query Vector| VectorDB[Qdrant Vector Store]
    VectorDB -->|Retrieved Chunks| AnalystAgent[AI Analyst Agent]
    AnalystAgent -->|Synthesize| Gemini[Gemini 1.5 Flash]
    Gemini -->|Structured JSON| AnalystAgent
    AnalystAgent -->|Answer + Multi-Series Data| React_UI
    React_UI -->|Render| Recharts[Interactive Visualizations]
```

---

## 🚦 Getting Started

### 1. Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Google Gemini API Key

### 2. Backend Setup
```bash
# Navigate to project root
pip install -r requirements.txt

# Create .env file
# GOOGLE_API_KEY=your_key_here

# Start the server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🐳 Docker Deployment (Professional Path)

To run the entire system identically to how it will behave in the cloud, use Docker:

1.  **Set Environment Variables**:
    Create a `.env` file in the root and add your `GOOGLE_API_KEY`.

2.  **Launch the System**:
    ```bash
    docker-compose up --build
    ```
    This will start the **React UI** (on port 80), the **FastAPI Engine** (on port 8000), and the **Qdrant DB** (on port 6333) as a synchronized team.

3.  **Deploy to Cloud**:
    Simply link this GitHub repository to **Railway.app**. It will detect the `docker-compose.yml` and handle the rest!

---

## 💡 Smart Query Examples

*   **Grouped Comparison**: *"Compare Net Sales and Operating Profit for 2021-2023. Show me a bar chart."*
*   **Trend Tracking**: *"Identify the revenue trend for the MAGGI brand. Use a line chart."*
*   **Risk Assessment**: *"Summarize the top internal control risks and the mitigation strategy found in the report."*

---

## 🔒 Security & Self-Healing
The project includes self-healing database dependencies. Upon the first login of an `admin` user, the system automatically detects missing roles and seeds the database with enterprise permissions to prevent access blockers.

---
© 2026 Financial Document AI System. Built for Precision Financial Research.
