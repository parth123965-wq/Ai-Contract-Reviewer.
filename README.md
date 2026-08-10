# ⚖️ AI Contract Reviewer - Backend REST API & AI Engine

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![LangChain](https://img.shields.io/badge/LangChain-121013?style=for-the-badge&logo=chainlink&logoColor=white)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge)](https://www.trychroma.com/)

An enterprise-grade, asynchronous backend service and neural AI pipeline designed for automated legal contract ingestion, risk detection, indemnification exposure scoring, and clause breakdown.

---

## 🌟 Key Features

- 🔐 **JWT & Session Authentication**: Secure user registration, OAuth2 Bearer token authentication, and HTTP-only session cookie support.
- 📄 **Asynchronous Contract Upload**: Background processing of PDF, DOCX, and text contract files with file validation and storage management.
- ⚡ **Neural LangGraph Pipeline**: Stateful, multi-node RAG (Retrieval-Augmented Generation) graph workflow built using `langgraph`.
- 🔍 **Vector Indexing & Semantic Retrieval**: Sentence-transformer embeddings (`BAAI/bge-small-en-v1.5`) stored in a persistent ChromaDB vector database.
- 🤖 **Google Gemini Neural Scoring**: Integration with Google GenAI SDK (`gemini-2.0-flash` / `gemini-1.5-flash`) for deep clause reasoning, risk scoring (0-100), and legal recommendations.
- 🛡️ **Resilient Fallback Engine**: Dynamic text analysis fallback that extracts clause risk indicators and metrics directly from document text if offline or rate-limited.
- 🗄️ **Relational Persistence**: PostgreSQL database managed with SQLAlchemy ORM and Alembic database migration scripts.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Framework** | FastAPI | High-performance ASGI Web Framework |
| **Database** | PostgreSQL | Relational Database Engine |
| **ORM & Migrations**| SQLAlchemy 2.0 & Alembic | Database Modeling & Migration Management |
| **Authentication** | PyJWT & Passlib (Bcrypt) | Password Hashing & OAuth2 Bearer Token Auth |
| **Graph Orchestration**| LangGraph (`StateGraph`) | Directed Acyclic Graph (DAG) for AI Analysis Steps |
| **Vector Database** | ChromaDB | Persistent Local Vector Embeddings Store |
| **Embedding Model** | `SentenceTransformer` | Local Semantic Embeddings (`BAAI/bge-small-en-v1.5`) |
| **LLM Reasoning** | Google GenAI SDK (`google.genai`) | AI Contract Risk Analysis & Clause Summarization |
| **PDF Extraction** | PyMuPDF (`fitz`) | Text Extraction & Document Parsing |

---

## 🔄 AI Engine Analysis Pipeline (LangGraph Workflow)

```mermaid
graph TD
    A[Upload Contract PDF] --> B[extract_node: Parse Text via PyMuPDF]
    B --> C[chunk_node: Split Text via RecursiveCharacterTextSplitter]
    C --> D[embedding_node: Generate Sentence Embeddings]
    D --> E[vector_store_node: Store Embeddings in ChromaDB]
    E --> F[retrieve_context_node: Query Top Context Chunks]
    F --> G[prompt_node: Construct Legal Prompt Context]
    G --> H[llm_node: Google Gemini 2.0 / 1.5 Model Inference]
    H --> I[parser_node: Validate & Parse Structured JSON Result]
    I --> J[save_analysis_node: Persist Analysis to PostgreSQL]
    J --> K[Update Status to COMPLETED]
```

---

## 📁 Repository Directory Structure

```text
ai-contract-reviewer/
├── ai_engine/                    # Neural AI Engine & Graph Pipeline
│   ├── graph/                    # LangGraph State & Node Definitions
│   │   ├── graph.py              # StateGraph Builder & Edge Assembler
│   │   ├── nodes.py              # Node Implementation Functions
│   │   └── state.py              # TypedDict ContractState Schema
│   ├── schemas/                  # Analysis Result Pydantic Schemas
│   ├── services/                 # AI Component Services
│   │   ├── chunk_service.py      # Recursive Text Chunking
│   │   ├── embedding_service.py  # SentenceTransformer Embeddings
│   │   ├── llm_service.py        # Gemini API & Dynamic Fallback Engine
│   │   ├── parser_service.py     # Resilient JSON Parsing
│   │   ├── prompt_service.py     # Legal Prompt Engineering
│   │   ├── save_analysis.py      # Result Storage Service
│   │   ├── text_extractor.py     # PDF Text Extraction
│   │   └── vector_store_service.py # ChromaDB Queries
│   └── vector_store/             # ChromaDB Persistent Storage Path
│
├── app/                          # Core FastAPI Application
│   ├── api/                      # Router Controllers (auth, contracts, users)
│   │   ├── auth.py               # Auth & Session Endpoints
│   │   ├── contracts.py          # Contract Management & Upload Endpoints
│   │   └── users.py              # User Profile Endpoints
│   ├── core/                     # Application Settings & Configuration
│   ├── database/                 # SQLAlchemy Engine & Session Providers
│   ├── models/                   # SQLAlchemy Database Table Models
│   ├── repositories/             # Repository Pattern Data Access Layer
│   ├── schemas/                  # Request & Response Pydantic Models
│   └── services/                 # Business Logic Services
│
├── alembic/                      # Database Migration Scripts
├── uploads/                      # Uploaded Contract Storage Directory
├── .env                          # Environment Configuration File
├── alembic.ini                   # Alembic Configuration
├── requirements.txt              # Python Dependencies
└── README.md                     # Documentation
```

---

## 🔌 API Endpoints Specification

### 🔐 Authentication Router (`/auth`)

| Method | Endpoint | Description | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/auth/register` | Register new user account | `{ email, password, username }` | `UserResponse` |
| `POST` | `/auth/login` | Login user & receive JWT token | `{ email, password }` | `{ access_token, token_type, user }` |
| `POST` | `/auth/token` | OAuth2 Password form login | `OAuth2PasswordRequestForm` | `{ access_token, token_type, user }` |
| `POST` | `/auth/logout` | Logout & clear session cookie | None | `{ message }` |

### 👤 User Router (`/users`)

| Method | Endpoint | Description | Headers | Response |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/users/me` | Fetch active user profile | `Authorization: Bearer <token>` | `UserResponse` |

### 📄 Contracts Router (`/contracts`)

| Method | Endpoint | Description | Request | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/contracts/upload` | Upload contract & trigger AI graph | `multipart/form-data (file)` | `ContractResponse` |
| `GET` | `/contracts` | List all contracts for active user | `Authorization: Bearer <token>` | `ContractListResponse` |
| `GET` | `/contracts/{contract_id}` | Fetch contract details & AI analysis | `Authorization: Bearer <token>` | `ContractResponse` |
| `DELETE`| `/contracts/{id}` | Soft delete contract record | `Authorization: Bearer <token>` | `{ status: "success" }` |

---

## 🛠️ Environment Configuration (`.env`)

Create a `.env` file in the root directory:

```ini
APP_NAME = "AI Contract Reviewer"
APP_VERSION = "1.0.0"
DEBUG = True
DATABASE_URL = "postgresql://postgres:password@localhost:5432/contract_reviewers"
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
UPLOAD_DIR = "uploads/contracts"
LOG_LEVEL = "INFO"

# AI Engine Configuration
MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "contracts"
CHROMA_DB_PATH = "ai_engine/vector_store"
AI_MODEL_NAME = "gemini-2.0-flash"
GOOGLE_API_KEY = "AIzaSy..."
GEMINI_API_KEY = "AIzaSy..."
```

---

## 🚀 Local Installation & Setup

### Prerequisites

- **Python**: `v3.10` or higher
- **PostgreSQL**: Running instance on `localhost:5432`
- **Git**

### 1. Clone Repository & Setup Virtual Environment

```bash
git clone https://github.com/your-username/ai-contract-reviewer.git
cd ai-contract-reviewer

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database & Run Migrations

Ensure PostgreSQL is running and database `contract_reviewers` exists:

```bash
# Run database migrations using Alembic
alembic upgrade head
```

### 4. Start Application Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access Interactive API Documentation (Swagger UI) at:
- **Swagger Docs**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🛡️ License

Distributed under the **MIT License**. See `LICENSE` for more information.
