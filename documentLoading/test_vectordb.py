# from langchain_community.vectorstores import Chroma
import chromadb

client = chromadb.PersistentClient("../vector_db1")
collection = client.get_collection("book_to_scrape")
print("Config ok")

result = collection.query(query_texts="What does dad say about how to make money?",
                          n_results = 3)
print(dict.keys(result))

document = result['documents'][0]
for d in document:
    print(d)
    print("--------------")