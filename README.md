# 📋 TaskManager AI

An AI-powered task management application that lets users **create, view, update, and delete tasks using natural language**.

Instead of writing SQL queries manually, users can simply ask:

> "Add a task to study DSA"

> "Show my pending tasks"

> "Mark task 2 as completed"

The AI agent understands the request, selects the appropriate SQL tool, interacts with the SQLite database, and returns the result conversationally.

---

## ✨ Features

- 🤖 Natural-language task management
- 📝 Create tasks using conversational commands
- 📋 Retrieve and view tasks
- 🔄 Update task status
- 🗑️ Delete tasks
- 🧠 Agent-based tool calling
- 💾 SQLite database integration
- 💬 Conversational memory with LangGraph
- 🌐 Interactive Streamlit interface
- ⚡ Groq-powered LLM inference

---

## 🛠️ Tech Stack

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">

<img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white">

<img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white">

<img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white">

<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">

<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white">

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">

<img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white">

</p>

---

## 🏗️ Architecture

```text
                   ┌─────────────────────┐
                   │       User          │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │     Streamlit UI    │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │    LangChain Agent  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ SQL Database Tools  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │     SQLite DB       │
                   │                     │
                   │      tasks          │
                   └─────────────────────┘
                              ▲
                              │
                   ┌──────────┴──────────┐
                   │     LangGraph       │
                   │  Conversation State│
                   └─────────────────────┘