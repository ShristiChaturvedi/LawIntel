from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(chunks):

    vector_db = FAISS.from_documents(
        chunks,
        embedding_model
    )

    vector_db.save_local("vectorstore")

    print("Vector database created successfully!")
