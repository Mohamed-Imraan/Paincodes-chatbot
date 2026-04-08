from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import time

st.set_page_config(page_title="Pain Codes AI Assistant", page_icon="🤖", layout="wide")

# ----------- Custom CSS -----------
st.markdown("""
<style>

/* Full page background */
html, body, [data-testid="stAppViewContainer"] {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color: white;
}

/* Remove white container */
[data-testid="stHeader"]{
background: transparent;
}

[data-testid="stToolbar"]{
right: 2rem;
}

/* Chat bubbles */
[data-testid="stChatMessage"]{
background: rgba(255,255,255,0.08);
border-radius:15px;
padding:10px;
backdrop-filter: blur(10px);
}

/* Sidebar dark */
[data-testid="stSidebar"]{
background: #111827;
color:white;
}

/* Input box */
[data-testid="stChatInput"]{
background:#1f2937;
border-radius:10px;
}

/* Title styling */
.title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#00ffff;
}

/* Subtitle */
.subtitle{
text-align:center;
color:#d1d5db;
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)


# ----------- Title -----------
st.markdown('<p class="title">🤖 Pain Codes AI Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Smart Coding & AI Companion</p>', unsafe_allow_html=True)

# ----------- Sidebar -----------
with st.sidebar:

    st.header("⚙️ Control Panel")

    st.info("AI Model: Llama2")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
        {"role":"assistant","content":"👋 Hello! I am **Pain Codes AI Assistant**.\n\nHow can I assist you today?"}
        ]

    st.markdown("---")

    st.markdown("### 🚀 About")
    st.write("Pain Codes AI is a smart assistant for coding, AI learning and tech guidance.")

# ----------- Default message -----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"assistant","content":"👋 Hello! I am **Pain Codes AI Assistant**.\n\nHow can I assist you today?"}
    ]

# ----------- Display messages -----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------- Input -----------
user_input = st.chat_input("Ask about coding, AI, projects...")

prompt = ChatPromptTemplate.from_messages(
[
("system","You are a helpful AI assistant named Pain Codes Assistant."),
("user","{query}")
]
)

llm = Ollama(model="llama2")
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

# ----------- Chat logic -----------
if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ *Thinking...*")

        response = chain.invoke({"query":user_input})

        time.sleep(1)

        message_placeholder.markdown(response)

    st.session_state.messages.append({"role":"assistant","content":response})