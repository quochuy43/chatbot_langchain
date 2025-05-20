from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# download and split documents
def load_and_split_documents():
    loader = DirectoryLoader("./knowledge_base", glob="*.md", loader_cls=lambda path: TextLoader(path, encoding='utf-8'))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50
    )
    split_docs = text_splitter.split_documents(documents)
    return split_docs

# vector store
def create_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # create vector FAISS from ducuments
    vector_store = FAISS.from_documents(documents, embeddings)
    return vector_store

# test retrieval
def test_retrival(vector_store):
    sample_queries = [
        "Chi phí vận chuyển được tính như thế nào?",
        "Giá điện thoại Samsung Galaxy S24 Ultra là bao nhiêu?"
    ]

    # retrieval with each query
    for query in sample_queries:
        print(f"Query: {query}")
        docs = vector_store.similarity_search(query, k=3)
        for i, doc in enumerate(docs, 1):
            print(f"Result {i}: {doc.page_content[:200]}... ")

if __name__ == "__main__":
    split_docs = load_and_split_documents()
    print("Downloaded documents")

    vector_store = create_vector_store(split_docs)
    print("Created vector store FAISS")

    test_retrival(vector_store)

    # save vector store
    vector_store.save_local("faiss_index")
