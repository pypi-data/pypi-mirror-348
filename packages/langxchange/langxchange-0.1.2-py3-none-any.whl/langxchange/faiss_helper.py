import faiss
import numpy as np
import uuid


class FAISSHelper:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata_store = {}  # id -> {"text": ..., "meta": ...}
        self.id_list = []  # maintain insertion order for FAISS index

    def insert(self, vectors: list, documents: list, metadatas: list = None, ids: list = None):
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]

        try:
            self.index.add(np.array(vectors).astype("float32"))
            for i, doc, meta in zip(ids, documents, metadatas):
                self.metadata_store[i] = {"text": doc, "metadata": meta}
                self.id_list.append(i)
            return ids
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into FAISS: {e}")

    def query(self, embedding_vector: list, top_k: int = 5):
        try:
            D, I = self.index.search(np.array([embedding_vector]).astype("float32"), top_k)
            results = []
            for idx in I[0]:
                if 0 <= idx < len(self.id_list):
                    _id = self.id_list[idx]
                    results.append({
                        "id": _id,
                        "text": self.metadata_store[_id]["text"],
                        "metadata": self.metadata_store[_id]["metadata"]
                    })
            return results
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query FAISS: {e}")

    def count(self):
        return self.index.ntotal
