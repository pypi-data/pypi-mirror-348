import unittest
import numpy as np
from VowDB import VowDB

class TestVowDB(unittest.TestCase):
    def setUp(self):
        self.db = VowDB(max_elements=100, file_path="test_vectors.faiss")
    
    def test_insert_and_find(self):
        result = self.db.insert("test text", {"category": "test"})
        self.assertEqual(result["status"], "inserted")
        self.assertEqual(result["text"], "test text")
        self.assertIn("metadata_key", result)
        self.assertIn("embedding", result)
        self.assertTrue(len(result["metadata_key"]) > 0)
        self.assertTrue(len(result["embedding"]) > 0)
        
        results = self.db.find("test", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "test text")
        self.assertIn("metadata_key", results[0])
        self.assertIn("embedding", results[0])
        self.assertEqual(results[0]["metadata_key"], result["metadata_key"])
    
    def test_batch_insert(self):
        texts = ["text1", "text2"]
        metadatas = [{"id": 1}, {"id": 2}]
        results = self.db.insert_batch(texts, metadatas)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["status"], "inserted")
        self.assertEqual(results[0]["text"], "text1")
        self.assertIn("metadata_key", results[0])
        self.assertIn("embedding", results[0])
        
        query_results = self.db.find("text1", top_k=2)
        self.assertEqual(len(query_results), 2)
        self.assertEqual(query_results[0]["text"], "text1")
        self.assertIn("metadata_key", query_results[0])
    
    def test_save_load(self):
        result = self.db.insert("save test")
        self.db.save()
        new_db = VowDB(max_elements=100, file_path="test_vectors.faiss")
        new_db.load()
        results = new_db.find("save", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "save test")
        self.assertIn("metadata_key", results[0])
        self.assertIn("embedding", results[0])

if __name__ == "__main__":
    unittest.main()

# import unittest
# import numpy as np
# from VowDB import VowDB

# class TestVowDB(unittest.TestCase):
#     def setUp(self):
#         self.db = VowDB(max_elements=100, file_path="test_vectors.faiss")
    
#     def test_insert_and_find(self):
#         result = self.db.insert("test text", {"category": "test"})
#         self.assertEqual(result["status"], "inserted")
#         self.assertIn("metadata_key", result)
#         self.assertIn("embedding", result)
#         self.assertTrue(len(result["metadata_key"]) > 0)
#         self.assertTrue(len(result["embedding"]) > 0)
        
#         results = self.db.find("test", top_k=1)
#         self.assertEqual(len(results), 1)
#         self.assertIn("metadata_key", results[0])
#         self.assertIn("embedding", results[0])
#         self.assertEqual(results[0]["metadata_key"], result["metadata_key"])
    
#     def test_batch_insert(self):
#         texts = ["text1", "text2"]
#         metadatas = [{"id": 1}, {"id": 2}]
#         results = self.db.insert_batch(texts, metadatas)
#         self.assertEqual(len(results), 2)
#         self.assertEqual(results[0]["status"], "inserted")
#         self.assertIn("metadata_key", results[0])
#         self.assertIn("embedding", results[0])
        
#         query_results = self.db.find("text1", top_k=2)
#         self.assertEqual(len(query_results), 2)
#         self.assertIn("metadata_key", query_results[0])
    
#     def test_save_load(self):
#         result = self.db.insert("save test")
#         self.db.save()
#         new_db = VowDB(max_elements=100, file_path="test_vectors.faiss")
#         new_db.load()
#         results = new_db.find("save", top_k=1)
#         self.assertEqual(len(results), 1)
#         self.assertIn("metadata_key", results[0])
#         self.assertIn("embedding", results[0])

# if __name__ == "__main__":
#     unittest.main()
# # import unittest
# # from vowdb import VowDB

# # class TestVowDB(unittest.TestCase):
# #     def setUp(self):
# #         self.db = VowDB(max_elements=100, file_path="test_vectors.faiss")
    
# #     def test_insert_and_find(self):
# #         self.db.insert("test text", {"category": "test"})
# #         results = self.db.find("test", top_k=1)
# #         self.assertEqual(len(results), 1)
# #         self.assertEqual(results[0]["text"], "test text")
# #         self.assertEqual(results[0]["metadata"]["category"], "test")
    
# #     def test_batch_insert(self):
# #         texts = ["text1", "text2"]
# #         metadatas = [{"id": 1}, {"id": 2}]
# #         results = self.db.insert_batch(texts, metadatas)
# #         self.assertEqual(len(results), 2)
# #         self.assertEqual(results[0]["status"], "inserted")
# #         query_results = self.db.find("text1", top_k=2)
# #         self.assertEqual(len(query_results), 2)
    
# #     def test_save_load(self):
# #         self.db.insert("save test")
# #         self.db.save()
# #         new_db = VowDB(max_elements=100, file_path="test_vectors.faiss")
# #         new_db.load()
# #         results = new_db.find("save", top_k=1)
# #         self.assertEqual(len(results), 1)
# #         self.assertEqual(results[0]["text"], "save test")

# # if __name__ == "__main__":
# #     unittest.main()