import os

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from utils.config import CHROMA_DIR
from utils.summarizer import answer_question_from_context


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vectorstore(transcript: str, collection_name: str = "meeting_transcript"):
    os.makedirs(CHROMA_DIR, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )

    documents = [Document(page_content=transcript)]
    chunks = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR,
        collection_name=collection_name,
    )

    return vectorstore


def load_vectorstore(collection_name: str = "meeting_transcript"):
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
        collection_name=collection_name,
    )


def ask_transcript_question(
    question: str,
    collection_name: str = "meeting_transcript",
    k: int = 4,
) -> str:
    vectorstore = load_vectorstore(collection_name=collection_name)

    docs = vectorstore.similarity_search(question, k=k)

    context = "\n\n".join(doc.page_content for doc in docs)

    return answer_question_from_context(question, context)