import json
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def json_file_to_pdf(json_file, output_file):
    # Load JSON data from file with explicit encoding
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    flowables = []

    # Check if the JSON data is a list
    if isinstance(data, list):
        # Convert each list item to text and add to the PDF
        for item in data:
            text = json.dumps(item, indent=4)
            paragraph = Paragraph(text, styles['Normal'])
            flowables.append(paragraph)
    else:
        # Convert JSON data to text and add to the PDF
        text = json.dumps(data, indent=4)
        paragraph = Paragraph(text, styles['Normal'])
        flowables.append(paragraph)

    doc.build(flowables)

json_file ="E:/BKDN/TTNT/Chatpdf/documents/output4.json"
output_file = "E:/BKDN/TTNT/Chatpdf/documents/data.pdf"
# Convert JSON data to PDF
json_file_to_pdf(json_file,output_file)


JSON_PATH = "../documents/data.pdf"

# create loader
loader = PyPDFLoader(JSON_PATH)
# split document
pages = loader.load_and_split()
# Embedding function
embedding_func = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Create vector store
vectordb = Chroma.from_documents(
    documents=pages,
    embedding=embedding_func,
    persist_directory="../vector_db1",  # Adjust the directory path as needed
    collection_name="book_to_scrape"
)

# Make vector store persistent
vectordb.persist()
