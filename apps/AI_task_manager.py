from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase 
from langchain_community.agent_toolkits import SQLDatabaseToolkit 
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///my_tasks.db")

db.run("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK(status IN ('pending', 'in_progress', 'completed'))
        DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

model = ChatGroq(model = "openai/gpt-oss-120b")
toolkit = SQLDatabaseToolkit(db = db, llm = model)
tools = toolkit.get_tools()
system_prompt = """
You are a task management assistant that interacts with a SQL database containing a 'tasks' table. 

TASK RULES:
1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC
2. After CREATE/UPDATE/DELETE, confirm with SELECT query
3. If the user requests a list of tasks, present the output in a structured table format to ensure a clean and organized display in the browser."

CRUD OPERATIONS:
    CREATE: INSERT INTO tasks(title, description, status)
    READ: SELECT * FROM tasks WHERE ... LIMIT 10
    UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
    DELETE: DELETE FROM tasks WHERE id=? OR title=?

Table schema: id, title, description, status(pending/in_progress/completed), created_at.
"""

#we made it into a function because streamlit refreshes page after every execution.. it will re run the whole file from line 1, but if it refreshes then the memory outside the function will get refreshed too, which is not good for memory saving also, we dont need to define agent again and again so we used a decorator cachea-resouce that this function will not be refreshed 
@st.cache_resource
def get_agent():
    agent = create_agent(
        model = model,
        tools = tools,
        checkpointer = InMemorySaver(),
        system_prompt = system_prompt
    )
    return agent

agent = get_agent()



            
# ─────────────────────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────────────────────

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="TaskManager AI",
    page_icon="📋",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 900px;
    }

   

    /* Welcome box */
    .welcome-box {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,0.25);
        margin: 20px 0;
        text-align: center;
    }

    .welcome-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .welcome-text {
        color: #888;
        font-size: 0.95rem;
    }

    /* Example prompts */
    .prompt-box {
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid rgba(128,128,128,0.2);
        margin: 5px 0;
        font-size: 0.9rem;
    }

    /* Sidebar */
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .sidebar-section {
        margin-top: 25px;
        font-size: 0.85rem;
        color: #888;
    }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📋 TaskManager AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "Manage your tasks using natural language."
    )

    st.divider()

    # New chat button
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
    **Create**
    
    > Add a task to study DSA

    **View**
    
    > Show my pending tasks

    **Update**
    
    > Mark task 2 as completed

    **Delete**
    
    > Delete my completed tasks
    """)

    st.divider()

    st.caption("Powered by LangChain + LangGraph + Groq + SQLite")




# ─────────────────────────────────────────────────────────────
# WELCOME SCREEN
# ─────────────────────────────────────────────────────────────

if not st.session_state.messages:


    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="prompt-box">
        📝 Add a task to study DSA
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="prompt-box">
        📋 Show my pending tasks
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="prompt-box">
        ✅ Mark task 1 as completed
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="prompt-box">
        🔎 Show all my tasks
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DISPLAY PREVIOUS CHAT
# ─────────────────────────────────────────────────────────────

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
        avatar="🧑" if message["role"] == "user" else "🤖"
    ):
        st.markdown(message["content"])


# ─────────────────────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────────────────────

query = st.chat_input(
    "Ask me to manage your tasks..."
)


# ─────────────────────────────────────────────────────────────
# PROCESS QUERY
# ─────────────────────────────────────────────────────────────

if query:

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Display user message
    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.markdown(query)

    # Generate AI response
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
                        }
                    }
                )

                result = response["messages"][-1].content

                st.markdown(result)

                # Store AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result
                })

            except Exception as e:

                st.error(
                    "Something went wrong while processing your request."
                )

                st.caption(str(e))          
