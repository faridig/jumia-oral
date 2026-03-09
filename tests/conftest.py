import os
import unittest.mock
import pytest
import warnings

@pytest.fixture(autouse=True, scope="session")
def silence_warnings():
    # Appliquer le Silence Technique (Guidance Sprint 13)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*urllib3.*")
    yield

@pytest.fixture(autouse=True)
def mock_openai_if_ci():
    if os.getenv("GITHUB_ACTIONS") == "true":
        with unittest.mock.patch("llama_index.llms.openai.OpenAI"), \
             unittest.mock.patch("llama_index.embeddings.openai.OpenAIEmbedding"), \
             unittest.mock.patch("qdrant_client.QdrantClient"):
            yield
    else:
        yield
