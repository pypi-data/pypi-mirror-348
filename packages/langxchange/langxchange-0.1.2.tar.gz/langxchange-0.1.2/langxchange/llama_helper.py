import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from sentence_transformers import SentenceTransformer


class LLaMAHelper:

    def __init__(self, chat_model: str = None, embed_model: str = None):
        self.chat_model_name = chat_model or os.getenv("LLAMA_CHAT_MODEL", "meta-llama/Llama-2-7b-chat-hf")
        self.embed_model_name = embed_model or os.getenv("LLAMA_EMBED_MODEL", "all-MiniLM-L6-v2")

        # Load tokenizer and model (assumes HF model)
        self.tokenizer = AutoTokenizer.from_pretrained(self.chat_model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.chat_model_name)
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

        # Embedding model
        self.embedder = SentenceTransformer(self.embed_model_name)

    def generate_text(self, prompt: str, max_length: int = 256, temperature: float = 0.7):
        try:
            results = self.generator(prompt, max_length=max_length, do_sample=True, temperature=temperature)
            return results[0]["generated_text"]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to generate text: {e}")

    # def get_embedding(self, text: str) -> list:
    #     try:
    #         return self.embedder.encode(text).tolist()
    #     except Exception as e:
    #         raise RuntimeError(f"[❌ ERROR] Failed to generate embedding: {e}")
    
    def get_embedding(self, text: str) -> list:
        try:
            embedding = self.embedder.encode(text)
            return embedding.tolist() if hasattr(embedding, "tolist") else embedding
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to generate embedding: {e}")


    def count_tokens(self, prompt: str):
        return len(self.tokenizer.tokenize(prompt))
