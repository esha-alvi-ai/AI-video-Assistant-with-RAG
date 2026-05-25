from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from utils.config import mistral_api_key as MISTRAL_API_KEY


def get_mistral_llm():
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY is missing. Add it to your .env file.")

    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=MISTRAL_API_KEY,
        temperature=0.2,
    )


def summarize_meeting(transcript: str) -> dict:
    llm = get_mistral_llm()

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI meeting assistant.

Analyze the meeting transcript and return:

1. Meeting Summary
2. Key Decisions
3. Action Items
4. Important Discussion Points

Transcript:
{transcript}
"""
    )

    chain = prompt | llm

    response = chain.invoke({"transcript": transcript})

    return {
        "summary_text": response.content
    }


def answer_question_from_context(question: str, context: str) -> str:
    llm = get_mistral_llm()

    prompt = ChatPromptTemplate.from_template(
        """
Answer the user's question using only the meeting transcript context.

If the answer is not available in the context, say:
"I could not find that in the transcript."

Context:
{context}

Question:
{question}
"""
    )

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})

    return response.content