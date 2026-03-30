from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from documents.models import DocumentChunk, PolicyDocument
import os

def load_extract():
     folder_path = os.path.join(os.getcwd(), "policy_documents")
     print("Loading PDFs from:", folder_path)
     loader = DirectoryLoader(
          folder_path,
          glob="*.pdf",
          loader_cls=PyPDFLoader
     )

     documents = loader.load()
     print(f"Loaded {len(documents)} documents")
     return documents



def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
       chunk_size = 1000,
       chunk_overlap = 100
    )
 
    chunks = splitter.split_documents(documents)
    return chunks

def store_chunks(chunks):
    for index,chunk in enumerate(chunks):
        text = chunk.page_content
        source = chunk.metadata["source"]
        filename = os.path.basename(source)
        policy_doc, _ = PolicyDocument.objects.get_or_create(file_reference = filename)
        chunk_split = DocumentChunk(
            policy_document=policy_doc ,
            chunk_text = text,
            chunk_index = index
        )
        chunk_split.save()