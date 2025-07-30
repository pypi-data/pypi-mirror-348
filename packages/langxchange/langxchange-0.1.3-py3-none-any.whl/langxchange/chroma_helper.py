import os
import uuid
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from chromadb import Client
from chromadb.config import Settings
from dotenv import load_dotenv


class ChromaHelper:records
    # Common column names to look for text content
    _POSSIBLE_TEXT_COLS = ["documents", "text", "content", "records"]

    def __init__(self, llm_helper, persist_directory=None):
        """
        llm_helper must implement get_embedding(str)->List[float]
        """
        if not llm_helper or not hasattr(llm_helper, "get_embedding"):
            raise ValueError("❌ A valid LLM helper instance with a 'get_embedding' method is required.")

        load_dotenv()  # load .env if present

        self.llm_helper = llm_helper
        persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_PATH", "./chroma_store")
        self.client = Client(Settings(persist_directory=persist_directory))

    def _choose_text_column(self, df: pd.DataFrame, override: str = None) -> str:
        """Pick the column to embed from, either override or first match."""
        if override:
            if override not in df.columns:
                raise KeyError(f"Override text_column='{override}' not in DataFrame columns: {df.columns.tolist()}")
            return override

        for col in self._POSSIBLE_TEXT_COLS:
            if col in df.columns:
                return col

        raise KeyError(f"No text column found in DataFrame. Tried: {self._POSSIBLE_TEXT_COLS}")

    def embed_texts_batched(self, texts: list) -> list:
        return [self.llm_helper.get_embedding(text) for text in texts]

    def ingest_to_chroma(
        self,
        df: pd.DataFrame,
        collection_name: str,
        text_column: str = None,
        engine: str = "llm"
    ) -> int:
        """
        Ingests a DataFrame into ChromaDB. Auto-detects or respects text_column.
        Returns total count in collection after ingestion.
        """
        batch_size = int(os.getenv("CHROMA_BATCH_SIZE", 100))
        max_workers = int(os.getenv("CHROMA_THREADS", 10))

        collection = self.client.get_or_create_collection(name=collection_name)
        total_records = len(df)
        print(f"🚀 Ingesting {total_records} records into '{collection_name}' using engine '{engine}'")

        def process_batch(batch_df: pd.DataFrame) -> int:
            # dynamically choose text column
            col = self._choose_text_column(batch_df, override=text_column)
            texts = batch_df[col].astype(str).tolist()

            ids = [str(uuid.uuid4()) for _ in texts]
            metadatas = batch_df.to_dict(orient="records")

            try:
                embeddings = self.embed_texts_batched(texts)
                collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
                return len(batch_df)
            except Exception as e:
                print(f"❌ Failed to add batch: {e}")
                return 0

        # build batches
        batches = [df[i : i + batch_size] for i in range(0, total_records, batch_size)]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_batch, b) for b in batches]
            with tqdm(total=len(batches), desc="🔄 Ingesting", unit="batch") as pbar:
                for fut in as_completed(futures):
                    fut.result()  # propagate exceptions
                    pbar.update(1)

        # return final count
        return len(collection.get()["ids"])

    def insert(
        self,
        collection_name: str,
        documents: list,
        embeddings: list,
        metadatas: list = None,
        ids: list = None
    ) -> list:
        """
        Directly insert parallel lists of documents/embeddings into the given collection.
        """
        collection = self.client.get_or_create_collection(name=collection_name)

        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]
        else:
            metadatas = [{"default": "value", **md} if not md else md for md in metadatas]

        try:
            collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into Chroma: {e}")

        return ids

    def query(
        self,
        collection_name: str,
        embedding_vector: list,
        top_k: int = 5,
        include_metadata: bool = True
    ) -> dict:
        """
        Query ChromaDB by embedding_vector; returns raw query response.
        """
        collection = self.client.get_or_create_collection(name=collection_name)
        try:
            return collection.query(
                query_embeddings=[embedding_vector],
                n_results=top_k,
                include=["documents", "metadatas"] if include_metadata else ["documents"]
            )
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query Chroma: {e}")

    def get_collection_count(self, collection_name: str) -> int:
        """
        Return the number of items in the named collection.
        """
        collection = self.client.get_or_create_collection(name=collection_name)
        try:
            return len(collection.get()["ids"])
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Could not get Chroma collection count: {e}")
