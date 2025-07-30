VowDB 🔥

Blazing-fast vector database for similarity search, like Pinecone or Milvus. Powered by Faiss & any embedding model.



Install 💻

Install the latest version of VowDB using pip:

pip install vowdb



Requires Python 3.8+, faiss-cpu, numpy, psutil, and an embedding model (e.g., sentence-transformers, langchain_ollama).



Setup 🚀

Initialize with any embedding model and specify vector dimension. For Ollama, ensure the server is running and the model is pulled.

Ollama Setup





Install Ollama: Download from https://ollama.com/ and follow installation instructions.



Start the Ollama server:

ollama serve



Pull the model:

ollama pull nomic-embed-text

Code Example

from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaEmbeddings
from vowdb import VowDB

# Example with SentenceTransformers (dimension: 384)
model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./model_cache")
db = VowDB(embedding_model=model, vector_dim=384, file_path="vectors.faiss")

# Example with OllamaEmbeddings (dimension: 768 for nomic-embed-text)
ollama_model = OllamaEmbeddings(model="nomic-embed-text")
db_ollama = VowDB(embedding_model=ollama_model, vector_dim=768, file_path="ollama_vectors.faiss")



Ready in ~1.2s.



Add Data 📝

Insert vectors with metadata:

# One
result = db.insert("Hello World", metadata={"greeting": "yes"})  # ~0.57s
# Returns: {"status": "inserted", "id": 0, "vector": "[0.1,0.2,...]", "metadata": {"greeting": "yes", "id": "uuid", ...}}

# Many
texts = ["Hii", "I Am Rushikesh!", "News article"]
metadatas = [{"greeting": "yes"}, {"category": "introduction"}, {"greeting": "no"}]
results = db.insert_batch(texts, metadatas)



Search 🔍

Query with vectors and SQL-like filters (use && for AND, || for OR). Returns vectors and metadata.

1. AND Power

db.find("hello", top_k=3, filter_query="category=news && score>0.9 && greeting=yes")

Result:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}



2. Vector Search

db.find("hello", top_k=3)

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=1, distance=0.48, vector=[0.3,0.4,...], metadata={category=greeting, score=0.6, greeting=yes}



3. Exact Match

db.find("Hello World", top_k=3, filter_query="text=Hello World")

Result:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}



4. Prefix Hunt

db.find("Hel", top_k=3, filter_query="text=Hel*")

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=1, distance=0.48, vector=[0.3,0.4,...], metadata={category=greeting, score=0.6, greeting=yes}



5. Category Snap

db.find("news", top_k=3, filter_query="category=news")

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=2, distance=0.50, vector=[0.5,0.6,...], metadata={category=news, score=0.7, greeting=no}



6. OR Flex

db.find("news", top_k=3, filter_query="category=news||greeting")

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=1, distance=0.48, vector=[0.3,0.4,...], metadata={category=greeting, score=0.6, greeting=yes}



7. Multi-Filter

db.find("news", top_k=3, filter_query="category=news && score>0.7 && greeting=yes")

Result:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}



8. Score Range

db.find("news", top_k=3, filter_query="score=0.6-0.8")

Results:
id=1, distance=0.48, vector=[0.3,0.4,...], metadata={category=greeting, score=0.6, greeting=yes}
id=2, distance=0.50, vector=[0.5,0.6,...], metadata={category=news, score=0.7, greeting=no}



9. Skip Some

db.find("news", top_k=3, filter_query="text!=Hii && category!=introduction")

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=2, distance=0.50, vector=[0.5,0.6,...], metadata={category=news, score=0.7, greeting=no}



10. Name Drop

db.find("Rushikesh", top_k=3)

Result:
id=1, distance=0.20, vector=[0.7,0.8,...], metadata={category=introduction, score=0.9}



11. Text or Score

db.find("Hel", top_k=3, filter_query="text=Hel*||score>=0.9")

Results:
id=0, distance=0.45, vector=[0.1,0.2,...], metadata={category=news, score=0.95, greeting=yes}
id=1, distance=0.20, vector=[0.7,0.8,...], metadata={category=introduction, score=0.9}



Save/Load 💾

Keep or get data:

db.save()
db.load()



Info 🌟

Version: 0.1.5
Author: Rushikesh Sunil Kotkar
License: MIT
GitHub: https://github.com/rushikeshkotkar04/vowdb
PyPI: Fast vector similarity with slick = queries.



Contribute 🤝

Got ideas? Issues? PRs?
Hit up: https://github.com/rushikeshkotkar04/vowdb