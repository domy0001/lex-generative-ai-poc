import os
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

api_key=os.environ['OPENAI_API_KEY']
s3_vector_db_arn = os.environ['VECTOR_DB_ARN']
embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)

def handler():
    documents = []
    documents_path = '../../files/documents'
    try:
        for file in os.listdir('../../files/documents'):
            if file.endswith('.pdf'):
                pdf_path = f'{documents_path}/' + file
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            elif file.endswith('.docx') or file.endswith('.doc'):
                doc_path = f'{documents_path}/' + file
                loader = Docx2txtLoader(doc_path)
                documents.extend(loader.load())
            elif file.endswith('.txt'):
                text_path = f'{documents_path}/' + file
                loader = TextLoader(text_path)
                documents.extend(loader.load())
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        chunked_documents = text_splitter.split_documents(documents)
        print(f'Text splitted: {chunked_documents}')

        vectordb = Chroma.from_documents(documents, embedding=embeddings_model, persist_directory="./data")
        vectordb.persist()
        print(f'Vector db: {vectordb}')

    except Exception as ex:
        print(ex)


