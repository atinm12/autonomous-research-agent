# Autonomous Financial Research Agent

An autonomous AI-powered financial research system that performs multi-source analysis using ReAct reasoning, vector memory, synthesis pipelines, and resilience infrastructure.

---

# Features

- Autonomous ReAct reasoning loop
- SEC EDGAR integration
- Financial data retrieval
- Web search integration
- News sentiment analysis
- Vector memory architecture
- Episodic memory
- Multi-source synthesis
- Fact checking
- Graceful degradation
- Circuit breaker resilience
- Evaluation framework
- Benchmark dashboards

---

# Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| LLM | OpenAI API |
| Orchestration | LangGraph |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers |
| Financial Data | yfinance |
| Search | DuckDuckGo |
| SEC Data | EDGAR |

---

# Project Structure

```text
agent/
memory/
tools/
synthesis/
evaluation/
tests/
results/
docs/
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd autonomous-research-agent
```

---

## 2. Create Virtual Environment

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# API Key Setup

Create a `.env` file in the root directory.

Add:

```env
OPENAI_API_KEY=your_key_here
```

---

# Quick Start

Run the agent:

```bash
python test_agent.py
```

Run memory tests:

```bash
python -m tests.test_memory
```

Run resilience tests:

```bash
python -m tests.test_resilience
```

Run stress tests:

```bash
python -m tests.test_stress
```

---

# System Capabilities

The agent supports:
- autonomous financial research
- memory retrieval
- synthesis reasoning
- contradiction resolution
- resilience recovery
- stress-tested degradation handling

---

# Evaluation

The system includes:
- hallucination detection
- citation validation
- benchmark testing
- token usage analysis
- tool efficiency scoring

---

# Stress Testing

Validated under:
- 50% tool failure conditions
- concurrent research execution
- API outage simulation
- large context windows

---

# Future Improvements

- multi-agent collaboration
- distributed memory
- reinforcement learning
- streaming execution
- cloud deployment
- real-time financial monitoring