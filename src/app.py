import os
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_core.messages import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found. Please set it in a .env file.")
    st.stop()

# Load dataset
@st.cache_data
def load_dataset():
    with open("src/website_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    docs = [{"page": e["page"], "content": e["text"], "url": e["url"]} for e in data]
    return docs


# Vectorstore
@st.cache_resource
def get_vectorstore_from_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = []
    for d in docs:
        split_docs.extend(text_splitter.split_text(d["content"]))
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(split_docs, embeddings)
    return vector_store


# Conversational chain using OpenAI
@st.cache_resource
def get_conversational_chain(_vector_store):
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0.5     
    )
    retriever = _vector_store.as_retriever()

    # Custom prompt
    template = """
    You are a helpful assistant for AT Digital’s website.
    Use the provided context to answer the question. 
    If the context does not contain enough information, 
    still give the best possible answer using your own knowledge. 
    Never say "I don't know". Always try to help.

    Context:
    {context}

    Chat History:
    {chat_history}

    Question: {question}

    Answer:
    """
    custom_prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"],
        template=template
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    return qa_chain

# Streamlit UI
st.set_page_config(page_title="Ask AT Digital", page_icon="🤖")
st.title("Ask AT Digital Chatbot (OpenAI Version)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load data and vectorstore once
if "qa_chain" not in st.session_state:
    st.info("Loading website data and embeddings... This may take a minute.")
    docs = load_dataset()
    vector_store = get_vectorstore_from_docs(docs)
    st.session_state.qa_chain = get_conversational_chain(vector_store)
    st.success("Ready to chat!")

# Sidebar
with st.sidebar:
    st.header("About")
    st.write("This chatbot answers questions using AT Digital’s website dataset. Powered by OpenAI GPT.")


# User input
user_query = st.chat_input("Type your question here...")

if user_query and "qa_chain" in st.session_state:
    # Append human message
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    # Format chat_history for ConversationalRetrievalChain
    formatted_history = []
    for i in range(0, len(st.session_state.chat_history), 2):
        human_msg = st.session_state.chat_history[i].content
        ai_msg = st.session_state.chat_history[i + 1].content if i + 1 < len(st.session_state.chat_history) else ""
        formatted_history.append((human_msg, ai_msg))

    # Get AI response
    result = st.session_state.qa_chain({
        "question": user_query,
        "chat_history": formatted_history
    })
    answer = result.get("answer", "Sorry, I could not find an answer.")
    st.session_state.chat_history.append(AIMessage(content=answer))

# Display chat messages
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
