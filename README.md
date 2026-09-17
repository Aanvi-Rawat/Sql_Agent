# 🤖 AI Task Manager — SQL Agent

An AI-powered task management application that allows users to manage tasks using **natural language**.

Instead of manually writing SQL queries, users can simply ask the AI to create, view, update, or delete tasks.

> 💬 "Create a task to complete my DSA assignment"

> 💬 "Show me my pending tasks"

> 💬 "Mark task 3 as completed"

The application uses a **LangGraph agent powered by Groq** to understand user requests, select the appropriate tool, and interact with a **SQLite database**.

---

## ✨ Features

- 💬 Natural language task management
- ➕ Create tasks using conversational commands
- 📋 View and filter tasks
- 🔄 Update task status
- 🗑️ Delete tasks
- 🤖 LLM-powered tool calling
- 🧠 LangGraph agent orchestration
- 💾 Persistent SQLite database
- ⚡ Fast LLM inference using Groq
- 🎨 Interactive Streamlit interface
- 🔐 Environment-based API key management

---

## 🛠️ Tech Stack

<p align="center">

<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</a>

<a href="https://www.langchain.com/">
<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge"/>
</a>

<a href="https://www.langchain.com/langgraph">
<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge"/>
</a>

<a href="https://groq.com/">
<img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge"/>
</a>

<a href="https://www.sqlite.org/">
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
</a>

<a href="https://streamlit.io/">
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
</a>


</p>

| Technology | Purpose |
|------------|---------|
| 🐍 **Python** | Core programming language |
| 🦜 **LangChain** | LLM and tool integration |
| 🧠 **LangGraph** | Agent orchestration and state management |
| ⚡ **Groq** | Fast LLM inference |
| 🗄️ **SQLite** | Persistent task database |
| 🎨 **Streamlit** | Interactive web interface |
| 🔐 **python-dotenv** | Environment variable management |


---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         │  Natural Language   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    STREAMLIT UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LANGGRAPH AGENT   │
                         │                     │
                         │      GROQ LLM       │
                         │   Tool Selection    │
                         └──────────┬──────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌────────────┐     ┌────────────┐     ┌────────────┐
          │create_task │     │ get_tasks  │     │update_task │
          └──────┬─────┘     └──────┬─────┘     └──────┬─────┘
                 │                  │                  │
                 └──────────────────┼──────────────────┘
                                    │
                              ┌─────▼──────┐
                              │delete_task │
                              └─────┬──────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   SQLITE DATABASE   │
                         │     tasks table     │
                         └─────────────────────┘


