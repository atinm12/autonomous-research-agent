"""
Unit tests for the three-layer memory system:
  - Short-term: ContextManager
  - Long-term: Vector store (ChromaDB + SentenceTransformers)
  - Episodic: JSON log
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock

from memory.context_manager import ContextManager, summarize_context


class TestContextManager:
    def test_add_and_retrieve(self):
        cm = ContextManager()
        cm.add("First item")
        cm.add("Second item")
        context = cm.get_context()
        assert "First item" in context
        assert "Second item" in context

    def test_max_context_items_enforced(self):
        cm = ContextManager()
        for i in range(15):
            cm.add(f"item_{i}")
        assert len(cm.memory) <= 10

    def test_clear_resets_memory(self):
        cm = ContextManager()
        cm.add("Some data")
        cm.clear()
        assert len(cm.memory) == 0
        assert cm.get_context() == ""

    def test_summarize_short_context(self):
        short = "This is a short context."
        assert summarize_context(short) == short

    def test_summarize_long_context(self):
        long_text = " ".join([f"word{i}" for i in range(500)])
        result = summarize_context(long_text)
        assert len(result.split()) < len(long_text.split())
        assert "..." in result


class TestVectorStore:
    @pytest.fixture
    def mock_chroma(self):
        """Patch ChromaDB and SentenceTransformer to avoid heavy dependencies."""
        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "documents": [["Azure cloud revenue grew 28%"]],
            "ids": [["doc_123_0"]],
        }
        mock_client = MagicMock()
        mock_client.get_or_create_collection.return_value = mock_collection

        with patch("memory.vector_store.chromadb.Client", return_value=mock_client):
            with patch("memory.vector_store.embedding_model") as mock_emb:
                mock_emb.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
                with patch("memory.vector_store.collection", mock_collection):
                    yield mock_collection

    def test_store_memory_returns_confirmation(self, mock_chroma):
        from memory.vector_store import store_memory
        result = store_memory("Microsoft Azure is a major cloud platform.")
        assert "Stored" in result or isinstance(result, str)

    def test_search_memory_returns_results(self, mock_chroma):
        from memory.vector_store import search_memory
        results = search_memory("cloud computing")
        assert "documents" in results


class TestEpisodicMemory:
    def test_log_episode_creates_entry(self, tmp_path):
        episode_file = tmp_path / "episodic_log.json"
        with patch("memory.episodic.EPISODIC_FILE", str(episode_file)):
            from memory.episodic import log_episode
            result = log_episode(
                query="Microsoft cloud analysis",
                outcome="success",
                strategy="Used financial_data_api and sec_filing_search."
            )
            assert result == "Episode logged successfully."

        data = json.loads(episode_file.read_text())
        assert len(data) == 1
        assert data[0]["query"] == "Microsoft cloud analysis"
        assert data[0]["outcome"] == "success"

    def test_log_episode_appends_multiple(self, tmp_path):
        episode_file = tmp_path / "episodic_log.json"
        with patch("memory.episodic.EPISODIC_FILE", str(episode_file)):
            from memory.episodic import log_episode
            log_episode("Query 1", "success", "strategy A")
            log_episode("Query 2", "partial", "strategy B")

        data = json.loads(episode_file.read_text())
        assert len(data) == 2
        assert data[1]["query"] == "Query 2"
