from langchain_google_genai import ChatGoogleGenerativeAI
from decouple import config

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config("GOOGLE_API_KEY"))
result = llm.invoke("Write a ballad about LangChain")
print(result.content)