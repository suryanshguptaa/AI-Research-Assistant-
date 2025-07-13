import os
from pathlib import Path


# Model Configuration
# config/settings.py
MODEL_PATH = r"C:\model\llama-2-7b-chat.Q4_K_M.gguf"
# Updated path
MODEL_TYPE = "llama"
MODEL_CONTEXT_LENGTH = 4096
MODEL_MAX_TOKENS = 512
MODEL_TEMPERATURE = 0.7

# Embedding Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Vector Store Configuration
VECTORSTORE_PERSIST_DIR = "./data/vectorstore"
COLLECTION_NAME = "documents"

# UI Configuration
PAGE_TITLE = "🔬 AI Research Assistant"
PAGE_ICON = "🔬"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# File Upload Configuration
SUPPORTED_FORMATS = ["pdf", "txt", "docx"]
MAX_FILE_SIZE = 200  # MB
AUTO_SUMMARY_MAX_WORDS = 150

# Question Generation Configuration
QUESTION_TYPES = ["factual", "analytical", "inferential", "evaluative"]
NUM_QUESTIONS_GENERATE = 3
EVALUATION_CRITERIA = ["accuracy", "completeness", "relevance", "clarity"]

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"


# Ensure directories exist
for dir_path in [DATA_DIR, DOCUMENTS_DIR, EMBEDDINGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
