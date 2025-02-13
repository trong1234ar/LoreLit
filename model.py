from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv(".env")
# langchain_api_key = os.getenv("langchain_api")
# gemini_api_key = os.getenv("gemini_api")
langchain_api_key = st.secrets["langchain_api"]
gemini_api_key = st.secrets["gemini_api"]

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=gemini_api_key
)

