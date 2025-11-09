"""
Model caching and initialization for embeddings and NLP models.
Loads models once at startup to improve performance.
"""

import os
from sentence_transformers import SentenceTransformer
import spacy

# Global model instances
_embedding_model = None
_nlp_model = None

def get_embedding_model():
    """
    Returns the sentence transformer model for embeddings.
    Uses 'all-MiniLM-L6-v2' - fast and efficient for semantic similarity.
    """
    global _embedding_model
    if _embedding_model is None:
        print("Loading embedding model (all-MiniLM-L6-v2)...")
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded successfully!")
    return _embedding_model

def get_nlp_model():
    """
    Returns the spaCy NLP model for text processing.
    Uses 'en_core_web_sm' - small English model for entity recognition.
    """
    global _nlp_model
    if _nlp_model is None:
        print("Loading spaCy NLP model (en_core_web_sm)...")
        try:
            _nlp_model = spacy.load('en_core_web_sm')
            print("spaCy model loaded successfully!")
        except OSError:
            print("spaCy model not found. Downloading...")
            os.system("python -m spacy download en_core_web_sm")
            _nlp_model = spacy.load('en_core_web_sm')
            print("spaCy model downloaded and loaded successfully!")
    return _nlp_model

def preload_models():
    """
    Preloads all models at startup.
    Call this when the FastAPI app starts to avoid first-request delays.
    """
    print("Preloading all models...")
    get_embedding_model()
    get_nlp_model()
    print("All models loaded and ready!")
