from src.helper import load_pdf_file, text_split, download_huggingface_embeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY


extracted_data = load_pdf_file(data = 'data/')
text_chunks = text_split(extracted_data)
embeddings = download_huggingface_embeddings()


pc = Pinecone(api_key= PINECONE_API_KEY)

index_name = "askmedi"

pc.create_index(
    name=index_name,
    dimension=384,  # Dimension of the embeddings
    metric="cosine",  # Similarity metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
        # size="small"
    )
)

#Embed each chunk and upsert the embeddings into your Pinecone index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name
)

