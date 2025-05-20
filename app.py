import streamlit as st
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

# RetrievalQA
@st.cache_resource
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

# Streamlit
st.title("Chatbot hỗ trợ khách hàng về thương mại điện tử")
st.write("Hỏi về sản phẩm, vận chuyển, đổi trả, hoặc các vấn đề khác!")

query = st.text_input("Nhập câu hỏi của bạn:", placeholder="Ví dụ: Chi phí vận chuyển là bao nhiêu?")

if query:
    try:
        qa_chain = create_qa_chain()
        result = qa_chain.invoke({"query": query})
        st.write("**Phản hồi:**", result["result"])
        # st.write("**Tài liệu nguồn:**")
        # for i, doc in enumerate(result["source_documents"], 1):
        #     st.write(f"{i}. {doc.page_content[:200]}...")
    except Exception as e:
        st.error(f"Failed: {str(e)}")