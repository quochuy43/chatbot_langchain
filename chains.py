from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Prompt Template
def create_prompt_template():
    template = """
    Bạn là trợ lý hỗ trợ khách hàng cho một nền tảng thương mại điện tử. 
    Sử dụng thông tin sau để trả lời truy vấn của người dùng một cách ngắn gọn và chính xác:
    Ngữ cảnh: {context}
    Truy vấn người dùng: {query}
    Phản hồi:
    """
    return PromptTemplate(input_variables=["context", "query"], template=template)

# Build chain
def create_qa_chain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", api_key=GOOGLE_API_KEY)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        input_key="query", 
        return_source_documents=True
    )
    return qa_chain

# Test chain
def test_qa_chain(qa_chain):
    sample_queries = [
        "Chi phí vận chuyển được tính như thế nào?",
        "Giá điện thoại Samsung Galaxy S24 Ultra là bao nhiêu?"
    ]
    
    for query in sample_queries:
        print(f"\nQuery: {query}")
        try:
            result = qa_chain.invoke({"query": query})
            print(f"Reponses: {result['result']}")
            print("Original document:", [doc.page_content[:100] for doc in result['source_documents']])
        except Exception as e:
            print(f"Failed: {str(e)}")

if __name__ == "__main__":
    qa_chain = create_qa_chain()
    print("Created chain RetrievalQA.")
    test_qa_chain(qa_chain)