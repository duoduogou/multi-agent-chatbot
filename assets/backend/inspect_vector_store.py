
from vector_store import VectorStore
from logger import logger
import logging

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

def inspect_store():
    print("Initializing VectorStore...")
    vs = VectorStore()
    
    # Try to search for anything matching "GPU" which should be in the uploaded doc
    print("Querying for 'GPU'...")
    try:
        docs = vs.get_documents("GPU", k=10)
        print(f"Found {len(docs)} documents for query 'GPU'")
        for i, doc in enumerate(docs):
            print(f"Doc {i}: Source={doc.metadata.get('source')}, Content Preview={doc.page_content[:100]}...")
            
    except Exception as e:
        print(f"Error querying: {e}")

    # Also try to just see if we can get collection stats if possible, 
    # but vs.get_documents is the main public API.
    
if __name__ == "__main__":
    inspect_store()
