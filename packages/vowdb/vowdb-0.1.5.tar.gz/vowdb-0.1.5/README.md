# VowDB 🔥  
Blazing-fast vector database for text similarity. Powered by Faiss & Sentence Transformers.

---

## Install 💻  
Grab it with pip:

**pip install vowdb**

> Requires Python 3.8+, faiss-cpu, sentence-transformers, numpy, psutil.

---

## Setup 🚀  
Kick it off:

**from vowdb import VowDB**  
**db = VowDB(model_name="all-MiniLM-L6-v2", file_path="vectors.faiss")**

> Ready in ~1.2s.

---

## Add Data 📝  
Drop in texts:

**# One**  
**db.insert("Hello World", metadata={"greeting": "yes"})**  
**# ~0.57s**

**# Many**  
**texts = ["Hii", "I Am Rushikesh Sunil Kotkar!", "News article"]**  
**metadatas = [{"greeting": "yes"}, {"category": "introduction"}, {"greeting": "no"}]**  
**db.insert_batch(texts, metadatas)**

---

## Search 🔍  
Find stuff with `=` style filters. Check these dope examples.

### 1. AND Power  
**db.find("hello", top_k=3, filter_query="category=news && score>0.9 && greeting=yes")**

_Result:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}

---

### 2. Text Vibe  
**db.find("hello", top_k=3)**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=Hii, dist=0.48, meta={category=greeting, score=0.6, greeting=yes}

---

### 3. Exact Match  
**db.find("Hello World", top_k=3, filter_query="text=Hello World")**

_Result:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}

---

### 4. Prefix Hunt  
**db.find("Hel", top_k=3, filter_query="text=Hel*")**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=Hii, dist=0.48, meta={category=greeting, score=0.6, greeting=yes}

---

### 5. Category Snap  
**db.find("news", top_k=3, filter_query="category=news")**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=News article, dist=0.50, meta={category=news, score=0.7, greeting=no}

---

### 6. OR Flex  
**db.find("news", top_k=3, filter_query="category=news || category=greeting")**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=Hii, dist=0.48, meta={category=greeting, score=0.6, greeting=yes}

---

### 7. Multi-Filter  
**db.find("news", top_k=3, filter_query="category=news && score>0.7 && greeting=yes")**

_Result:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}

---

### 8. Score Range  
**db.find("news", top_k=3, filter_query="score=0.6-0.8")**

_Results:_  
text=Hii, dist=0.48, meta={category=greeting, score=0.6, greeting=yes}  
text=News article, dist=0.50, meta={category=news, score=0.7, greeting=no}

---

### 9. Skip Some  
**db.find("news", top_k=3, filter_query="text!=Hii && category!=introduction")**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=News article, dist=0.50, meta={category=news, score=0.7, greeting=no}

---

### 10. Name Drop  
**db.find("Rushikesh", top_k=3)**

_Result:_  
text=I Am Rushikesh Sunil Kotkar!, dist=0.20, meta={category=introduction, score=0.9}

---

### 11. Text or Score  
**db.find("Hel", top_k=3, filter_query="text=Hel* || score>=0.9")**

_Results:_  
text=Hello World, dist=0.45, meta={category=news, score=0.95, greeting=yes}  
text=I Am Rushikesh Sunil Kotkar!, dist=0.20, meta={category=introduction, score=0.9}

---

## Save/Load 💾  
Keep or get data:

**db.save()**  
**db.load()**

---

## Info 🌟  

**Version:** 
**Author:** Rushikesh Sunil Kotkar  
**License:** MIT  
**GitHub:** https://github.com/rushikeshkotkar04/vowdb  
**PyPI:** Fast text similarity with slick = queries.

---

## Contribute 🤝  
Got ideas? Issues? PRs?  
Hit up: https://github.com/rushikeshkotkar04/vowdb
