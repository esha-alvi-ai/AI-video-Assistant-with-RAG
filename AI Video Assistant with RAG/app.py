import os
import streamlit as st

from utils.audio_processor import save_uploaded_file
from utils.config import UPLOAD_DIR
from utils.meeting_pipeline import process_meeting_input
from utils.summarizer import summarize_meeting
from utils.rag_pipeline import build_vectorstore, ask_transcript_question
from utils.exporter import export_txt, export_pdf


st.set_page_config(
    page_title="AI Video Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
)

st.title("🎙️ AI Video Meeting Assistant with RAG")

st.write(
    "Upload English, Hindi, or Urdu meeting audio/video/subtitles, "
    "or paste a YouTube URL. The app converts everything to English, "
    "summarizes the meeting, extracts decisions/action items, and lets you chat with the transcript."
)

input_mode = st.selectbox(
    "Input type",
    [
        "youtube",
        "uploaded_video",
        "uploaded_audio",
        "uploaded_subtitle",
    ],
)

source_language = st.selectbox(
    "Source language",
    [
        "english",
        "hindi",
        "urdu",
    ],
)

model_size = st.selectbox(
    "Whisper model size",
    [
        "base",
        "small",
        "medium",
    ],
    index=0,
)

source = None

if input_mode == "youtube":
    source = st.text_input("Enter YouTube URL")

elif input_mode == "uploaded_video":
    uploaded_file = st.file_uploader(
        "Upload video",
        type=["mp4", "mkv", "mov", "avi", "webm"],
    )

    if uploaded_file:
        source = save_uploaded_file(uploaded_file, UPLOAD_DIR)
        st.success(f"Uploaded: {source}")

elif input_mode == "uploaded_audio":
    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["mp3", "wav", "m4a", "aac", "ogg", "flac"],
    )

    if uploaded_file:
        source = save_uploaded_file(uploaded_file, UPLOAD_DIR)
        st.success(f"Uploaded: {source}")

elif input_mode == "uploaded_subtitle":
    uploaded_file = st.file_uploader(
        "Upload subtitle file",
        type=["srt"],
    )

    if uploaded_file:
        source = save_uploaded_file(uploaded_file, UPLOAD_DIR)
        st.success(f"Uploaded: {source}")


if "english_text" not in st.session_state:
    st.session_state.english_text = ""

if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""


if st.button("Process Meeting"):
    if not source:
        st.error("Please provide a valid input first.")
    else:
        with st.spinner("Processing meeting..."):
            result = process_meeting_input(
                source=source,
                source_language=source_language,
                input_mode=input_mode,
                model_size=model_size,
            )

            st.session_state.english_text = result["english_text"]

            summary_result = summarize_meeting(st.session_state.english_text)
            st.session_state.summary_text = summary_result["summary_text"]

            build_vectorstore(st.session_state.english_text)

        st.success("Meeting processed successfully.")


if st.session_state.english_text:
    st.subheader("English Transcript")
    st.text_area(
        "Transcript",
        st.session_state.english_text,
        height=300,
    )

if st.session_state.summary_text:
    st.subheader("Meeting Summary / Decisions / Action Items")
    st.markdown(st.session_state.summary_text)


if st.session_state.english_text:
    st.subheader("Chat with Meeting Transcript")

    question = st.text_input("Ask a question about the meeting")

    if st.button("Ask"):
        if question.strip():
            with st.spinner("Searching transcript..."):
                answer = ask_transcript_question(question)
            st.write(answer)


if st.session_state.english_text or st.session_state.summary_text:
    st.subheader("Export Results")

    export_content = f"""
MEETING SUMMARY

{st.session_state.summary_text}


ENGLISH TRANSCRIPT

{st.session_state.english_text}
"""

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Export TXT"):
            path = export_txt(export_content)
            st.success(f"TXT exported: {path}")

    with col2:
        if st.button("Export PDF"):
            path = export_pdf(export_content)
            st.success(f"PDF exported: {path}")