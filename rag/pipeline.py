from vectorstore.pinecone_store import search_chunks
from rag.prompts import fallback_prompt, qa_prompt, router_prompt, llm_prompt
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    api_key= os.getenv("GEMINI_API_KEY"),
    model="gemini-2.5-flash-lite",
    temperature= 0

)

def retrieve_documents(question):
    chunks = search_chunks(question)
    if not chunks:
        return []
    return chunks[:3]
 
def format_context(chunks):
    related_context = ""
    for index,chunk in enumerate(chunks, start=1):
        text = chunk.get("metadata", {}).get("text", "").strip()
        if text:
            related_context += f"\n\n--- Document {index} ---\n{text}"
    return related_context.strip()

def run_rag_query(question, history_text):
    chunks = retrieve_documents(question)
    if not chunks:
        fallback_chain = (fallback_prompt() | llm)
        result = fallback_chain.invoke({
            "question" : question
        })
        return result.content
    formatted_chunks = format_context(chunks)
    if not formatted_chunks.strip():
        fallback_chain = (fallback_prompt() | llm)
        result = fallback_chain.invoke({
            "question": question
        })
        return result.content
    chain = (qa_prompt() | llm)
    result = chain.invoke({
        "chat_history" : history_text,
        "related_context" : formatted_chunks,
        "question" : question
    })
    return result.content
    
def run_agent_query(question, history_text):
    chain = (router_prompt() | llm)
    result = chain.invoke({
        "chat_history" : history_text,
        "question" : question
    })
    return result.content

def run_llm_query(question, history_text):
    chain = (llm_prompt() | llm)
    result = chain.invoke({
        "chat_history" : history_text,
        "question" : question
    })
    return result.content

def run_agent(question, chat_history):
    chat_history = chat_history[-3:]
    history_text = ""
    for chat in chat_history:
        if chat["role"] == "user":
            history_text += f"User : {chat['content']}\n"
        else :
            history_text += f"AI : {chat['content']}"
    decision = run_agent_query(question, history_text)
    cleaned_decision = decision.strip().upper()
    print(f"Question: {question}")
    print(f"Decision: {cleaned_decision}")
    if cleaned_decision == "POLICY":
        result = run_rag_query(question, history_text)
    else :
        result = run_llm_query(question, history_text)
    return result