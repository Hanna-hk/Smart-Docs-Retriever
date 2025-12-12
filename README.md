# Smart-Docs-Retriever
Smart Docs Retriever is a semantic search engine designed to help industrial technicians quickly find solutions in massive technical manuals. This tool uses Machine Learning (NLP) to understand the intent behind a query.

## Technical Architecture
The project follows a modular architecture separating the heavy lifting (Indexing) from the user interaction (Searching):
* **Data Loader:** Parses raw .txt logs and manuals using Regex.
* **Indexer:** Generates embeddings and saves them as .npy matrix (Build time).
* **Searcher:** Loads the matrix into RAM and processes user queries (Run time).
* **DB Logger:** Connects to database, inserts and selects queries.

## Tech Stack
* **Language:** Python 3.x
* **AI/ML:** `sentence-transformers` (all-MiniLM-L6-v2) for generating 384-dimensional vector embeddings.
* **Math:** `NumPy` for high-performance matrix operations (Cosine Similarity).
* **Database:** `SQLite` for logging user search history and analytics.
* **Automation:** `Bash` scripting for environment setup and portability.

## How to run
**Prerequisites:**
Python installed
Git bash (if on Windows) or Terminal (Linux/Mac)

1. Clone the repository
```
git clone https://github.com/Hanna-hk/Smart-Docs-Retriever.git
cd Smart-Docs-Retriever
```

2. Run the application
```
./run.sh "Why is the motor vibrating?"
```