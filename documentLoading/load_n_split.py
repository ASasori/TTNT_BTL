from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
PDF_PATH = "E:/BKDN/TTNT/Chatpdf/documents/Rich-Dad-Poor-Dad.pdf"

# create loader
loader = PyPDFLoader(PDF_PATH)
# split document
pages = loader.load_and_split()

# embedding function
embedding_func = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# create vector store
vectordb = Chroma.from_documents(
    documents=pages,
    embedding=embedding_func,
    persist_directory=f"../Chatpdf/vector_db2",
    collection_name="rich_dad_poor_dad")

# make vector store persistant
vectordb.persist()