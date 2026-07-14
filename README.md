# 🛡️ LLM Evaluation & Red Teaming Framework

An automated **LLM evaluation, red teaming, and safety benchmarking platform** built with **FastAPI** and **Streamlit**.

The framework enables developers and researchers to evaluate multiple Large Language Models (LLMs) against common safety and reliability challenges such as **jailbreaking, prompt injection, hallucination, and bias**. It supports multiple providers through a unified interface, executes evaluation tasks asynchronously, and generates structured reports with an interactive analytics dashboard.

---

# ✨ Features

- 🔄 Multi-provider LLM support (Google AI Studio & OpenRouter)
- ⚡ Asynchronous evaluation engine
- 🧪 Automated red teaming
- 📊 Interactive Streamlit dashboard
- 📁 Dynamic dataset loading
- 📈 CSV and JSON report generation
- 📝 Centralized logging
- ⚙️ Environment-based configuration
- 🚦 Rate-limit aware execution
- 🔌 Easily extensible architecture

---

# 🏗️ Architecture

The project consists of two major components:

- **FastAPI Backend**
  - Handles model communication
  - Runs evaluation pipelines
  - Executes asynchronous requests
  - Generates reports

- **Streamlit Dashboard**
  - Select evaluation datasets
  - Configure models
  - Launch evaluation runs
  - Visualize results

---

# 📂 Project Structure

```text
.
├── app/
│   ├── api/
│   │   └── evaluate.py
│   │
│   ├── datasets/
│   │   ├── bias.json
│   │   ├── hallucination.json
│   │   ├── jailbreak.json
│   │   ├── prompt_injection.json
│   │   └── loader.py
│   │
│   ├── evaluator/
│   │   ├── engine.py
│   │   ├── result.py
│   │   └── runner.py
│   │
│   ├── models/
│   │   ├── base_llm.py
│   │   ├── factory.py
│   │   ├── gemini_provider.py
│   │   └── openai_provider.py
│   │
│   ├── redteam/
│   │   └── metrics.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── report_manager.py
│   │
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── outputs/
│   ├── csv/
│   ├── json/
│   ├── logs/
│   └── reports/
│
├── .env
├── requirements.txt
└── run_dashboard.bat
```

---

# 🚀 How It Works

```text
                User
                  │
                  ▼
        Streamlit Dashboard
                  │
                  ▼
          FastAPI Evaluation API
                  │
                  ▼
        Evaluation Engine
                  │
      ┌───────────┴────────────┐
      ▼                        ▼
 Google AI Studio         OpenRouter
      │                        │
      └───────────┬────────────┘
                  ▼
          Response Collection
                  ▼
        Safety & Quality Metrics
                  ▼
      CSV / JSON / Dashboard Reports
```

---

# ⚙️ Core Components

## 1. API Layer

Responsible for receiving evaluation requests from the dashboard and exposing REST endpoints.

**Location**

```
app/api/
```

Main responsibilities

- Receive evaluation jobs
- Validate requests
- Launch evaluation engine
- Return results

---

## 2. Evaluation Engine

The core orchestration layer.

**Location**

```
app/evaluator/
```

Responsibilities

- Execute prompts asynchronously
- Manage concurrent workers
- Handle retries
- Respect provider rate limits
- Collect responses
- Generate structured results

---

## 3. Model Factory

Provides a unified interface for different LLM providers.

**Location**

```
app/models/
```

Currently supported

- Google AI Studio
- OpenRouter

The factory automatically routes requests based on the selected model.

Example:

```
google/gemini-2.5-pro
          │
          ▼
 Google AI Studio Provider

meta-llama/llama-3
          │
          ▼
OpenRouter Provider
```

---

## 4. Dataset Loader

Automatically discovers evaluation datasets.

Supported datasets include

- Jailbreak
- Prompt Injection
- Hallucination
- Bias

Adding a new dataset only requires placing another JSON file inside:

```
app/datasets/
```

No additional code changes are required.

---

## 5. Red Team Metrics

The scoring engine responsible for evaluating model behavior.

Current metrics include

- Refusal detection
- Prompt injection success
- Jailbreak success
- Hallucination detection
- Bias indicators

Designed to be easily extended with custom metrics.

---

## 6. Report Manager

Automatically exports evaluation artifacts.

Supported formats

- JSON
- CSV

Reports are stored inside

```
outputs/
```

---

# ⚡ Key Capabilities

### Hybrid Model Routing

Automatically routes requests to the appropriate provider.

- Google models → Google AI Studio
- Other supported models → OpenRouter

---

### Asynchronous Execution

Evaluation requests are processed concurrently using asyncio.

Benefits

- Faster execution
- Better throughput
- Lower waiting time

---

### Rate-Limit Awareness

The engine includes

- concurrency control
- cooldown timers
- request scheduling
- retry handling

to remain compatible with free-tier API limits.

---

### Dynamic Dataset Discovery

Datasets are detected automatically at runtime.

Simply add:

```
new_dataset.json
```

inside

```
app/datasets/
```

and it becomes available in the dashboard.

---

### Transparent Failure Handling

Instead of hiding errors, the framework records them.

Examples

- Timeout
- API failure
- Authentication error
- Rate limit exceeded

This prevents artificially inflated evaluation scores.

---

# 📊 Evaluation Categories

The framework currently evaluates models across four primary safety dimensions.

| Category | Purpose |
|-----------|----------|
| Jailbreak | Measures resistance against attempts to bypass safety restrictions |
| Prompt Injection | Evaluates susceptibility to malicious instruction injection |
| Hallucination | Detects fabricated or unsupported responses |
| Bias | Identifies potentially biased or unfair outputs |

---

# 📈 Scoring Strategy

### Jailbreak

A response is considered **safe** if the model refuses harmful instructions.

Example refusal

> "I can't assist with that request."

---

### Prompt Injection

The model should reject malicious attempts to override previous instructions.

---

### Hallucination

The response is evaluated for factual consistency and unsupported claims.

---

### Bias

Responses are analyzed for potentially biased or discriminatory behavior.

---

# 📁 Output Structure

Each evaluation generates structured artifacts.

```
outputs/

├── csv/
│
├── json/
│
├── logs/
│
└── reports/
```

Generated artifacts include

- Raw model responses
- Evaluation scores
- Summary statistics
- Execution logs

---

# 🔧 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/llm-evaluation-framework.git

cd llm-evaluation-framework
```

---

## 2. Create a Virtual Environment

Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

Windows

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example requirements

```text
fastapi
uvicorn
streamlit
httpx
openai
pandas
pydantic
pydantic-settings
python-dotenv
```

---

## 4. Configure Environment Variables

Create a `.env` file.

```env
OPENROUTER_API_KEY=your_openrouter_key

GEMINI_API_KEY=your_google_ai_studio_key

OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

ENVIRONMENT=development

LOG_LEVEL=INFO
```

---

# ▶️ Running the Project

## Terminal 1

Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Health endpoint

```
http://localhost:8000/health
```

---

## Terminal 2

Launch Streamlit

```bash
streamlit run dashboard/app.py
```

---

# 📊 Example Workflow

```
Select Model

↓

Choose Dataset

↓

Configure Evaluation

↓

Run Async Evaluation

↓

Generate Metrics

↓

Export Reports

↓

Analyze Dashboard
```

---

# 🛠️ Future Improvements

Planned enhancements include

- LangSmith integration
- DeepEval integration
- OpenAI Evals compatibility
- Human evaluation workflows
- More red-team datasets
- Additional LLM providers
- Authentication
- Database-backed history
- Interactive charts
- Docker deployment
- Kubernetes support

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to add

- new datasets
- evaluation metrics
- provider integrations
- dashboard improvements

please open an issue before submitting a large pull request.

---

