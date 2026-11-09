# TalentRank AI — Enterprise Document Intelligence & Resume RAG Engine

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-FF6F61?style=for-the-badge)
![Groq LLM](https://img.shields.io/badge/Groq-Llama_3.1_70B-f05032?style=for-the-badge)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

TalentRank AI is an enterprise-grade Retrieval-Augmented Generation (RAG) system and automated candidate scoring engine. It ingests PDF and DOCX resume documents, verifies technical skill authenticity, and provides structured HR recruiter recommendations alongside deterministic match scoring.

---

## Key Features

- **Metadata-Isolated RAG Engine:** Uses ONNX embeddings in ChromaDB with `file_id` metadata filtering to eliminate context leaking across candidate files.
- **Deterministic Skill Verification:** Implements case-insensitive, bidirectional substring matching to accurately calculate skill coverage percentages without LLM hallucination.
- **Full-Document Recruiter LLM:** Leverages `Llama-3.1-70B` via Groq API to evaluate candidate fit, verify practical skill usage in work experience, and issue HR Verdicts (`Strong Hire`, `Consider`, `Pass`).
- **Interactive Leaderboard & Analytics:** Single-page dashboard built with Tailwind CSS featuring drag-and-drop batch upload, real-time candidate ranking, and one-click CSV export.

---

## System Architecture

```text
 ┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────┐
 │  PDF / DOCX     │ ────> │ PyPDF Text Ingestion │ ────> │ ONNX Vector Store  │
 │ Candidate Files │       │   & Parsing Engine   │       │   (ChromaDB)       │
 └─────────────────┘       └──────────────────────┘       └────────────────────┘
                                                                    │
                                                             Metadata Query
                                                                    │
 ┌─────────────────┐       ┌──────────────────────┐                 ▼
 │ Ranked CSV & UI │ <──── │ Deterministic Match  │ <──── ┌────────────────────┐
 │   Dashboard     │       │ & Llama-3.1 70B LLM  │       │ Isolated Candidate │
 └─────────────────┘       └──────────────────────┘       │  Text Context      │
                                                          └────────────────────┘
```

## Tech Stack

* **Backend Framework:** FastAPI (Python 3.11+)
* **Vector Store:** ChromaDB with `all-MiniLM-L6-v2` ONNX embeddings
* **LLM Engine:** Groq API (`llama-3.1-70b-versatile`)
* **Document Processing:** PyPDF & `pdfminer.high_level`
* **Frontend:** Vanilla JavaScript (ES6+ DataTransfer API), Tailwind CSS

## Repository Structure

```text
enterprise-document-intelligence/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── evaluation.py
│   ├── engines/
│   │   ├── chunker.py
│   │   ├── ingestion.py
│   │   ├── scoring.py
│   │   └── vector_store.py
│   ├── schemas/
│   │   ├── evaluation.py
│   │   ├── job_description.py
│   │   └── resume.py
│   ├── services/
│   │   └── llm_service.py
│   ├── utils/
│   │   └── helpers.py
│   ├── config.py
│   └── main.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── tests/
│   ├── test_chunker.py
│   ├── test_ingestion.py
│   ├── test_llm_service.py
│   ├── test_scoring.py
│   └── test_vector_store.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── test_upload.py
└── uv.lock
```

## Prerequisites

* **Python 3.11** or higher
* **`uv`** package manager (or standard `pip` + `venv`)
* **Groq API Key**

## Installation & Execution

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/enterprise-document-intelligence.git
   cd enterprise-document-intelligence
   ```

2. **Set Environment Variables:**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

3. **Install Dependencies:**
   ```bash
   uv sync
   ```

4. **Launch the Server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

5. **Open Dashboard:**
   Navigate to `http://127.0.0.1:8000/` in your browser.

## License

Distributed under the MIT License. See `LICENSE` for details.