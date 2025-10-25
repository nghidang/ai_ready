import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

# Fix tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize ChromaDB and embedding model
def initialize_chroma_db():
    """Initialize ChromaDB client and embedding model"""
    try:
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Initialize embedding model
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        collection = client.get_or_create_collection(
            name="policies",
            metadata={"hnsw:space": "cosine"}
        )
        
        return client, collection, embedding_model
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return None, None, None

def load_policies_to_chroma(policies_collection, embedding_model, policies_file='example_policies.json'):
    """Load policies from JSON file into ChromaDB"""
    if not policies_collection or not embedding_model:
        return False
    
    try:
        # Load policies from JSON file
        with open(policies_file, 'r') as f:
            policies = json.load(f)
        
        # Check if policies are already loaded
        if policies_collection.count() > 0:
            print("Policies already loaded in ChromaDB")
            return True
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for policy in policies:
            documents.append(policy['text'])
            metadatas.append(policy['metadata'])
            ids.append(policy['id'])
        
        # Add to ChromaDB
        policies_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Loaded {len(policies)} policies into ChromaDB")
        return True
        
    except Exception as e:
        print(f"Error loading policies: {e}")
        return False

def query_policies(policies_collection, embedding_model, question, n_results=3):
    """Query policies using semantic search"""
    if not policies_collection or not embedding_model:
        return "Policy database not available. Please check ChromaDB setup."
    
    try:
        # Generate embedding for the question
        query_embedding = embedding_model.encode(question).tolist()
        
        # Search in ChromaDB
        results = policies_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return "No relevant policies found."
        
        # Format results
        formatted_results = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            formatted_results.append({
                'text': doc,
                'metadata': metadata,
                'relevance_score': 1 - distance  # Convert distance to similarity
            })
        
        return formatted_results
        
    except Exception as e:
        return f"Error querying policies: {str(e)}"

class PolicyRetriever:
    """Policy retrieval class that manages ChromaDB operations"""
    
    def __init__(self, policies_file='example_policies.json'):
        self.policies_file = policies_file
        self.client, self.collection, self.embedding_model = initialize_chroma_db()
        self._load_policies()
    
    def _load_policies(self):
        """Load policies on initialization"""
        if self.collection and self.embedding_model:
            load_policies_to_chroma(self.collection, self.embedding_model, self.policies_file)
    
    def query_policy(self, question):
        """Query company policies and return relevant information"""
        try:
            results = query_policies(self.collection, self.embedding_model, question)
            
            if isinstance(results, str):  # Error message
                return results
            
            if not results:
                return "No relevant policies found for your question."
            
            # Format the response
            response = "Based on company policies:\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. **{result['metadata']['category']}** (Relevance: {result['relevance_score']:.2f})\n"
                response += f"   {result['text']}\n"
                if 'effective_date' in result['metadata']:
                    response += f"   *Effective: {result['metadata']['effective_date']}*\n"
                response += "\n"
            
            return response
            
        except Exception as e:
            return f"Error querying policies: {str(e)}"
    
    def is_available(self):
        """Check if the policy retriever is properly initialized"""
        return self.collection is not None and self.embedding_model is not None
