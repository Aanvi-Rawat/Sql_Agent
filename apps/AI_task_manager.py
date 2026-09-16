# ============================================================
# AI TASK MANAGER
# LangChain + LangGraph + Groq + SQLite + Streamlit
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import sqlite3
import streamlit as st

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TaskManager AI",
    page_icon="📋",
    layout="centered"
)


# ============================================================
# DATABASE
# ============================================================

DB_PATH = "my_tasks.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# Create table
conn = get_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(
        status IN ('pending', 'in_progress', 'completed')
    ) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()


# ============================================================
# SQL TOOLS
# ============================================================

@tool
def create_task(title: str, description: str = "") -> str:
    """
    Create a new task.

    Use this when the user wants to add or create a task.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO tasks (title, description)
        VALUES (?, ?)
        """,
        (title, description)
    )

    task_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return f"Task created successfully with ID {task_id}."


@tool
def get_tasks(status: str = "") -> str:
    """
    Retrieve tasks from the database.

    status can be:
    - pending
    - in_progress
    - completed

    Leave status empty to retrieve all tasks.
    """

    conn = get_connection()

    if status:
        cursor = conn.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks
            WHERE status = ?
            ORDER BY created_at DESC
            LIMIT 10
            """,
            (status,)
        )
    else:
        cursor = conn.execute(
            """
            SELECT id, title, description, status, created_at
            FROM tasks
            ORDER BY created_at DESC
            LIMIT 10
            """
        )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "No tasks found."

    result = []

    for row in rows:
        result.append(
            f"ID: {row[0]} | "
            f"Title: {row[1]} | "
            f"Description: {row[2]} | "
            f"Status: {row[3]} | "
            f"Created: {row[4]}"
        )

    return "\n".join(result)


@tool
def update_task(
    task_id: int,
    status: str
) -> str:
    """
    Update the status of an existing task.

    Allowed statuses:
    - pending
    - in_progress
    - completed
    """

    if status not in [
        "pending",
        "in_progress",
        "completed"
    ]:
        return (
            "Invalid status. Use pending, "
            "in_progress, or completed."
        )

    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE id = ?
        """,
        (status, task_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return f"No task found with ID {task_id}."

    conn.close()

    return f"Task {task_id} updated to {status}."


@tool
def delete_task(task_id: int) -> str:
    """
    Delete a task using its ID.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return f"No task found with ID {task_id}."

    conn.close()

    return f"Task {task_id} deleted successfully."


# ============================================================
# MODEL
# ============================================================

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    reasoning_effort="low"
)


# ============================================================
# TOOLS
# ============================================================

tools = [
    create_task,
    get_tasks,
    update_task,
    delete_task
]


# ============================================================
# SYSTEM PROMPT
# ============================================================

system_prompt = """
You are TaskManager AI, an assistant that manages a user's tasks.

You have access to four tools:

1. create_task
   - Creates a new task.

2. get_tasks
   - Retrieves tasks.
   - Can filter by status.

3. update_task
   - Updates a task's status.

4. delete_task
   - Deletes a task.

TASK STATUS VALUES:

- pending
- in_progress
- completed


RULES:

1. Use the appropriate tool whenever the user asks you to
   create, view, update, or delete a task.

2. Never invent task IDs or task information.

3. When the user asks to see tasks, use get_tasks.

4. When the user asks for pending tasks, use:
   get_tasks(status="pending")

5. When the user asks for completed tasks, use:
   get_tasks(status="completed")

6. When creating a task, use create_task.

7. When updating a task, use update_task.

8. When deleting a task, use delete_task.

9. After a successful create, update, or delete operation,
   provide a concise confirmation.

10. Do not repeatedly call the same tool with the same arguments.

11. If a tool returns that a task does not exist, tell the user
    that the task could not be found.

12. Keep responses concise and friendly.

13. When presenting multiple tasks, format them as a markdown table
    with these columns:

    ID | Title | Description | Status | Created

14. For normal conversation that does not involve task management,
    answer normally without using a database tool.
"""


# ============================================================
# AGENT
# ============================================================

@st.cache_resource
def get_agent():

    memory = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=memory,
        system_prompt=system_prompt
    )

    return agent


agent = get_agent()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

.prompt-box {
    padding: 12px 15px;
    border-radius: 10px;
    border: 1px solid rgba(128,128,128,0.25);
    margin: 7px 0;
    font-size: 0.9rem;
}

.sidebar-title {
    font-size: 1.35rem;
    font-weight: 700;
}

.sidebar-section {
    margin-top: 22px;
    margin-bottom: 8px;
    font-size: 0.75rem;
    color: #888;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📋 TaskManager AI</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Manage your tasks using natural language."
    )

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-section">WHAT YOU CAN ASK</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    📝 **Create**

    `Add a task to study DSA`

    📋 **View**

    `Show my pending tasks`

    🔄 **Update**

    `Mark task 2 as completed`

    🗑️ **Delete**

    `Delete task 3`
    """)

    st.divider()

    st.caption(
        "LangChain • LangGraph • Groq • SQLite"
    )


# ============================================================
# WELCOME / EXAMPLES
# ============================================================

if not st.session_state.messages:

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="prompt-box">
            📝 Add a task to study DSA
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="prompt-box">
            📋 Show my pending tasks
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="prompt-box">
            ✅ Mark task 1 as completed
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="prompt-box">
            🔎 Show all my tasks
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar=(
            "👤"
            if message["role"] == "user"
            else "🤖"
        )
    ):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

query = st.chat_input(
    "Ask me to manage your tasks..."
)


# ============================================================
# PROCESS QUERY
# ============================================================

if query:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(query)


    # AI message
    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Thinking..."):

            try:

                response = agent.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": query
                            }
                        ]
                    },
                    {
                        "configurable": {
                            "thread_id": "1"
                        },
                        "recursion_limit": 10
                    }
                )

                result = response["messages"][-1].content

                st.markdown(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result
                })


            except Exception as e:

                st.error(
                    "Something went wrong while processing your request."
                )

                st.code(str(e))