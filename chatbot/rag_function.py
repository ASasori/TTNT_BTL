from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from decouple import config
from langchain.chains import RetrievalQA
from langchain.schema.output_parser import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings

    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)
    # context = "\n\n".join(str(p.page_content) for p in pages)
    # texts = text_splitter.split_text(context)

prompt = ChatPromptTemplate.from_template(
    "tell me about {topic}"
)
output_parser = StrOutputParser()


embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="../vector_db",
    collection_name="rich_dad_poor_dad",
    embedding_function=embedding_function,
)


# create prompt
QA_prompt = PromptTemplate(
    template="""Use the following pieces of context to answer the user question.
chat_history: {chat_history}
Context: {text}
Question: {question}
Answer:""",
    input_variables=["text", "question", "chat_history"]
)

# create chat model
#llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=config("GOOGLE_API_KEY"))
# create memory
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history")

# create retriever chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={'fetch_k': 4, 'k': 3},
        search_type='mmr'
    ),
    chain_type="refine"
)
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     memory =memory,
#     retriever=vector_db.as_retriever(),
#     return_source_documents = True,
#     chain_type="refine"
# )
# question
question = "What is the book about?"
chain = prompt | llm | output_parser

import chromadb

client = chromadb.PersistentClient("../vector_db1")
collection = client.get_collection("book_to_scrape")
print("Config ok")

# result = collection.query(query_texts="What does dad say about how to make money?",
#                           n_results = 3)
# print(dict.keys(result))
def rag2(question: str) -> str:
    result_string = chain.invoke({"topic": question})
    return result_string
    # if isinstance(result, list):
    #     result_string = ""
    #     for idx, doc in enumerate(result):
    #         result_string += f"Result {idx + 1}:\n"
    #         result_string += f"Title: {doc.metadata.get('title', 'N/A')}\n"
    #         result_string += f"Price: {doc.metadata.get('price', 'N/A')}\n"
    #         result_string += f"Availability: {doc.metadata.get('availability', 'N/A')}\n"
    #         result_string += f"Description: {doc.page_content}\n\n"
    #     return result_string
    # else:
    #     return "No results found."

def rag(question: str) -> str:
    # call QA chain
    print("test in rag")
    print(question)
    response = qa_chain({"question": question})

    return response.get("answer")
