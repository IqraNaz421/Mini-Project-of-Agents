# 🤖 Agentic AI SDK Projects

Welcome to a series of AI Agent projects built using the **Agentic AI SDK**. This repository demonstrates the power of LLMs, multi-agent systems, model routing, and more — all integrated in a clean and modular way using the blazing-fast Python tool `uv`.

---

## 👩‍💻 GitHub: [IqraNaz421](https://github.com/IqraNaz421)

---

## 📂 Project List

### 🔹 `00_swarm`
A **multi-agent swarm system** where agents work together to perform tasks, demonstrating inter-agent communication and collaboration.

### 🔹 `01_uv`
Basic setup using [`uv`](https://github.com/astral-sh/uv) — a lightning-fast Python package and environment manager. Includes installation and dependency management via `requirements.txt`.

### 🔹 `02_openrouter`
Integration with **[OpenRouter](https://openrouter.ai)** to access multiple LLM providers like GPT-4, Claude, and more. Easily switch between models.

### 🔹 `03_litellm_openai_agent`
Smart **LLM routing** using [LiteLLM](https://github.com/BerriAI/litellm). Routes prompts to OpenAI models efficiently and provides fallback mechanisms and logging.

### 🔹 `04_hello_agent`
A beginner-friendly **"Hello Agent"** setup. This is the most basic single-agent example that introduces you to the Agentic SDK.

### 🔹 `chatbot`
An **Advanced Travel Agency Chatbot** powered by LLMs. It can:
- Recommend destinations
- Suggest hotels & flights
- Plan complete itineraries
- Handle travel FAQs and more!

---

## ⚙️ Tech Stack

| Tool/Library     | Description                              |
|------------------|------------------------------------------|
| 🤖 Agentic SDK   | For building AI agents                   |
| ⚡ `uv`           | Fast Python package manager              |
| 🌐 OpenRouter     | Access to multiple LLM providers         |
| 🚀 LiteLLM        | Model routing and logging for LLMs       |
| 🧠 Swarm Agents   | Multi-agent task solving                 |
| 🗺️ Travel Chatbot | AI assistant for trip planning           |

---

## 🛠 Installation & Setup

### ✅ Requirements

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv) installed

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
📦 Install Dependencies

# Clone the repository
git clone https://github.com/IqraNaz421/agentic-ai-sdk-projects.git
cd agentic-ai-sdk-projects

# Install dependencies using uv
uv pip install -r requirements.txt
▶️ How to Run Each Project
Each folder is a self-contained project. To run one:

cd 00_swarm  # or 01_uv, 02_openrouter, etc.
python main.py
Make sure you add your API keys or .env variables where required for OpenRouter, OpenAI, etc.

📁 Folder Structure
css

📦 agentic-ai-sdk-projects/
├── 00_swarm/
│   └── main.py
├── 01_uv/
│   └── uv_setup.py
├── 02_openrouter/
│   └── openrouter_agent.py
├── 03_litellm_openai_agent/
│   └── router_agent.py
├── 04_hello_agent/
│   └── hello.py
├── chatbot/
│   └── travel_agent.py
├── requirements.txt
└── README.md
⭐ Why uv?
uv is a modern Python package manager that's faster than pip, supports lockfiles, and ensures clean virtual environments. Ideal for projects like this with multiple moving parts.

🧠 Learn More
Agentic SDK GitHub

LiteLLM

OpenRouter

uv by Astral

📜 License
This project is open-source and available under the MIT License.

🙌 Author
Built with ❤️ by Iqra Naz
🔗 github.com/IqraNaz421

