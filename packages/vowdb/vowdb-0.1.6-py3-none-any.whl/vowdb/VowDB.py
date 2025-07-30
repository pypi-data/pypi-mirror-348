import threading
import logging
import os
import pickle
import psutil
import uuid
import random
import string
import re
from typing import List, Dict, Optional, Any

class VowDB:
    """A high-performance synchronous vector database for similarity search using Faiss."""
    
    def __init__(
        self,
        embedding_model: Any,
        vector_dim: int,
        file_path: str = "vectors.faiss",
        max_elements: int = 100000,
        cache_size: int = 1000
    ):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.embedding_model = embedding_model
        if not isinstance(vector_dim, int) or vector_dim <= 0:
            raise ValueError("vector_dim must be a positive integer")
        self.vector_dim = vector_dim
        self.logger.info(f"Initialized with embedding model, dimension: {self.vector_dim}")
        
        self.max_elements = max_elements
        self._validate_memory()
        import faiss
        try:
            self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)
            self.index.hnsw.ef_construction = 200
            self.index.hnsw.ef_search = 50
        except Exception as e:
            self.logger.error(f"Failed to initialize Faiss index: {str(e)}")
            raise
        self.num_elements = 0
        self.logger.info(f"Initialized Faiss HNSW index with max_elements: {max_elements}")
        self.vector_file = file_path
        self.metadata_file = file_path + ".meta"
        self.metadata = {}
        self.lock = threading.Lock()
        self.embedding_cache = {}
        self.cache_size = cache_size

    def _validate_memory(self):
        vector_size = self.vector_dim * 4
        index_size = self.max_elements * vector_size
        available_memory = psutil.virtual_memory().available
        if index_size > available_memory * 0.8:
            self.logger.warning(
                f"Index size ({index_size / 1e6:.2f} MB) may exceed available memory "
                f"({available_memory / 1e6:.2f} MB)"
            )
            raise ValueError("Insufficient memory for requested max_elements")

    def _generate_random_metadata(self) -> Dict:
        """Generate random metadata for testing."""
        return {
            "id": str(uuid.uuid4()),
            "category": ''.join(random.choices(string.ascii_lowercase, k=8)),
            "score": random.uniform(0, 1)
        }

    def embed_text(self, text: str) -> 'np.ndarray':
        import numpy as np
        if text in self.embedding_cache:
            self.logger.debug(f"Retrieved embedding for '{text}' from cache")
            return self.embedding_cache[text]
        try:
            self.logger.debug(f"Generating embedding for '{text}'")
            if hasattr(self.embedding_model, 'encode'):
                vector = self.embedding_model.encode([text])[0]
            elif hasattr(self.embedding_model, 'embed_documents'):
                vector = self.embedding_model.embed_documents([text])[0]
            else:
                raise AttributeError("Embedding model must have 'encode' or 'embed_documents' method")
            vector = np.array(vector, dtype=np.float32) if isinstance(vector, list) else vector
            if vector.shape[-1] != self.vector_dim:
                raise ValueError(f"Embedding dimension {vector.shape[-1]} does not match vector_dim {self.vector_dim}")
            if len(self.embedding_cache) < self.cache_size:
                self.embedding_cache[text] = vector
                self.logger.debug(f"Cached embedding for '{text}'")
            return vector
        except Exception as e:
            self.logger.error(
                f"Failed to embed text '{text}': {str(e)}. "
                "Ensure Ollama server is running (`ollama serve`) and model 'nomic-embed-text' is pulled (`ollama pull nomic-embed-text`)."
            )
            raise

    def embed_texts(self, texts: List[str]) -> 'np.ndarray':
        import numpy as np
        vectors = []
        uncached_texts = []
        uncached_indices = []
        for i, text in enumerate(texts):
            if text in self.embedding_cache:
                vectors.append(self.embedding_cache[text])
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        if uncached_texts:
            try:
                if hasattr(self.embedding_model, 'encode'):
                    new_vectors = self.embedding_model.encode(uncached_texts)
                elif hasattr(self.embedding_model, 'embed_documents'):
                    new_vectors = self.embedding_model.embed_documents(uncached_texts)
                else:
                    raise AttributeError("Embedding model must have 'encode' or 'embed_documents' method")
                new_vectors = [np.array(v, dtype=np.float32) if isinstance(v, list) else v for v in new_vectors]
                for vector, text, idx in zip(new_vectors, uncached_texts, uncached_indices):
                    if vector.shape[-1] != self.vector_dim:
                        raise ValueError(f"Embedding dimension {vector.shape[-1]} does not match vector_dim {self.vector_dim}")
                    vectors.insert(idx, vector)
                    if len(self.embedding_cache) < self.cache_size:
                        self.embedding_cache[text] = vector
            except Exception as e:
                self.logger.error(
                    f"Failed to embed texts: {str(e)}. "
                    "Ensure Ollama server is running (`ollama serve`) and model 'nomic-embed-text' is pulled (`ollama pull nomic-embed-text`)."
                )
                raise
        return np.array(vectors)

    def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
        import numpy as np
        try:
            vector = self.embed_text(text)
            with self.lock:
                if self.num_elements >= self.max_elements:
                    return {"status": "error", "message": "Index full"}
                idx = self.num_elements
                self.index.add(np.array([vector], dtype=np.float32))
                random_meta = self._generate_random_metadata()
                final_meta = metadata or {}
                final_meta.update(random_meta)
                self.metadata[idx] = {"text": text, "metadata": final_meta}
                self.num_elements += 1
            self.logger.info(f"Inserted item with ID: {idx}")
            return {
                "status": "inserted",
                "id": idx,
                "vector": np.array2string(vector, separator=','),
                "metadata": final_meta
            }
        except Exception as e:
            self.logger.error(f"Insert failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
        import numpy as np
        try:
            vectors = self.embed_texts(texts)
            metadatas = metadatas or [{}] * len(texts)
            with self.lock:
                start_idx = self.num_elements
                if start_idx + len(texts) > self.max_elements:
                    return [{"status": "error", "message": "Index full"}] * len(texts)
                idxs = list(range(start_idx, start_idx + len(texts)))
                self.index.add(vectors.astype(np.float32))
                results = []
                for idx, text, metadata, vector in zip(idxs, texts, metadatas, vectors):
                    random_meta = self._generate_random_metadata()
                    final_meta = metadata.copy()
                    final_meta.update(random_meta)
                    self.metadata[idx] = {"text": text, "metadata": final_meta}
                    results.append({
                        "status": "inserted",
                        "id": idx,
                        "vector": np.array2string(vector, separator=','),
                        "metadata": final_meta
                    })
                self.num_elements += len(texts)
            self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
            return results
        except Exception as e:
            self.logger.error(f"Batch insert failed: {str(e)}")
            return [{"status": "error", "message": str(e)}] * len(texts)

    def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
        import numpy as np
        try:
            if idx >= self.num_elements:
                return {"status": "error", "message": "Invalid index"}
            vector = self.embed_text(text)
            with self.lock:
                import faiss
                temp_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
                temp_index.hnsw.ef_construction = 200
                temp_index.hnsw.ef_search = 50
                all_vectors = self.index.reconstruct_n(0, self.num_elements)
                all_vectors[idx] = vector
                temp_index.add(all_vectors)
                self.index = temp_index
                random_meta = self._generate_random_metadata()
                final_meta = metadata or self.metadata.get(idx, {}).get("metadata", {})
                final_meta.update(random_meta)
                self.metadata[idx] = {"text": text, "metadata": final_meta}
            self.logger.info(f"Updated item with ID: {idx}")
            return {
                "status": "updated",
                "id": idx,
                "vector": np.array2string(vector, separator=','),
                "metadata": final_meta
            }
        except Exception as e:
            self.logger.error(f"Update failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def delete(self, idx: int) -> Dict:
        import numpy as np
        try:
            with self.lock:
                if idx >= self.num_elements:
                    return {"status": "error", "message": "Invalid index"}
                self.metadata.pop(idx, None)
                import faiss
                all_vectors = self.index.reconstruct_n(0, self.num_elements)
                mask = np.ones(self.num_elements, dtype=bool)
                mask[idx] = False
                remaining_vectors = all_vectors[mask]
                new_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
                new_index.hnsw.ef_construction = 200
                new_index.hnsw.ef_search = 50
                if remaining_vectors.size > 0:
                    new_index.add(remaining_vectors.astype(np.float32))
                self.index = new_index
                self.num_elements -= 1
                new_metadata = {}
                for i, j in enumerate(sorted(set(range(self.num_elements + 1)) - {idx})):
                    if j in self.metadata:
                        new_metadata[i] = self.metadata[j]
                self.metadata = new_metadata
                self.logger.info(f"Deleted item with ID: {idx}")
                return {"status": "deleted", "id": idx}
        except Exception as e:
            self.logger.error(f"Delete failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def _parse_query(self, query: str) -> Dict:
        """Parse a single-line SQL-like query into a structured format."""
        if not query:
            return {"type": "match_all"}

        def parse_condition(term: str) -> Dict:
            term = term.strip()
            if "=" in term or "==" in term:
                field, value = term.replace("==", "=").split("=", 1)
                operators = [">=", "<=", "!=", ">", "<"]
                op = "="
                for operator in operators:
                    if value.startswith(operator):
                        op = operator
                        value = value[len(operator):]
                        break
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                if field == "text" and value.endswith("*"):
                    return {
                        "type": "contains",
                        "field": "text",
                        "value": value[:-1].lower()
                    }
                if "-" in value and op == "=":
                    try:
                        start, end = value.split("-")
                        if field in ["score"]:
                            return {
                                "type": "range",
                                "field": field,
                                "start": float(start),
                                "end": float(end),
                                "inclusive": True
                            }
                        else:
                            return {
                                "type": "range",
                                "field": field,
                                "start": start,
                                "end": end,
                                "inclusive": True
                            }
                    except ValueError:
                        raise ValueError(f"Invalid range format in '{term}'")
                try:
                    if field in ["score"]:
                        value = float(value)
                    return {
                        "type": "compare",
                        "field": field,
                        "operator": op,
                        "value": value
                    }
                except ValueError:
                    return {
                        "type": "contains" if field == "text" else "compare",
                        "field": field,
                        "operator": op,
                        "value": value
                    }
            else:
                return {"type": "contains", "value": term.lower()}

        and_pattern = re.compile(r'\s*&&\s*')
        and_parts = and_pattern.split(query)
        if len(and_parts) > 1:
            return {
                "type": "and",
                "conditions": [self._parse_query(part.strip()) for part in and_parts]
            }

        or_parts = query.split("||")
        if len(or_parts) > 1:
            return {
                "type": "or",
                "conditions": [parse_condition(part.strip()) for part in or_parts]
            }

        return parse_condition(query)

    def _evaluate_condition(self, metadata: Dict, text: str, condition: Dict) -> bool:
        """Evaluate if metadata and/or text satisfies a query condition."""
        if condition["type"] == "match_all":
            return True
        elif condition["type"] == "and":
            return all(self._evaluate_condition(metadata, text, sub_cond) for sub_cond in condition["conditions"])
        elif condition["type"] == "or":
            return any(self._evaluate_condition(metadata, text, sub_cond) for sub_cond in condition["conditions"])
        elif condition["type"] == "compare":
            if condition["field"] == "text":
                value = text
            else:
                if condition["field"] not in metadata:
                    return False
                value = metadata[condition["field"]]
            op = condition["operator"]
            cond_value = condition["value"]
            if isinstance(value, (int, float)) and isinstance(cond_value, (int, float)):
                if op in ["=", "=="]: return value == cond_value
                if op == ">": return value > cond_value
                if op == "<": return value < cond_value
                if op == ">=": return value >= cond_value
                if op == "<=": return value <= cond_value
                if op == "!=": return value != cond_value
            else:
                value = str(value)
                cond_value = str(cond_value)
                if op in ["=", "=="]: return value == cond_value
                if op == "!=": return value != cond_value
                if op == ">": return value > cond_value
                if op == "<": return value < cond_value
                if op == ">=": return value >= cond_value
                if op == "<=": return value <= cond_value
            return False
        elif condition["type"] == "range":
            if condition["field"] == "text":
                value = text
            else:
                if condition["field"] not in metadata:
                    return False
                value = metadata[condition["field"]]
            if isinstance(value, (int, float)):
                return condition["start"] <= value <= condition["end"]
            else:
                return condition["start"] <= str(value) <= condition["end"]
        elif condition["type"] == "contains":
            if condition.get("field") == "text":
                return condition["value"] in text.lower()
            if condition["value"] in text.lower():
                return True
            return any(
                condition["value"] in str(value).lower()
                for value in metadata.values()
            )
        return False

    def find(self, query: str, top_k: int = 3, filter_query: Optional[str] = None) -> List[Dict]:
        import numpy as np
        try:
            if self.num_elements == 0:
                self.logger.warning("Find called on empty index")
                return []
            parsed_filter = self._parse_query(filter_query) if filter_query else {"type": "match_all"}
            query_vector = self.embed_text(query)
            if query_vector.shape[-1] != self.vector_dim:
                raise ValueError(f"Query vector dimension {query_vector.shape[-1]} does not match index dimension {self.vector_dim}")
            search_k = min(top_k * 2, self.num_elements)
            distances, labels = self.index.search(np.array([query_vector], dtype=np.float32), search_k)
            results = []
            for label, dist in zip(labels[0], distances[0]):
                if len(results) >= top_k:
                    break
                if label in self.metadata:
                    meta = self.metadata[label]["metadata"]
                    text = self.metadata[label]["text"]
                    if self._evaluate_condition(meta, text, parsed_filter):
                        vector = self.index.reconstruct(int(label))
                        results.append({
                            "id": int(label),
                            "distance": float(dist),
                            "vector": np.array2string(vector, separator=','),
                            "metadata": meta
                        })
            self.logger.info(f"Found {len(results)} results for query with filter: {filter_query}")
            return results
        except Exception as e:
            self.logger.error(f"Find failed: {str(e)}")
            return [{"status": "error", "message": str(e)}]

    def save(self) -> Dict:
        try:
            with self.lock:
                import faiss
                faiss.write_index(self.index, self.vector_file)
                with open(self.metadata_file, "wb") as f:
                    pickle.dump(self.metadata, f)
            self.logger.info("Saved index and metadata")
            return {"status": "saved"}
        except Exception as e:
            self.logger.error(f"Save failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def load(self) -> Dict:
        try:
            if not os.path.exists(self.vector_file):
                return {"status": "error", "message": "Index file not found"}
            with self.lock:
                import faiss
                self.index = faiss.read_index(self.vector_file)
                self.index.hnsw.ef_search = 50
                with open(self.metadata_file, "rb") as f:
                    self.metadata = pickle.load(f)
                self.num_elements = self.index.ntotal
            self.logger.info("Loaded index and metadata")
            return {"status": "loaded"}
        except Exception as e:
            self.logger.error(f"Load failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_stats(self) -> Dict:
        return {
            "num_elements": self.num_elements,
            "max_elements": self.max_elements,
            "cache_size": len(self.embedding_cache),
            "memory_usage_mb": (self.num_elements * self.vector_dim * 4) / 1e6
        }