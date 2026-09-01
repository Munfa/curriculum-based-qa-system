# Curriculum-Based Question Answering System

A curriculum-grounded study assistant for Bangladeshi school textbooks. The project combines a vanilla JavaScript frontend, a FastAPI backend, semantic retrieval from a local Chroma vector database, and Gemini-based generation and grading.

Students can browse the available classes, subjects, and chapters, ask textbook questions, generate multiple-choice questions (MCQs), generate creative questions (CQs), and submit answers for grading.

## Main Features

- Curriculum metadata browsing by class, subject, and chapter
- Retrieval-augmented question answering (RAG)
- Textbook-grounded MCQ generation
- Immediate MCQ grading
- Bangladeshi curriculum-style CQ generation
- AI-assisted CQ grading with feedback
- Local persistent Chroma vector index
- Bangla and English curriculum support
- Responsive frontend built without a JavaScript framework
- Optional frontend mock implementation for UI-only development

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- ChromaDB
- Sentence Transformers
- `intfloat/multilingual-e5-large` embedding model
- Google Gemini through `google-genai`
- `python-dotenv`

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- Browser Fetch API

### Data and retrieval

- NCTB SchoolText-derived JSONL chunks
- Persistent Chroma vector database
- 1,024-dimensional multilingual E5 embeddings
- JSON question-pattern examples for MCQ and CQ prompting

## Required Python Version

The repository's `.python-version` declares:

```text
3.11
```

Use Python 3.11.x. Python 3.12 may work with compatible dependency versions, but Python 3.11 is the intended and documented runtime.

Check the installed version:

```powershell
python --version
```

Expected output resembles:

```text
Python 3.11.x
```

## Project Structure

```text
curriculum-based-qa-system/
|
|-- .python-version                  # Declares Python 3.11
|-- .gitignore                       # Ignore rules and retrieval-artifact exceptions
|-- requirements.txt                 # Backend Python dependencies
|-- README.md                        # Main project documentation
|-- api.py                           # Backward-compatible FastAPI entry point
|-- .env.example                    # Safe environment-variable template
|
|-- backend/
|   |-- app.py                       # FastAPI factory and router registration
|   |-- config.py                    # Environment variables and absolute paths
|   |-- schemas.py                   # Pydantic request models
|   |-- dependencies.py              # HTTP input normalization helpers
|   `-- routers/
|       |-- health.py                # Health endpoint
|       |-- metadata.py              # Curriculum metadata endpoints
|       `-- study.py                 # QA, MCQ, and CQ endpoints
|
|-- cleaned/
|   `-- chunks_v1.jsonl              # Cleaned textbook chunks used for metadata
|                                     # and as the source represented by the index
|
|-- index_v1/
|   |-- config.json                  # Embedding model, dimension, and mock flag
|   `-- chroma_db/                   # Persistent Chroma collection files
|
|-- retrieval/
|   |-- __init__.py
|   |-- RETRIEVAL_CONTRACT.md        # Retrieval interface documentation
|   |-- retrieval.py                 # Query embedding, filtering, search, metadata APIs
|   |-- clean_corpus.py              # Raw dataset cleaning and quality-report pipeline
|   `-- build_index.py               # Chroma index build/query utility
|
|-- generation_grading/
|   |-- __init__.py
|   |-- llm.py                       # Gemini client and structured JSON generation
|   |-- build_QA.py                  # RAG answer prompt and response construction
|   |-- build_MCQ.py                 # MCQ retrieval, prompt, generation, answer storage
|   |-- build_CQ.py                  # CQ retrieval, prompt, generation, answer storage
|   |-- grading.py                   # MCQ and CQ grading
|   |-- stores.py                    # Temporary in-memory answer stores
|   `-- get_patterns.py              # Loads and samples exam-style examples
|
|-- question_pattern/
|   |-- mcq_pattern.json             # Active MCQ few-shot examples
|   |-- cq_pattern.json              # Active CQ few-shot examples
|   |-- mcq_question_pattern.json    # Additional/original MCQ pattern data
|   `-- cq_question_pattern.json     # Additional/original CQ pattern data
|
|-- scripts/
|   `-- smoke_test.py                # Direct end-to-end developer smoke test
|
|-- frontend/
|   |-- index.html                   # Application page and script loading
|   |-- README.md                    # Older frontend-specific documentation
|   |-- css/
|   |   `-- styles.css               # Layout, responsive design, states, question UI
|   |-- js/
|   |   |-- config.js                # Real/mock mode and backend base URL
|   |   |-- api.js                   # Frontend API abstraction
|   |   |-- app.js                   # State, events, rendering, QA/MCQ/CQ workflows
|   |   `-- mockApi.js               # Optional in-browser mock backend
|   |-- data/
|   |   `-- nctb_curriculum_2026.json # Frontend mock curriculum metadata
|   `-- tools/
|       `-- build_curriculum.py      # Builds the frontend curriculum JSON
|
`-- extra/                           # Earlier/reference copies and source materials
```

The committed retrieval assets are substantial. At the time of writing, `cleaned/chunks_v1.jsonl` is about 26.7 MB and the Chroma SQLite database is about 123.7 MB. Git LFS may therefore be required to obtain the real binary contents after cloning.

## System Architecture

```text
Browser UI
   |
   | HTTP/JSON
   v
FastAPI backend (api.py)
   |
   +---- Metadata lookup --------> cleaned/chunks_v1.jsonl
   |
   +---- Query embedding --------> multilingual-e5-large
   |                                  |
   |                                  v
   +---- Semantic retrieval -----> ChromaDB (index_v1/chroma_db)
   |                                  |
   |                                  v
   +---- Grounded prompt --------> Gemini 2.5 Flash Lite
                                      |
                                      v
                              Answer / MCQ / CQ / grade
```

## How the Application Works

### 1. Frontend initialization

`frontend/index.html` loads `config.js`, `api.js`, and `app.js`. `app.js` creates the client-side state, caches DOM elements, binds selectors and mode buttons, and calls the metadata endpoints.

With the current configuration:

```javascript
USE_MOCK: false
BASE_URL: "http://127.0.0.1:8002"
```

all study requests are sent to the local FastAPI backend.

### 2. Curriculum metadata

The backend reads `cleaned/chunks_v1.jsonl` and builds a cached class/subject/chapter tree. The frontend requests:

1. available classes;
2. subjects for the selected class;
3. chapters for the selected class and subject.

The metadata tree is cached in the backend process after its first load.

### 3. Semantic retrieval

For a QA, MCQ, or CQ request, `retrieval/retrieval.py`:

1. loads `index_v1/config.json`;
2. loads `intfloat/multilingual-e5-large` through Sentence Transformers;
3. opens the persistent `nctb_schooltext` Chroma collection;
4. prefixes E5 queries with `query: `;
5. embeds the user's query;
6. applies class, subject, and chapter filters;
7. retrieves the top five relevant passages;
8. converts cosine distance into a similarity score.

The embedding model and Chroma collection are loaded once per backend process and cached. The first retrieval can therefore be noticeably slower than later requests.

### 4. Question answering

`generation_grading/build_QA.py` retrieves five textbook passages and builds a prompt that instructs Gemini to use only those passages. It returns:

- a concise student-friendly answer;
- source chapter numbers;
- source chunk IDs.

### 5. MCQ generation and grading

`generation_grading/build_MCQ.py` retrieves textbook passages, samples MCQ style examples from `question_pattern/mcq_pattern.json`, and requests exactly four options with one correct answer.

The correct option is stored in the backend's in-memory `mcq_ans_store`, indexed by a generated UUID. The public generation response does not expose the correct answer. On submission, `grading.py` compares the selected option with the stored answer and returns the score and feedback.

### 6. CQ generation and grading

`generation_grading/build_CQ.py` retrieves passages, samples CQ examples, and generates:

- one stimulus;
- four linked parts: `ka`, `kha`, `ga`, and `gha`;
- hidden reference answers for all four parts.

Reference answers are stored in the backend's in-memory `cq_ans_store`. During grading, each student answer is compared with its reference answer by Gemini. The API returns a score and feedback for every part plus the total.

### 7. Frontend rendering

The frontend never calls `fetch()` directly from its UI handlers. `app.js` calls the methods in `api.js`, which makes it possible to switch between real and mock backends without rewriting the UI.

`app.js` is responsible for:

- selection state and progress indicators;
- QA, MCQ, and CQ mode switching;
- difficulty selection;
- request loading and error states;
- question and answer rendering;
- MCQ and CQ submission;
- grading feedback and score animation;
- HTML escaping before inserting generated text.

## API Endpoints

FastAPI also provides interactive documentation at `http://127.0.0.1:8002/docs`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Lightweight backend availability check |
| GET | `/metadata/classes` | List available classes |
| GET | `/metadata/subjects?class=6` | List subjects for a class |
| GET | `/metadata/chapters?class=6&subject=Science` | List chapters |
| POST | `/qa` | Answer a textbook-grounded question |
| POST | `/mcq/generate` | Generate one MCQ |
| POST | `/mcq/grade` | Grade a generated MCQ answer |
| POST | `/cq/generate` | Generate one CQ |
| POST | `/cq/grade` | Grade answers to a generated CQ |

### QA request example

```json
{
  "class": 6,
  "subject": "Science",
  "chapter": 5,
  "question": "What is photosynthesis?"
}
```

### MCQ generation request example

```json
{
  "class": 6,
  "subject": "Science",
  "chapter": 5,
  "difficulty": "medium"
}
```

### MCQ grading request example

```json
{
  "question_id": "generated-question-uuid",
  "selected_option": "The complete option text"
}
```

### CQ generation request example

```json
{
  "class": 6,
  "subject": "Science",
  "chapter": 5,
  "difficulty": "medium"
}
```

### CQ grading request example

```json
{
  "question_id": "generated-question-uuid",
  "student_answers": {
    "ka": "Answer to part ka",
    "kha": "Answer to part kha",
    "ga": "Answer to part ga",
    "gha": "Answer to part gha"
  }
}
```

## Installation

### 1. Clone and enter the repository

```powershell
git clone <repository-url>
cd "curriculum-based-qa-system"
```

If the repository uses Git LFS, install Git LFS and fetch the retrieval artifacts:

```powershell
git lfs install
git lfs pull
```

Confirm that these files are present and non-empty:

```powershell
Get-Item ".\cleaned\chunks_v1.jsonl"
Get-Item ".\index_v1\config.json"
Get-Item ".\index_v1\chroma_db\chroma.sqlite3"
```

### 2. Create a Python 3.11 virtual environment

If an existing `.venv` points to a deleted Python installation, remove or rename that environment first, then create a new one.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, either adjust the current-user execution policy or run the environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to a `.env` file in the repository root:

```powershell
Copy-Item .env.example .env
```

Then open `.env` and replace the placeholder:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

Do not commit `.env`; it is already ignored by Git.

The backend can start and serve health/metadata routes without this key. QA generation, MCQ generation, CQ generation, and CQ grading require it.

### 4. Verify the frontend backend URL

`frontend/js/config.js` should contain:

```javascript
const CONFIG = {
  USE_MOCK: false,
  BASE_URL: "http://127.0.0.1:8002",
  MOCK_LATENCY_MS: 250,
};
```

## Running the Project

Use two PowerShell terminals.

### Terminal 1: start the backend

From the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.app:app --host 127.0.0.1 --port 8002 --reload
```

Alternatively:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8002 --reload
```

Verify it:

```powershell
Invoke-RestMethod http://127.0.0.1:8002/health
```

Expected result:

```text
status
------
ok
```

### Terminal 2: start the frontend

```powershell
cd frontend
..\.venv\Scripts\python.exe -m http.server 8000
```

Open:

```text
http://127.0.0.1:8000
```

Do not open `frontend/index.html` directly with a `file:///` URL. Running an HTTP server avoids browser restrictions and makes asset loading reliable.

### Stop the services

Press `Ctrl+C` in each terminal.

## Quick Functional Test

1. Open `http://127.0.0.1:8002/health` and confirm `{"status":"ok"}`.
2. Open `http://127.0.0.1:8002/docs` and try `GET /metadata/classes`.
3. Open `http://127.0.0.1:8000`.
4. Select a class, subject, and a specific chapter.
5. Use **Ask Question** and submit a textbook-related question.
6. Generate and submit an MCQ.
7. Generate a CQ, answer its four parts, and submit it for grading.
8. Check the backend terminal and browser developer console if a request fails.

For the most reliable retrieval test, choose a specific chapter. `All Chapters` is sent as a literal string by the current frontend and is not currently translated into an unfiltered `null` chapter by the backend.

## Running the Direct Python Demo

`scripts/smoke_test.py` directly runs QA, MCQ, CQ, and metadata calls with hard-coded values:

```powershell
.\.venv\Scripts\python.exe -m scripts.smoke_test
```

It is a developer smoke-test script, not the web application entry point. It requires the retrieval assets, embedding model, internet access to Gemini, and a valid API key.

## Frontend Mock Mode

Mock mode is useful when developing only the interface.

1. Set `USE_MOCK: true` in `frontend/js/config.js`.
2. Uncomment this line in `frontend/index.html`:

```html
<script src="js/mockApi.js"></script>
```

3. Start the frontend HTTP server.

In mock mode, metadata comes from `frontend/data/nctb_curriculum_2026.json`, while generated answers and grades are browser-side placeholders. No FastAPI server or Gemini key is required.

## Rebuilding Retrieval Data

The ready-to-run repository already contains cleaned chunks and an index. Rebuild them only when the source dataset or cleaning/indexing logic changes.

### Clean an extracted dataset

Intended command:

```powershell
python retrieval\clean_corpus.py --root "<path-to-extracted-nctb-dataset>" --out cleaned
```

The cleaner quarantines chunks that fail the quality threshold, are too short, or appear fragmented. Review the chosen thresholds before a production rebuild.

### Build a new vector index

```powershell
python retrieval\build_index.py `
  --input cleaned\chunks_clean.jsonl `
  --out_dir index_v1 `
  --model intfloat/multilingual-e5-large
```

The first real index build downloads the embedding model from Hugging Face and can require significant time, memory, disk space, and network bandwidth.

For pipeline-only testing, mock embeddings are available:

```powershell
python retrieval\build_index.py `
  --input cleaned\chunks_clean.jsonl `
  --out_dir index_test `
  --mock_embeddings
```

Do not use a mock-embedding index for real retrieval quality.

### Query an index from the command line

```powershell
python retrieval\build_index.py `
  --out_dir index_v1 `
  --query "photosynthesis" `
  --filter_class 6 `
  --filter_subject Science `
  --top_k 5
```

## Environment Variables

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `GEMINI_API_KEY` | For AI operations | None | Authenticates Gemini requests |
| `gemini_api_key` | Alternative | None | Lowercase fallback for the same key |
| `BANGLA_QA_INDEX` | No | `index_v1` | Overrides the index directory |
| `BANGLA_QA_CHUNKS` | No | `cleaned/chunks_v1.jsonl` | Overrides the metadata chunk file |

Run the backend from the repository root when using the default relative paths.

## Runtime and Deployment Notes

- CORS currently allows every origin. Restrict `allow_origins` before a production deployment.
- MCQ correct answers and CQ reference answers are stored only in process memory.
- Restarting the backend invalidates previously generated question IDs.
- Multiple Uvicorn workers do not share those in-memory stores; generation and grading may reach different workers. Use one worker for the current design or move answer state to a shared database/cache.
- The first retrieval loads the multilingual E5 model and may be slow.
- The embedding model may download on first use if it is not already cached.
- AI operations require network access to Google's Gemini service.
- `--reload` is convenient for development but should not be used in production.
- The frontend and backend ports are intentionally different: frontend `8000`, backend `8002`.
- FastAPI converts backend exceptions into HTTP error responses; details appear in the frontend error state and backend logs.

## Troubleshooting

### Existing `.venv` does not start

The environment may reference a Python executable that no longer exists. Install Python 3.11 and recreate `.venv`.

### `python` or `py` is not recognized

Install Python 3.11, enable the installer option that adds Python to `PATH`, restart PowerShell, and recreate the virtual environment.

### `GEMINI_API_KEY environment variable is not set`

Create the root `.env` file and restart the backend.

### Metadata works but QA/MCQ/CQ fails

Check the Gemini key, network access, model API availability, selected metadata, and backend logs. Metadata does not call Gemini, so it can work while generation fails.

### No relevant textbook passages were retrieved

Confirm that the selected class, subject, and chapter exactly match indexed metadata. Prefer a specific chapter instead of `All Chapters`.

### Chroma collection or index file is missing

Run `git lfs pull` or restore/build `index_v1`. Confirm that the collection name is `nctb_schooltext`.

### Frontend cannot reach the backend

Confirm:

- the backend is listening on port `8002`;
- `/health` returns successfully;
- `BASE_URL` is `http://127.0.0.1:8002`;
- the page was loaded from the frontend HTTP server;
- no firewall or proxy is blocking localhost.

### Browser displays older JavaScript

Use a hard refresh (`Ctrl+F5`) or disable the browser cache while developer tools are open.

## Current Known Limitations

- `All Chapters` is not yet normalized to an unfiltered backend query.
- MCQ/CQ state is volatile and tied to one backend process.
- CQ grading asks Gemini for scores from 1 to 4 for every part; this does not currently enforce conventional per-part Bangladeshi CQ mark weights.
- There is currently no automated test suite in the repository.
- Authentication, rate limiting, persistent student history, and production database storage are not implemented.

## Recommended Development Workflow

1. Use Python 3.11 and a clean virtual environment.
2. Keep retrieval artifacts under the documented paths.
3. start and verify the backend health endpoint;
4. verify metadata through `/docs`;
5. start the frontend server;
6. test one specific class/subject/chapter workflow;
7. test QA, then MCQ generation/grading, then CQ generation/grading;
8. inspect both backend logs and the browser console during failures;
9. add automated API and retrieval tests before production deployment.

## License

See [LICENSE](LICENSE). Ensure that any textbook source data and model/API usage comply with their respective licenses and terms.
