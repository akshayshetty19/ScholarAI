
import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


# Session state
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []


def process_document(path):

    # Load PDFs
    loader = PyPDFDirectoryLoader(path)
    docs = loader.load()

    if not docs:
        raise ValueError("No readable PDF documents found.")

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    # Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    # Vector database
    vector_db = InMemoryVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # Groq LLM
    llm = ChatGroq(model="openai/gpt-oss-20b")

    # Retrieval tool
    @tool
    def retrieve_context(query: str) -> str:
        """Retrieve relevant PDF passages with source filenames and page numbers."""
        retrieved_docs = vector_db.similarity_search(query, k=3)

        context_parts = []

        for doc in retrieved_docs:
            source = os.path.basename(doc.metadata.get("source", "Unknown"))
            page = doc.metadata.get("page", "Unknown")

            # PyPDFLoader page numbers are normally zero-indexed
            if isinstance(page, int):
                page = page + 1

            context_parts.append(
                f"Source: {source}, Page: {page}\n"
                f"{doc.page_content}"
            )

        return "\n\n---\n\n".join(context_parts)

    system_prompt = """
    You are ScholarAI, an AI study and research assistant.

    Answer questions about uploaded PDFs using the retrieve_context tool.
    Use the tool whenever a question requires information from the documents.
    Base document-related answers on the retrieved passages.
    Do not invent facts or citations.
    Cite sources using the filename and page number provided by the tool.
    If the documents do not contain the answer, say so clearly.
    """

    # Conversation memory
    memory = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt=system_prompt,
        checkpointer=memory
    )

    st.session_state.agent = agent
    st.session_state.vector_store = vector_db
    st.session_state.document_uploaded = True


st.title("ScholarAI - AI Study Assistant")


# PDF upload UI
if not st.session_state.document_uploaded:

    uploaded = st.file_uploader(
        "Select PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded and st.button("Process PDFs"):

        with st.spinner("Processing your PDFs..."):

            path = "./doc_files"
            os.makedirs(path, exist_ok=True)

            for file in uploaded:
                file_path = os.path.join(path, file.name)

                with open(file_path, "wb") as f:
                    f.write(file.getvalue())

            try:
                process_document(path)
                st.success("PDFs processed successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error processing PDFs: {e}")


# Chat UI
if st.session_state.document_uploaded and st.session_state.agent:

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    query = st.chat_input("Ask a question about your PDFs...")

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        st.chat_message("user").markdown(query)

        config = {
            "configurable": {
                "thread_id": "scholarai-chat"
            }
        }

        try:
            with st.spinner("Thinking..."):

                response = st.session_state.agent.invoke(
                    {
                        "messages": [
                            {"role": "user", "content": query}
                        ]
                    },
                    config=config
                )

                answer = response["messages"][-1].content

            st.chat_message("assistant").markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Error generating answer: {e}")
