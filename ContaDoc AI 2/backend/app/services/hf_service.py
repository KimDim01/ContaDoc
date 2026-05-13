import requests
from app.core.config import settings

class HFClient:
    def __init__(self):
        self.api_token = settings.HF_API_TOKEN
        self.base_url = settings.HF_BASE_URL
        self.model = settings.HF_MODEL

    def validate_and_list_models(self):
        """
        Validates the API token and attempts to list models via HF API.
        """
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            # The HF Router usually provides model lists via the /models endpoint or simply by testing a call
            # We'll perform a simple "Health Check" request first
            response = requests.get(f"{self.base_url}/models", headers=headers, timeout=10)

            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "API Token is valid.",
                    "models": response.json().get("models", "Models listed in response")
                }
            else:
                return {
                    "status": "error",
                    "message": f"API Validation failed: {response.status_code}",
                    "detail": response.text
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection error: {str(e)}"
            }

    def chat_completion(self, prompt: str):
        """
        Makes a chat completion call to the Hugging Face Router.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }

        response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"HF API Error: {response.status_code} - {response.text}")

hf_client = HFClient()
