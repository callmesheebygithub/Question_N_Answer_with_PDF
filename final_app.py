# # final_app.py

# import warnings
# from langchain_community.document_loaders import PDFMinerLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_community.llms import Ollama

# warnings.filterwarnings('ignore')

# class FileReader:
#     def __init__(self, dir_path, query):
#         self.dir_path = dir_path
#         self.query = query

#     def load_documents(self):
#         # Initialize the DirectoryLoader with the directory path
#         loader = DirectoryLoader(self.dir_path, glob="**/*.pdf", loader_cls=PDFMinerLoader)
#         return loader.load()

#     def text_split(self):
#         # Initialize the RecursiveCharacterTextSplitter with chunk size and overlap
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30)

#         documents = self.load_documents()
        
#         # Combine the contents of all documents into a single string
#         combined_text = [doc.page_content for doc in documents]
        
#         # Split the combined text into chunks
#         split_docs = text_splitter.create_documents(combined_text)

#         return split_docs

#     def embedding_model(self):
#         # Initialize the OllamaEmbeddings model
#         embeddings_function = OllamaEmbeddings(model="gemma2:2b")
#         texts = self.text_split()
#         embeddings = embeddings_function.embed_documents([doc.page_content for doc in texts])
#         return embeddings_function, embeddings
    
#     def ollama_model(self):
#         embedding_function = self.vector_store()
#         # Perform a similarity search
#         vector_database_retrieve = Chroma(persist_directory="vector_database", embedding_function=embedding_function)
#         docs = vector_database_retrieve.similarity_search(self.query,k=1)
        
#         # Define the prompt with the context
#         context = "\n".join([doc.page_content for doc in docs])
#         prompt = f"{context}\n\nBased on the provided context, please provide a concise and meaningful answer in two lines or less:"

        
#         # Initialize the Ollama model
#         llm = Ollama(model="gemma2:2b")
#         # Get the answer from the model
#         answer = llm(prompt)
#         return answer

#     def vector_store(self):
#         embedding_function, _ = self.embedding_model()
#         split_text = self.text_split()
#         # Create and persist the vector database
#         Chroma.from_documents(split_text, embedding_function, persist_directory="vector_database")
#         return embedding_function
import warnings
from langchain_community.document_loaders import PDFMinerLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

warnings.filterwarnings('ignore')

class FileReader:
    def __init__(self, dir_path, query):
        self.dir_path = dir_path
        self.query = query
        self.embedding_function = None
        self.vector_database = None
        self.load_and_prepare_data()

    def load_documents(self):
        loader = DirectoryLoader(self.dir_path, glob="**/*.pdf", loader_cls=PDFMinerLoader)
        return loader.load()

    def text_split(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30)
        combined_text = [doc.page_content for doc in documents]
        split_docs = text_splitter.create_documents(combined_text)
        return split_docs

    def embedding_model(self, split_docs):
        embeddings_function = OllamaEmbeddings(model="gemma2:2b")
        embeddings = embeddings_function.embed_documents([doc.page_content for doc in split_docs])
        return embeddings_function, embeddings
    
    def load_and_prepare_data(self):
        documents = self.load_documents()
        split_docs = self.text_split(documents)
        self.embedding_function, _ = self.embedding_model(split_docs)
        self.vector_database = Chroma.from_documents(split_docs, self.embedding_function, persist_directory="vector_database")

    def ollama_model(self):
        vector_database_retrieve = Chroma(persist_directory="vector_database", embedding_function=self.embedding_function)
        docs = vector_database_retrieve.similarity_search(self.query)
        
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"{context}\n\nBased on the provided context, please provide a concise and meaningful answer in two lines or less:"
        
        llm = Ollama(model="gemma2:2b")
        answer = llm(prompt)
        return answer
