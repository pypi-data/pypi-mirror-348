import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import threading
import logging
import os
import pickle
import psutil
import uuid
import random
import string
import re

class VowDB:
    """A high-performance synchronous vector database for similarity search using Faiss."""
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        file_path: str = "vectors.faiss",
        max_elements: int = 100000,
        cache_size: int = 1000
    ):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.embedding_model = SentenceTransformer(model_name)
        self.vector_dim = self.embedding_model.get_sentence_embedding_dimension()
        self.logger.info(f"Initialized embedding model: {model_name}, dimension: {self.vector_dim}")
        self.max_elements = max_elements
        self._validate_memory()
        self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)
        self.index.hnsw.ef_construction = 200
        self.index.hnsw.ef_search = 50
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

    def embed_text(self, text: str) -> np.ndarray:
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        vector = self.embedding_model.encode([text])[0]
        if len(self.embedding_cache) < self.cache_size:
            self.embedding_cache[text] = vector
        return vector

    def embed_texts(self, texts: List[str]) -> np.ndarray:
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
            new_vectors = self.embedding_model.encode(uncached_texts)
            for text, vector, idx in zip(uncached_texts, new_vectors, uncached_indices):
                vectors.insert(idx, vector)
                if len(self.embedding_cache) < self.cache_size:
                    self.embedding_cache[text] = vector
        return np.array(vectors)

    def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
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
                "text": text,
                "metadata_key": final_meta["id"],
                "embedding": np.array2string(vector, separator=',')
            }
        except Exception as e:
            self.logger.error(f"Insert failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
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
                        "text": text,
                        "metadata_key": final_meta["id"],
                        "embedding": np.array2string(vector, separator=',')
                    })
                self.num_elements += len(texts)
            self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
            return results
        except Exception as e:
            self.logger.error(f"Batch insert failed: {str(e)}")
            return [{"status": "error", "message": str(e)}] * len(texts)

    def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
        try:
            if idx >= self.num_elements:
                return {"status": "error", "message": "Invalid index"}
            vector = self.embed_text(text)
            with self.lock:
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
                "text": text,
                "metadata_key": final_meta["id"],
                "embedding": np.array2string(vector, separator=',')
            }
        except Exception as e:
            self.logger.error(f"Update failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def delete(self, idx: int) -> Dict:
        try:
            with self.lock:
                if idx >= self.num_elements:
                    return {"status": "error", "message": "Invalid index"}
                self.metadata.pop(idx, None)
                self.logger.info(f"Deleted item with ID: {idx}")
                return {"status": "deleted", "id": idx}
        except Exception as e:
            self.logger.error(f"Delete failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    # def _parse_query(self, query: str) -> Dict:
    #     """Parse a single-line SQL-like query into a structured format."""
    #     if not query:
    #         return {"type": "match_all"}

    #     def parse_condition(term: str) -> Dict:
    #         term = term.strip()
    #         if ":" in term:
    #             field, value = term.split(":", 1)
    #             # Check for operators: ==, >=, <=, !=, >, <
    #             operators = ["==", ">=", "<=", "!=", ">", "<"]
    #             op = "="
    #             for operator in operators:
    #                 if value.startswith(operator):
    #                     op = operator
    #                     value = value[len(operator):]
    #                     break
    #             # Handle quoted strings (e.g., category=="news")
    #             if value.startswith('"') and value.endswith('"'):
    #                 value = value[1:-1]
    #             # Check for wildcard in text field
    #             if field == "text" and value.endswith("*"):
    #                 return {
    #                     "type": "contains",
    #                     "field": "text",
    #                     "value": value[:-1].lower()
    #                 }
    #             # Check for range
    #             if "-" in value and op in ["=", "=="]:
    #                 try:
    #                     start, end = value.split("-")
    #                     if field in ["score"]:
    #                         return {
    #                             "type": "range",
    #                             "field": field,
    #                             "start": float(start),
    #                             "end": float(end),
    #                             "inclusive": True
    #                         }
    #                     else:  # String range (lexicographic)
    #                         return {
    #                             "type": "range",
    #                             "field": field,
    #                             "start": start,
    #                             "end": end,
    #                             "inclusive": True
    #                         }
    #                 except ValueError:
    #                     raise ValueError(f"Invalid range format in '{term}'")
    #             # Comparison operator
    #             try:
    #                 if field in ["score"]:
    #                     value = float(value)
    #                 return {
    #                     "type": "compare",
    #                     "field": field,
    #                     "operator": op,
    #                     "value": value
    #                 }
    #             except ValueError:
    #                 return {
    #                     "type": "compare",
    #                     "field": field,
    #                     "operator": op,
    #                     "value": value
    #                 }
    #         else:  # Single-word query
    #             return {"type": "contains", "value": term.lower()}

    #     # Split by && or %&& (AND)
    #     and_pattern = re.compile(r'\s*(?:&&|%&&)\s*')
    #     and_parts = and_pattern.split(query)
    #     if len(and_parts) > 1:
    #         return {
    #             "type": "and",
    #             "conditions": [self._parse_query(part.strip()) for part in and_parts]
    #         }

    #     # Split by || (OR)
    #     or_parts = query.split("||")
    #     if len(or_parts) > 1:
    #         return {
    #             "type": "or",
    #             "conditions": [parse_condition(part.strip()) for part in or_parts]
    #         }

    #     return parse_condition(query)
    def _parse_query(self, query: str) -> Dict:
        """Parse a single-line SQL-like query into a structured format."""
        if not query:
            return {"type": "match_all"}

        def parse_condition(term: str) -> Dict:
            term = term.strip()
            if "=" in term:
                field, value = term.split("=", 1)
                # Check for operators: ==, >=, <=, !=, >, <
                operators = [">=", "<=", "!=", ">", "<"]
                op = "="
                for operator in operators:
                    if value.startswith(operator):
                        op = operator
                        value = value[len(operator):]
                        break
                # Handle quoted strings (e.g., category="news")
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                # Check for wildcard in text field
                if field == "text" and value.endswith("*"):
                    return {
                        "type": "contains",
                        "field": "text",
                        "value": value[:-1].lower()
                    }
                # Check for range
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
                        else:  # String range (lexicographic)
                            return {
                                "type": "range",
                                "field": field,
                                "start": start,
                                "end": end,
                                "inclusive": True
                            }
                    except ValueError:
                        raise ValueError(f"Invalid range format in '{term}'")
                # Comparison operator
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
                        "type": "compare",
                        "field": field,
                        "operator": op,
                        "value": value
                    }
            else:  # Single-word query
                return {"type": "contains", "value": term.lower()}

        # Split by && (AND)
        and_pattern = re.compile(r'\s*&&\s*')
        and_parts = and_pattern.split(query)
        if len(and_parts) > 1:
            return {
                "type": "and",
                "conditions": [self._parse_query(part.strip()) for part in and_parts]
            }

        # Split by || (OR)
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
            # Handle numeric comparisons
            if isinstance(value, (int, float)) and isinstance(cond_value, (int, float)):
                if op in ["=", "=="]: return value == cond_value
                if op == ">": return value > cond_value
                if op == "<": return value < cond_value
                if op == ">=": return value >= cond_value
                if op == "<=": return value <= cond_value
                if op == "!=": return value != cond_value
            # Handle string comparisons
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
            # Single-word query: search text and metadata
            if condition["value"] in text.lower():
                return True
            return any(
                condition["value"] in str(value).lower()
                for value in metadata.values()
            )
        return False

    def find(self, query: str, top_k: int = 3, filter_query: Optional[str] = None) -> List[Dict]:
        try:
            parsed_filter = self._parse_query(filter_query) if filter_query else {"type": "match_all"}
            query_vector = self.embed_text(query)
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
                            "text": text,
                            "metadata_key": meta["id"],
                            "embedding": np.array2string(vector, separator=',')
                        })
            self.logger.info(f"Found {len(results)} results for query with filter: {filter_query}")
            return results
        except Exception as e:
            self.logger.error(f"Find failed: {str(e)}")
            return [{"status": "error", "message": str(e)}]

    def save(self) -> Dict:
        try:
            with self.lock:
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


# import faiss
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Optional
# import threading
# import logging
# import os
# import pickle
# import psutil
# import uuid
# import random
# import string
# import re

# class VowDB:
#     """A high-performance synchronous vector database for similarity search using Faiss."""
    
#     def __init__(
#         self,
#         model_name: str = "all-MiniLM-L6-v2",
#         file_path: str = "vectors.faiss",
#         max_elements: int = 100000,
#         cache_size: int = 1000
#     ):
#         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#         self.logger = logging.getLogger(__name__)
#         self.embedding_model = SentenceTransformer(model_name)
#         self.vector_dim = self.embedding_model.get_sentence_embedding_dimension()
#         self.logger.info(f"Initialized embedding model: {model_name}, dimension: {self.vector_dim}")
#         self.max_elements = max_elements
#         self._validate_memory()
#         self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)
#         self.index.hnsw.ef_construction = 200
#         self.index.hnsw.ef_search = 50
#         self.num_elements = 0
#         self.logger.info(f"Initialized Faiss HNSW index with max_elements: {max_elements}")
#         self.vector_file = file_path
#         self.metadata_file = file_path + ".meta"
#         self.metadata = {}
#         self.lock = threading.Lock()
#         self.embedding_cache = {}
#         self.cache_size = cache_size

#     def _validate_memory(self):
#         vector_size = self.vector_dim * 4
#         index_size = self.max_elements * vector_size
#         available_memory = psutil.virtual_memory().available
#         if index_size > available_memory * 0.8:
#             self.logger.warning(
#                 f"Index size ({index_size / 1e6:.2f} MB) may exceed available memory "
#                 f"({available_memory / 1e6:.2f} MB)"
#             )
#             raise ValueError("Insufficient memory for requested max_elements")

#     def _generate_random_metadata(self) -> Dict:
#         """Generate random metadata for testing."""
#         return {
#             "id": str(uuid.uuid4()),
#             "category": ''.join(random.choices(string.ascii_lowercase, k=8)),
#             "score": random.uniform(0, 1)
#         }

#     def embed_text(self, text: str) -> np.ndarray:
#         if text in self.embedding_cache:
#             return self.embedding_cache[text]
#         vector = self.embedding_model.encode([text])[0]
#         if len(self.embedding_cache) < self.cache_size:
#             self.embedding_cache[text] = vector
#         return vector

#     def embed_texts(self, texts: List[str]) -> np.ndarray:
#         vectors = []
#         uncached_texts = []
#         uncached_indices = []
#         for i, text in enumerate(texts):
#             if text in self.embedding_cache:
#                 vectors.append(self.embedding_cache[text])
#             else:
#                 uncached_texts.append(text)
#                 uncached_indices.append(i)
#         if uncached_texts:
#             new_vectors = self.embedding_model.encode(uncached_texts)
#             for text, vector, idx in zip(uncached_texts, new_vectors, uncached_indices):
#                 vectors.insert(idx, vector)
#                 if len(self.embedding_cache) < self.cache_size:
#                     self.embedding_cache[text] = vector
#         return np.array(vectors)

#     def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
#         try:
#             vector = self.embed_text(text)
#             with self.lock:
#                 if self.num_elements >= self.max_elements:
#                     return {"status": "error", "message": "Index full"}
#                 idx = self.num_elements
#                 self.index.add(np.array([vector], dtype=np.float32))
#                 random_meta = self._generate_random_metadata()
#                 final_meta = metadata or {}
#                 final_meta.update(random_meta)
#                 self.metadata[idx] = {"text": text, "metadata": final_meta}
#                 self.num_elements += 1
#             self.logger.info(f"Inserted item with ID: {idx}")
#             return {
#                 "status": "inserted",
#                 "id": idx,
#                 "text": text,
#                 "metadata_key": final_meta["id"],
#                 "embedding": np.array2string(vector, separator=',')
#             }
#         except Exception as e:
#             self.logger.error(f"Insert failed: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
#         try:
#             vectors = self.embed_texts(texts)
#             metadatas = metadatas or [{}] * len(texts)
#             with self.lock:
#                 start_idx = self.num_elements
#                 if start_idx + len(texts) > self.max_elements:
#                     return [{"status": "error", "message": "Index full"}] * len(texts)
#                 idxs = list(range(start_idx, start_idx + len(texts)))
#                 self.index.add(vectors.astype(np.float32))
#                 results = []
#                 for idx, text, metadata, vector in zip(idxs, texts, metadatas, vectors):
#                     random_meta = self._generate_random_metadata()
#                     final_meta = metadata.copy()
#                     final_meta.update(random_meta)
#                     self.metadata[idx] = {"text": text, "metadata": final_meta}
#                     results.append({
#                         "status": "inserted",
#                         "id": idx,
#                         "text": text,
#                         "metadata_key": final_meta["id"],
#                         "embedding": np.array2string(vector, separator=',')
#                     })
#                 self.num_elements += len(texts)
#             self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
#             return results
#         except Exception as e:
#             self.logger.error(f"Batch insert failed: {str(e)}")
#             return [{"status": "error", "message": str(e)}] * len(texts)

#     def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
#         try:
#             if idx >= self.num_elements:
#                 return {"status": "error", "message": "Invalid index"}
#             vector = self.embed_text(text)
#             with self.lock:
#                 temp_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
#                 temp_index.hnsw.ef_construction = 200
#                 temp_index.hnsw.ef_search = 50
#                 all_vectors = self.index.reconstruct_n(0, self.num_elements)
#                 all_vectors[idx] = vector
#                 temp_index.add(all_vectors)
#                 self.index = temp_index
#                 random_meta = self._generate_random_metadata()
#                 final_meta = metadata or self.metadata.get(idx, {}).get("metadata", {})
#                 final_meta.update(random_meta)
#                 self.metadata[idx] = {"text": text, "metadata": final_meta}
#             self.logger.info(f"Updated item with ID: {idx}")
#             return {
#                 "status": "updated",
#                 "id": idx,
#                 "text": text,
#                 "metadata_key": final_meta["id"],
#                 "embedding": np.array2string(vector, separator=',')
#             }
#         except Exception as e:
#             self.logger.error(f"Update failed: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def delete(self, idx: int) -> Dict:
#         try:
#             with self.lock:
#                 if idx >= self.num_elements:
#                     return {"status": "error", "message": "Invalid index"}
#                 self.metadata.pop(idx, None)
#                 self.logger.info(f"Deleted item with ID: {idx}")
#                 return {"status": "deleted", "id": idx}
#         except Exception as e:
#             self.logger.error(f"Delete failed: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def _parse_query(self, query: str) -> Dict:
#         """Parse a single-line SQL-like query into a structured format."""
#         if not query:
#             return {"type": "match_all"}

#         def parse_condition(term: str) -> Dict:
#             term = term.strip()
#             if ":" in term:
#                 field, value = term.split(":", 1)
#                 # Check for operators: ==, >=, <=, !=, >, <
#                 operators = ["==", ">=", "<=", "!=", ">", "<"]
#                 op = "="
#                 for operator in operators:
#                     if value.startswith(operator):
#                         op = operator
#                         value = value[len(operator):]
#                         break
#                 # Handle quoted strings (e.g., category=="news")
#                 if value.startswith('"') and value.endswith('"'):
#                     value = value[1:-1]
#                 # Check for wildcard in text field
#                 if field == "text" and value.endswith("*"):
#                     return {
#                         "type": "contains",
#                         "field": "text",
#                         "value": value[:-1].lower()
#                     }
#                 # Check for range
#                 if "-" in value and op in ["=", "=="]:
#                     try:
#                         start, end = value.split("-")
#                         if field in ["score"]:
#                             return {
#                                 "type": "range",
#                                 "field": field,
#                                 "start": float(start),
#                                 "end": float(end),
#                                 "inclusive": True
#                             }
#                         else:  # String range (lexicographic)
#                             return {
#                                 "type": "range",
#                                 "field": field,
#                                 "start": start,
#                                 "end": end,
#                                 "inclusive": True
#                             }
#                     except ValueError:
#                         raise ValueError(f"Invalid range format in '{term}'")
#                 # Comparison operator
#                 try:
#                     if field in ["score"]:
#                         value = float(value)
#                     return {
#                         "type": "compare",
#                         "field": field,
#                         "operator": op,
#                         "value": value
#                     }
#                 except ValueError:
#                     return {
#                         "type": "compare",
#                         "field": field,
#                         "operator": op,
#                         "value": value
#                     }
#             else:  # Single-word query
#                 return {"type": "contains", "value": term.lower()}

#         # Split by && or %&& (AND)
#         and_pattern = re.compile(r'\s*(?:&&|%&&)\s*')
#         and_parts = and_pattern.split(query)
#         if len(and_parts) > 1:
#             return {
#                 "type": "and",
#                 "conditions": [self._parse_query(part.strip()) for part in and_parts]
#             }

#         # Split by || (OR)
#         or_parts = query.split("||")
#         if len(or_parts) > 1:
#             return {
#                 "type": "or",
#                 "conditions": [parse_condition(part.strip()) for part in or_parts]
#             }

#         return parse_condition(query)

#     def _evaluate_condition(self, metadata: Dict, text: str, condition: Dict) -> bool:
#         """Evaluate if metadata and/or text satisfies a query condition."""
#         if condition["type"] == "match_all":
#             return True
#         elif condition["type"] == "and":
#             return all(self._evaluate_condition(metadata, text, sub_cond) for sub_cond in condition["conditions"])
#         elif condition["type"] == "or":
#             return any(self._evaluate_condition(metadata, text, sub_cond) for sub_cond in condition["conditions"])
#         elif condition["type"] == "compare":
#             if condition["field"] == "text":
#                 value = text
#             else:
#                 if condition["field"] not in metadata:
#                     return False
#                 value = metadata[condition["field"]]
#             op = condition["operator"]
#             cond_value = condition["value"]
#             # Handle numeric comparisons
#             if isinstance(value, (int, float)) and isinstance(cond_value, (int, float)):
#                 if op in ["=", "=="]: return value == cond_value
#                 if op == ">": return value > cond_value
#                 if op == "<": return value < cond_value
#                 if op == ">=": return value >= cond_value
#                 if op == "<=": return value <= cond_value
#                 if op == "!=": return value != cond_value
#             # Handle string comparisons
#             else:
#                 value = str(value)
#                 cond_value = str(cond_value)
#                 if op in ["=", "=="]: return value == cond_value
#                 if op == "!=": return value != cond_value
#                 if op == ">": return value > cond_value
#                 if op == "<": return value < cond_value
#                 if op == ">=": return value >= cond_value
#                 if op == "<=": return value <= cond_value
#             return False
#         elif condition["type"] == "range":
#             if condition["field"] == "text":
#                 value = text
#             else:
#                 if condition["field"] not in metadata:
#                     return False
#                 value = metadata[condition["field"]]
#             if isinstance(value, (int, float)):
#                 return condition["start"] <= value <= condition["end"]
#             else:
#                 return condition["start"] <= str(value) <= condition["end"]
#         elif condition["type"] == "contains":
#             if condition.get("field") == "text":
#                 return condition["value"] in text.lower()
#             # Single-word query: search text and metadata
#             if condition["value"] in text.lower():
#                 return True
#             return any(
#                 condition["value"] in str(value).lower()
#                 for value in metadata.values()
#             )
#         return False

#     def find(self, query: str, top_k: int = 3, filter_query: Optional[str] = None) -> List[Dict]:
#         try:
#             parsed_filter = self._parse_query(filter_query) if filter_query else {"type": "match_all"}
#             query_vector = self.embed_text(query)
#             search_k = min(top_k * 2, self.num_elements)
#             distances, labels = self.index.search(np.array([query_vector], dtype=np.float32), search_k)
#             results = []
#             for label, dist in zip(labels[0], distances[0]):
#                 if len(results) >= top_k:
#                     break
#                 if label in self.metadata:
#                     meta = self.metadata[label]["metadata"]
#                     text = self.metadata[label]["text"]
#                     if self._evaluate_condition(meta, text, parsed_filter):
#                         vector = self.index.reconstruct(int(label))
#                         results.append({
#                             "id": int(label),
#                             "distance": float(dist),
#                             "text": text,
#                             "metadata_key": meta["id"],
#                             "embedding": np.array2string(vector, separator=',')
#                         })
#             self.logger.info(f"Found {len(results)} results for query with filter: {filter_query}")
#             return results
#         except Exception as e:
#             self.logger.error(f"Find failed: {str(e)}")
#             return [{"status": "error", "message": str(e)}]

#     def save(self) -> Dict:
#         try:
#             with self.lock:
#                 faiss.write_index(self.index, self.vector_file)
#                 with open(self.metadata_file, "wb") as f:
#                     pickle.dump(self.metadata, f)
#             self.logger.info("Saved index and metadata")
#             return {"status": "saved"}
#         except Exception as e:
#             self.logger.error(f"Save failed: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def load(self) -> Dict:
#         try:
#             if not os.path.exists(self.vector_file):
#                 return {"status": "error", "message": "Index file not found"}
#             with self.lock:
#                 self.index = faiss.read_index(self.vector_file)
#                 self.index.hnsw.ef_search = 50
#                 with open(self.metadata_file, "rb") as f:
#                     self.metadata = pickle.load(f)
#                 self.num_elements = self.index.ntotal
#             self.logger.info("Loaded index and metadata")
#             return {"status": "loaded"}
#         except Exception as e:
#             self.logger.error(f"Load failed: {str(e)}")
#             return {"status": "error", "message": str(e)}

#     def get_stats(self) -> Dict:
#         return {
#             "num_elements": self.num_elements,
#             "max_elements": self.max_elements,
#             "cache_size": len(self.embedding_cache),
#             "memory_usage_mb": (self.num_elements * self.vector_dim * 4) / 1e6
#         }

# # import faiss
# # import numpy as np
# # from sentence_transformers import SentenceTransformer
# # from typing import List, Dict, Optional
# # import threading
# # import logging
# # import os
# # import pickle
# # import psutil
# # import uuid
# # import random
# # import string

# # class VowDB:
# #     """A high-performance synchronous vector database for similarity search using Faiss."""
    
# #     def __init__(
# #         self,
# #         model_name: str = "all-MiniLM-L6-v2",
# #         file_path: str = "vectors.faiss",
# #         max_elements: int = 100000,
# #         cache_size: int = 1000
# #     ):
# #         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# #         self.logger = logging.getLogger(__name__)
# #         self.embedding_model = SentenceTransformer(model_name)
# #         self.vector_dim = self.embedding_model.get_sentence_embedding_dimension()
# #         self.logger.info(f"Initialized embedding model: {model_name}, dimension: {self.vector_dim}")
# #         self.max_elements = max_elements
# #         self._validate_memory()
# #         self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)
# #         self.index.hnsw.ef_construction = 200
# #         self.index.hnsw.ef_search = 50
# #         self.num_elements = 0
# #         self.logger.info(f"Initialized Faiss HNSW index with max_elements: {max_elements}")
# #         self.vector_file = file_path
# #         self.metadata_file = file_path + ".meta"
# #         self.metadata = {}
# #         self.lock = threading.Lock()
# #         self.embedding_cache = {}
# #         self.cache_size = cache_size

# #     def _validate_memory(self):
# #         vector_size = self.vector_dim * 4
# #         index_size = self.max_elements * vector_size
# #         available_memory = psutil.virtual_memory().available
# #         if index_size > available_memory * 0.8:
# #             self.logger.warning(
# #                 f"Index size ({index_size / 1e6:.2f} MB) may exceed available memory "
# #                 f"({available_memory / 1e6:.2f} MB)"
# #             )
# #             raise ValueError("Insufficient memory for requested max_elements")

# #     def _generate_random_metadata(self) -> Dict:
# #         """Generate random metadata for testing."""
# #         return {
# #             "id": str(uuid.uuid4()),
# #             "category": ''.join(random.choices(string.ascii_lowercase, k=8)),
# #             "score": random.uniform(0, 1)
# #         }

# #     def embed_text(self, text: str) -> np.ndarray:
# #         if text in self.embedding_cache:
# #             return self.embedding_cache[text]
# #         vector = self.embedding_model.encode([text])[0]
# #         if len(self.embedding_cache) < self.cache_size:
# #             self.embedding_cache[text] = vector
# #         return vector

# #     def embed_texts(self, texts: List[str]) -> np.ndarray:
# #         vectors = []
# #         uncached_texts = []
# #         uncached_indices = []
# #         for i, text in enumerate(texts):
# #             if text in self.embedding_cache:
# #                 vectors.append(self.embedding_cache[text])
# #             else:
# #                 uncached_texts.append(text)
# #                 uncached_indices.append(i)
# #         if uncached_texts:
# #             new_vectors = self.embedding_model.encode(uncached_texts)
# #             for text, vector, idx in zip(uncached_texts, new_vectors, uncached_indices):
# #                 vectors.insert(idx, vector)
# #                 if len(self.embedding_cache) < self.cache_size:
# #                     self.embedding_cache[text] = vector
# #         return np.array(vectors)

# #     def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
# #         try:
# #             vector = self.embed_text(text)
# #             with self.lock:
# #                 if self.num_elements >= self.max_elements:
# #                     return {"status": "error", "message": "Index full"}
# #                 idx = self.num_elements
# #                 self.index.add(np.array([vector], dtype=np.float32))
# #                 random_meta = self._generate_random_metadata()
# #                 final_meta = metadata or {}
# #                 final_meta.update(random_meta)
# #                 self.metadata[idx] = {"text": text, "metadata": final_meta}
# #                 self.num_elements += 1
# #             self.logger.info(f"Inserted item with ID: {idx}")
# #             return {
# #                 "status": "inserted",
# #                 "id": idx,
# #                 "text": text,
# #                 "metadata_key": final_meta["id"],
# #                 "embedding": np.array2string(vector, separator=',')
# #             }
# #         except Exception as e:
# #             self.logger.error(f"Insert failed: {str(e)}")
# #             return {"status": "error", "message": str(e)}

# #     def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
# #         try:
# #             vectors = self.embed_texts(texts)
# #             metadatas = metadatas or [{}] * len(texts)
# #             with self.lock:
# #                 start_idx = self.num_elements
# #                 if start_idx + len(texts) > self.max_elements:
# #                     return [{"status": "error", "message": "Index full"}] * len(texts)
# #                 idxs = list(range(start_idx, start_idx + len(texts)))
# #                 self.index.add(vectors.astype(np.float32))
# #                 results = []
# #                 for idx, text, metadata, vector in zip(idxs, texts, metadatas, vectors):
# #                     random_meta = self._generate_random_metadata()
# #                     final_meta = metadata.copy()
# #                     final_meta.update(random_meta)
# #                     self.metadata[idx] = {"text": text, "metadata": final_meta}
# #                     results.append({
# #                         "status": "inserted",
# #                         "id": idx,
# #                         "text": text,
# #                         "metadata_key": final_meta["id"],
# #                         "embedding": np.array2string(vector, separator=',')
# #                     })
# #                 self.num_elements += len(texts)
# #             self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
# #             return results
# #         except Exception as e:
# #             self.logger.error(f"Batch insert failed: {str(e)}")
# #             return [{"status": "error", "message": str(e)}] * len(texts)

# #     def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
# #         try:
# #             if idx >= self.num_elements:
# #                 return {"status": "error", "message": "Invalid index"}
# #             vector = self.embed_text(text)
# #             with self.lock:
# #                 temp_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
# #                 temp_index.hnsw.ef_construction = 200
# #                 temp_index.hnsw.ef_search = 50
# #                 all_vectors = self.index.reconstruct_n(0, self.num_elements)
# #                 all_vectors[idx] = vector
# #                 temp_index.add(all_vectors)
# #                 self.index = temp_index
# #                 random_meta = self._generate_random_metadata()
# #                 final_meta = metadata or self.metadata.get(idx, {}).get("metadata", {})
# #                 final_meta.update(random_meta)
# #                 self.metadata[idx] = {"text": text, "metadata": final_meta}
# #             self.logger.info(f"Updated item with ID: {idx}")
# #             return {
# #                 "status": "updated",
# #                 "id": idx,
# #                 "text": text,
# #                 "metadata_key": final_meta["id"],
# #                 "embedding": np.array2string(vector, separator=',')
# #             }
# #         except Exception as e:
# #             self.logger.error(f"Update failed: {str(e)}")
# #             return {"status": "error", "message": str(e)}

# #     def delete(self, idx: int) -> Dict:
# #         try:
# #             with self.lock:
# #                 if idx >= self.num_elements:
# #                     return {"status": "error", "message": "Invalid index"}
# #                 self.metadata.pop(idx, None)
# #                 self.logger.info(f"Deleted item with ID: {idx}")
# #                 return {"status": "deleted", "id": idx}
# #         except Exception as e:
# #             self.logger.error(f"Delete failed: {str(e)}")
# #             return {"status": "error", "message": str(e)}

# #     def find(self, query: str, top_k: int = 3) -> List[Dict]:
# #         try:
# #             query_vector = self.embed_text(query)
# #             distances, labels = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
# #             results = []
# #             for label, dist in zip(labels[0], distances[0]):
# #                 if label in self.metadata:
# #                     meta = self.metadata[label]["metadata"]
# #                     text = self.metadata[label]["text"]
# #                     vector = self.index.reconstruct(int(label))
# #                     results.append({
# #                         "id": int(label),
# #                         "distance": float(dist),
# #                         "text": text,
# #                         "metadata_key": meta["id"],
# #                         "embedding": np.array2string(vector, separator=',')
# #                     })
# #             self.logger.info(f"Found {len(results)} results for query")
# #             return results
# #         except Exception as e:
# #             self.logger.error(f"Find failed: {str(e)}")
# #             return [{"status": "error", "message": str(e)}]

# #     def save(self) -> Dict:
# #         try:
# #             with self.lock:
# #                 faiss.write_index(self.index, self.vector_file)
# #                 with open(self.metadata_file, "wb") as f:
# #                     pickle.dump(self.metadata, f)
# #             self.logger.info("Saved index and metadata")
# #             return {"status": "saved"}
# #         except Exception as e:
# #             self.logger.error(f"Save failed: {str(e)}")
# #             return {"status": "error", "message": str(e)}

# #     def load(self) -> Dict:
# #         try:
# #             if not os.path.exists(self.vector_file):
# #                 return {"status": "error", "message": "Index file not found"}
# #             with self.lock:
# #                 self.index = faiss.read_index(self.vector_file)
# #                 self.index.hnsw.ef_search = 50
# #                 with open(self.metadata_file, "rb") as f:
# #                     self.metadata = pickle.load(f)
# #                 self.num_elements = self.index.ntotal
# #             self.logger.info("Loaded index and metadata")
# #             return {"status": "loaded"}
# #         except Exception as e:
# #             self.logger.error(f"Load failed: {str(e)}")
# #             return {"status": "error", "message": str(e)}

# #     def get_stats(self) -> Dict:
# #         return {
# #             "num_elements": self.num_elements,
# #             "max_elements": self.max_elements,
# #             "cache_size": len(self.embedding_cache),
# #             "memory_usage_mb": (self.num_elements * self.vector_dim * 4) / 1e6
# #         }
        

# # # import faiss
# # # import numpy as np
# # # from sentence_transformers import SentenceTransformer
# # # from typing import List, Dict, Optional
# # # import threading
# # # import logging
# # # import os
# # # import pickle
# # # import psutil
# # # import uuid
# # # import random
# # # import string

# # # class VowDB:
# # #     """A high-performance synchronous vector database for similarity search using Faiss."""
    
# # #     def __init__(
# # #         self,
# # #         model_name: str = "all-MiniLM-L6-v2",
# # #         file_path: str = "vectors.faiss",
# # #         max_elements: int = 100000,
# # #         cache_size: int = 1000
# # #     ):
# # #         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# # #         self.logger = logging.getLogger(__name__)
# # #         self.embedding_model = SentenceTransformer(model_name)
# # #         self.vector_dim = self.embedding_model.get_sentence_embedding_dimension()
# # #         self.logger.info(f"Initialized embedding model: {model_name}, dimension: {self.vector_dim}")
# # #         self.max_elements = max_elements
# # #         self._validate_memory()
# # #         self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)
# # #         self.index.hnsw.ef_construction = 200
# # #         self.index.hnsw.ef_search = 50
# # #         self.num_elements = 0
# # #         self.logger.info(f"Initialized Faiss HNSW index with max_elements: {max_elements}")
# # #         self.vector_file = file_path
# # #         self.metadata_file = file_path + ".meta"
# # #         self.metadata = {}
# # #         self.lock = threading.Lock()
# # #         self.embedding_cache = {}
# # #         self.cache_size = cache_size

# # #     def _validate_memory(self):
# # #         vector_size = self.vector_dim * 4
# # #         index_size = self.max_elements * vector_size
# # #         available_memory = psutil.virtual_memory().available
# # #         if index_size > available_memory * 0.8:
# # #             self.logger.warning(
# # #                 f"Index size ({index_size / 1e6:.2f} MB) may exceed available memory "
# # #                 f"({available_memory / 1e6:.2f} MB)"
# # #             )
# # #             raise ValueError("Insufficient memory for requested max_elements")

# # #     def _generate_random_metadata(self) -> Dict:
# # #         """Generate random metadata for testing."""
# # #         return {
# # #             "id": str(uuid.uuid4()),
# # #             "category": ''.join(random.choices(string.ascii_lowercase, k=8)),
# # #             "score": random.uniform(0, 1)
# # #         }

# # #     def embed_text(self, text: str) -> np.ndarray:
# # #         if text in self.embedding_cache:
# # #             return self.embedding_cache[text]
# # #         vector = self.embedding_model.encode([text])[0]
# # #         if len(self.embedding_cache) < self.cache_size:
# # #             self.embedding_cache[text] = vector
# # #         return vector

# # #     def embed_texts(self, texts: List[str]) -> np.ndarray:
# # #         vectors = []
# # #         uncached_texts = []
# # #         uncached_indices = []
# # #         for i, text in enumerate(texts):
# # #             if text in self.embedding_cache:
# # #                 vectors.append(self.embedding_cache[text])
# # #             else:
# # #                 uncached_texts.append(text)
# # #                 uncached_indices.append(i)
# # #         if uncached_texts:
# # #             new_vectors = self.embedding_model.encode(uncached_texts)
# # #             for text, vector, idx in zip(uncached_texts, new_vectors, uncached_indices):
# # #                 vectors.insert(idx, vector)
# # #                 if len(self.embedding_cache) < self.cache_size:
# # #                     self.embedding_cache[text] = vector
# # #         return np.array(vectors)

# # #     def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
# # #         try:
# # #             vector = self.embed_text(text)
# # #             with self.lock:
# # #                 if self.num_elements >= self.max_elements:
# # #                     return {"status": "error", "message": "Index full"}
# # #                 idx = self.num_elements
# # #                 self.index.add(np.array([vector], dtype=np.float32))
# # #                 random_meta = self._generate_random_metadata()
# # #                 final_meta = metadata or {}
# # #                 final_meta.update(random_meta)
# # #                 self.metadata[idx] = {"text": text, "metadata": final_meta}
# # #                 self.num_elements += 1
# # #             self.logger.info(f"Inserted item with ID: {idx}")
# # #             return {
# # #                 "status": "inserted",
# # #                 "id": idx,
# # #                 "metadata_key": final_meta["id"],
# # #                 "embedding": np.array2string(vector, separator=',')
# # #             }
# # #         except Exception as e:
# # #             self.logger.error(f"Insert failed: {str(e)}")
# # #             return {"status": "error", "message": str(e)}

# # #     def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
# # #         try:
# # #             vectors = self.embed_texts(texts)
# # #             metadatas = metadatas or [{}] * len(texts)
# # #             with self.lock:
# # #                 start_idx = self.num_elements
# # #                 if start_idx + len(texts) > self.max_elements:
# # #                     return [{"status": "error", "message": "Index full"}] * len(texts)
# # #                 idxs = list(range(start_idx, start_idx + len(texts)))
# # #                 self.index.add(vectors.astype(np.float32))
# # #                 results = []
# # #                 for idx, text, metadata, vector in zip(idxs, texts, metadatas, vectors):
# # #                     random_meta = self._generate_random_metadata()
# # #                     final_meta = metadata.copy()
# # #                     final_meta.update(random_meta)
# # #                     self.metadata[idx] = {"text": text, "metadata": final_meta}
# # #                     results.append({
# # #                         "status": "inserted",
# # #                         "id": idx,
# # #                         "metadata_key": final_meta["id"],
# # #                         "embedding": np.array2string(vector, separator=',')
# # #                     })
# # #                 self.num_elements += len(texts)
# # #             self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
# # #             return results
# # #         except Exception as e:
# # #             self.logger.error(f"Batch insert failed: {str(e)}")
# # #             return [{"status": "error", "message": str(e)}] * len(texts)

# # #     def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
# # #         try:
# # #             if idx >= self.num_elements:
# # #                 return {"status": "error", "message": "Invalid index"}
# # #             vector = self.embed_text(text)
# # #             with self.lock:
# # #                 temp_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
# # #                 temp_index.hnsw.ef_construction = 200
# # #                 temp_index.hnsw.ef_search = 50
# # #                 all_vectors = self.index.reconstruct_n(0, self.num_elements)
# # #                 all_vectors[idx] = vector
# # #                 temp_index.add(all_vectors)
# # #                 self.index = temp_index
# # #                 random_meta = self._generate_random_metadata()
# # #                 final_meta = metadata or self.metadata.get(idx, {}).get("metadata", {})
# # #                 final_meta.update(random_meta)
# # #                 self.metadata[idx] = {"text": text, "metadata": final_meta}
# # #             self.logger.info(f"Updated item with ID: {idx}")
# # #             return {
# # #                 "status": "updated",
# # #                 "id": idx,
# # #                 "metadata_key": final_meta["id"],
# # #                 "embedding": np.array2string(vector, separator=',')
# # #             }
# # #         except Exception as e:
# # #             self.logger.error(f"Update failed: {str(e)}")
# # #             return {"status": "error", "message": str(e)}

# # #     def delete(self, idx: int) -> Dict:
# # #         try:
# # #             with self.lock:
# # #                 if idx >= self.num_elements:
# # #                     return {"status": "error", "message": "Invalid index"}
# # #                 self.metadata.pop(idx, None)
# # #                 self.logger.info(f"Deleted item with ID: {idx}")
# # #                 return {"status": "deleted", "id": idx}
# # #         except Exception as e:
# # #             self.logger.error(f"Delete failed: {str(e)}")
# # #             return {"status": "error", "message": str(e)}

# # #     def find(self, query: str, top_k: int = 3) -> List[Dict]:
# # #         try:
# # #             query_vector = self.embed_text(query)
# # #             distances, labels = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
# # #             results = []
# # #             for label, dist in zip(labels[0], distances[0]):
# # #                 if label in self.metadata:
# # #                     meta = self.metadata[label]["metadata"]
# # #                     vector = self.index.reconstruct(int(label))
# # #                     results.append({
# # #                         "id": int(label),
# # #                         "distance": float(dist),
# # #                         "metadata_key": meta["id"],
# # #                         "embedding": np.array2string(vector, separator=',')
# # #                     })
# # #             self.logger.info(f"Found {len(results)} results for query")
# # #             return results
# # #         except Exception as e:
# # #             self.logger.error(f"Find failed: {str(e)}")
# # #             return [{"status": "error", "message": str(e)}]

# # #     def save(self) -> Dict:
# # #         try:
# # #             with self.lock:
# # #                 faiss.write_index(self.index, self.vector_file)
# # #                 with open(self.metadata_file, "wb") as f:
# # #                     pickle.dump(self.metadata, f)
# # #             self.logger.info("Saved index and metadata")
# # #             return {"status": "saved"}
# # #         except Exception as e:
# # #             self.logger.error(f"Save failed: {str(e)}")
# # #             return {"status": "error", "message": str(e)}

# # #     def load(self) -> Dict:
# # #         try:
# # #             if not os.path.exists(self.vector_file):
# # #                 return {"status": "error", "message": "Index file not found"}
# # #             with self.lock:
# # #                 self.index = faiss.read_index(self.vector_file)
# # #                 self.index.hnsw.ef_search = 50
# # #                 with open(self.metadata_file, "rb") as f:
# # #                     self.metadata = pickle.load(f)
# # #                 self.num_elements = self.index.ntotal
# # #             self.logger.info("Loaded index and metadata")
# # #             return {"status": "loaded"}
# # #         except Exception as e:
# # #             self.logger.error(f"Load failed: {str(e)}")
# # #             return {"status": "error", "message": str(e)}

# # #     def get_stats(self) -> Dict:
# # #         return {
# # #             "num_elements": self.num_elements,
# # #             "max_elements": self.max_elements,
# # #             "cache_size": len(self.embedding_cache),
# # #             "memory_usage_mb": (self.num_elements * self.vector_dim * 4) / 1e6
# # #         }

# # # # import faiss
# # # # import numpy as np
# # # # from sentence_transformers import SentenceTransformer
# # # # from typing import List, Dict, Optional
# # # # import threading
# # # # import logging
# # # # import os
# # # # import pickle
# # # # import psutil

# # # # class VowDB:
# # # #     """A high-performance synchronous vector database for similarity search using Faiss."""
    
# # # #     def __init__(
# # # #         self,
# # # #         model_name: str = "all-MiniLM-L6-v2",
# # # #         file_path: str = "vectors.faiss",
# # # #         max_elements: int = 100000,
# # # #         cache_size: int = 1000
# # # #     ):
# # # #         """
# # # #         Initialize the vector database with synchronous operations.
        
# # # #         Args:
# # # #             model_name (str): Sentence transformer model name (default: 'all-MiniLM-L6-v2').
# # # #             file_path (str): Path to store the vector index (default: 'vectors.faiss').
# # # #             max_elements (int): Maximum number of vectors in the index (default: 100000).
# # # #             cache_size (int): Maximum number of cached embeddings (default: 1000).
# # # #         """
# # # #         # Setup logging
# # # #         logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# # # #         self.logger = logging.getLogger(__name__)

# # # #         # Initialize embedding model
# # # #         self.embedding_model = SentenceTransformer(model_name)
# # # #         self.vector_dim = self.embedding_model.get_sentence_embedding_dimension()
# # # #         self.logger.info(f"Initialized embedding model: {model_name}, dimension: {self.vector_dim}")

# # # #         # Validate memory availability
# # # #         self.max_elements = max_elements
# # # #         self._validate_memory()

# # # #         # Initialize Faiss HNSW index
# # # #         self.index = faiss.IndexHNSWFlat(self.vector_dim, 16)  # M=16, similar to hnswlib
# # # #         self.index.hnsw.ef_construction = 200
# # # #         self.index.hnsw.ef_search = 50
# # # #         self.num_elements = 0  # Track number of elements manually
# # # #         self.logger.info(f"Initialized Faiss HNSW index with max_elements: {max_elements}")

# # # #         # Persistence
# # # #         self.vector_file = file_path
# # # #         self.metadata_file = file_path + ".meta"
# # # #         self.metadata = {}  # Store text or metadata for each ID

# # # #         # Thread safety
# # # #         self.lock = threading.Lock()

# # # #         # Embedding cache
# # # #         self.embedding_cache = {}
# # # #         self.cache_size = cache_size

# # # #     def _validate_memory(self):
# # # #         """Validate that the system has enough memory for the index."""
# # # #         vector_size = self.vector_dim * 4  # 4 bytes per float
# # # #         index_size = self.max_elements * vector_size
# # # #         available_memory = psutil.virtual_memory().available
# # # #         if index_size > available_memory * 0.8:  # Use up to 80% of available memory
# # # #             self.logger.warning(
# # # #                 f"Index size ({index_size / 1e6:.2f} MB) may exceed available memory "
# # # #                 f"({available_memory / 1e6:.2f} MB)"
# # # #             )
# # # #             raise ValueError("Insufficient memory for requested max_elements")

# # # #     def embed_text(self, text: str) -> np.ndarray:
# # # #         """Convert text to vector with caching."""
# # # #         if text in self.embedding_cache:
# # # #             return self.embedding_cache[text]
# # # #         vector = self.embedding_model.encode([text])[0]
# # # #         if len(self.embedding_cache) < self.cache_size:
# # # #             self.embedding_cache[text] = vector
# # # #         return vector

# # # #     def embed_texts(self, texts: List[str]) -> np.ndarray:
# # # #         """Convert multiple texts to vectors with caching."""
# # # #         vectors = []
# # # #         uncached_texts = []
# # # #         uncached_indices = []
# # # #         for i, text in enumerate(texts):
# # # #             if text in self.embedding_cache:
# # # #                 vectors.append(self.embedding_cache[text])
# # # #             else:
# # # #                 uncached_texts.append(text)
# # # #                 uncached_indices.append(i)
# # # #         if uncached_texts:
# # # #             new_vectors = self.embedding_model.encode(uncached_texts)
# # # #             for text, vector, idx in zip(uncached_texts, new_vectors, uncached_indices):
# # # #                 vectors.insert(idx, vector)
# # # #                 if len(self.embedding_cache) < self.cache_size:
# # # #                     self.embedding_cache[text] = vector
# # # #         return np.array(vectors)

# # # #     def insert(self, text: str, metadata: Optional[Dict] = None) -> Dict:
# # # #         """Insert a single text synchronously."""
# # # #         try:
# # # #             vector = self.embed_text(text)
# # # #             with self.lock:
# # # #                 if self.num_elements >= self.max_elements:
# # # #                     return {"status": "error", "message": "Index full"}
# # # #                 idx = self.num_elements
# # # #                 self.index.add(np.array([vector], dtype=np.float32))
# # # #                 self.metadata[idx] = {"text": text, "metadata": metadata or {}}
# # # #                 self.num_elements += 1
# # # #             self.logger.info(f"Inserted item with ID: {idx}")
# # # #             return {"status": "inserted", "id": idx}
# # # #         except Exception as e:
# # # #             self.logger.error(f"Insert failed: {str(e)}")
# # # #             return {"status": "error", "message": str(e)}

# # # #     def insert_batch(self, texts: List[str], metadatas: Optional[List[Dict]] = None) -> List[Dict]:
# # # #         """Insert multiple texts synchronously."""
# # # #         try:
# # # #             vectors = self.embed_texts(texts)
# # # #             metadatas = metadatas or [{}] * len(texts)
# # # #             with self.lock:
# # # #                 start_idx = self.num_elements
# # # #                 if start_idx + len(texts) > self.max_elements:
# # # #                     return [{"status": "error", "message": "Index full"}] * len(texts)
# # # #                 idxs = list(range(start_idx, start_idx + len(texts)))
# # # #                 self.index.add(vectors.astype(np.float32))
# # # #                 for idx, text, metadata in zip(idxs, texts, metadatas):
# # # #                     self.metadata[idx] = {"text": text, "metadata": metadata}
# # # #                 self.num_elements += len(texts)
# # # #             self.logger.info(f"Inserted {len(texts)} items starting at ID: {start_idx}")
# # # #             return [{"status": "inserted", "id": idx} for idx in idxs]
# # # #         except Exception as e:
# # # #             self.logger.error(f"Batch insert failed: {str(e)}")
# # # #             return [{"status": "error", "message": str(e)}] * len(texts)

# # # #     def update(self, idx: int, text: str, metadata: Optional[Dict] = None) -> Dict:
# # # #         """Update a vector synchronously."""
# # # #         try:
# # # #             if idx >= self.num_elements:
# # # #                 return {"status": "error", "message": "Invalid index"}
# # # #             vector = self.embed_text(text)
# # # #             with self.lock:
# # # #                 # Faiss doesn't support direct update, so we rebuild a temporary index
# # # #                 temp_index = faiss.IndexHNSWFlat(self.vector_dim, 16)
# # # #                 temp_index.hnsw.ef_construction = 200
# # # #                 temp_index.hnsw.ef_search = 50
# # # #                 all_vectors = self.index.reconstruct_n(0, self.num_elements)
# # # #                 all_vectors[idx] = vector
# # # #                 temp_index.add(all_vectors)
# # # #                 self.index = temp_index
# # # #                 self.metadata[idx] = {"text": text, "metadata": metadata or self.metadata.get(idx, {}).get("metadata", {})}
# # # #             self.logger.info(f"Updated item with ID: {idx}")
# # # #             return {"status": "updated", "id": idx}
# # # #         except Exception as e:
# # # #             self.logger.error(f"Update failed: {str(e)}")
# # # #             return {"status": "error", "message": str(e)}

# # # #     def delete(self, idx: int) -> Dict:
# # # #         """Delete a vector synchronously (marks as deleted in metadata)."""
# # # #         try:
# # # #             with self.lock:
# # # #                 if idx >= self.num_elements:
# # # #                     return {"status": "error", "message": "Invalid index"}
# # # #                 self.metadata.pop(idx, None)
# # # #                 # Faiss doesn't support direct deletion, so we track deleted IDs
# # # #                 self.logger.info(f"Deleted item with ID: {idx}")
# # # #                 return {"status": "deleted", "id": idx}
# # # #         except Exception as e:
# # # #             self.logger.error(f"Delete failed: {str(e)}")
# # # #             return {"status": "error", "message": str(e)}

# # # #     def find(self, query: str, top_k: int = 3) -> List[Dict]:
# # # #         """Find top_k closest vectors synchronously."""
# # # #         try:
# # # #             query_vector = self.embed_text(query)
# # # #             distances, labels = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
# # # #             results = [
# # # #                 {"id": int(label), "distance": float(dist), "text": self.metadata.get(label, {}).get("text", ""),
# # # #                  "metadata": self.metadata.get(label, {}).get("metadata", {})}
# # # #                 for label, dist in zip(labels[0], distances[0]) if label in self.metadata
# # # #             ]
# # # #             self.logger.info(f"Found {len(results)} results for query")
# # # #             return results
# # # #         except Exception as e:
# # # #             self.logger.error(f"Find failed: {str(e)}")
# # # #             return [{"status": "error", "message": str(e)}]

# # # #     def save(self) -> Dict:
# # # #         """Save the index and metadata to disk synchronously."""
# # # #         try:
# # # #             with self.lock:
# # # #                 faiss.write_index(self.index, self.vector_file)
# # # #                 with open(self.metadata_file, "wb") as f:
# # # #                     pickle.dump(self.metadata, f)
# # # #             self.logger.info("Saved index and metadata")
# # # #             return {"status": "saved"}
# # # #         except Exception as e:
# # # #             self.logger.error(f"Save failed: {str(e)}")
# # # #             return {"status": "error", "message": str(e)}

# # # #     def load(self) -> Dict:
# # # #         """Load the index and metadata from disk synchronously."""
# # # #         try:
# # # #             if not os.path.exists(self.vector_file):
# # # #                 return {"status": "error", "message": "Index file not found"}
# # # #             with self.lock:
# # # #                 self.index = faiss.read_index(self.vector_file)
# # # #                 self.index.hnsw.ef_search = 50
# # # #                 with open(self.metadata_file, "rb") as f:
# # # #                     self.metadata = pickle.load(f)
# # # #                 self.num_elements = self.index.ntotal
# # # #             self.logger.info("Loaded index and metadata")
# # # #             return {"status": "loaded"}
# # # #         except Exception as e:
# # # #             self.logger.error(f"Load failed: {str(e)}")
# # # #             return {"status": "error", "message": str(e)}

# # # #     def get_stats(self) -> Dict:
# # # #         """Return database statistics synchronously."""
# # # #         return {
# # # #             "num_elements": self.num_elements,
# # # #             "max_elements": self.max_elements,
# # # #             "cache_size": len(self.embedding_cache),
# # # #             "memory_usage_mb": (self.num_elements * self.vector_dim * 4) / 1e6
# # # #         }