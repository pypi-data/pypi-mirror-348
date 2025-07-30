import os
import google.generativeai as genai


class GoogleGenAIHelper:
    def __init__(self, api_key: str = None, model: str = None, embed_model: str = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set.")

        genai.configure(api_key=self.api_key)

        self.chat_model = model or os.getenv("GOOGLE_CHAT_MODEL", "gemini-pro")
        self.embed_model = embed_model or os.getenv("GOOGLE_EMBED_MODEL", "models/embedding-001")

    def generate_text(self, prompt: str, temperature: float = 0.7):
        try:
            model = genai.GenerativeModel(self.chat_model)
            response = model.generate_content(prompt, generation_config={"temperature": temperature})
            return response.text
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Text generation failed: {e}")

    def get_embedding(self, text: str):
        try:
            model = genai.get_model(self.embed_model)
            response = model.embed_content(content=text, task_type="retrieval_document")
            return response["embedding"]
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to get Google embedding: {e}")

    def count_tokens(self, prompt: str):
        # No official token counter yet. Estimate: 1 token ≈ 0.75 words
        return int(len(prompt.split()) * 1.33)

    def list_models(self):
        try:
            return genai.list_models()
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to list GenAI models: {e}")
