import requests
import json
from typing import Optional, Dict, Any

class DeepSeekAPI:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com", proxy: Optional[str] = None, verify_ssl: bool = True):
        self.api_key = api_key
        self.base_url = base_url
        self.proxy = proxy
        self.verify_ssl = verify_ssl
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def chat_completion(
        self,
        messages: list,
        model: str = "deepseek-chat",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            print(f"  -> URL: {url}")
            print(f"  -> Model: {model}")
            print(f"  -> API Key prefix: {self.api_key[:10]}..." if len(self.api_key) > 10 else "  -> API Key: [short]")
            
            proxies = None
            if self.proxy:
                proxies = {"https": self.proxy}
                print(f"  -> Using proxy: {self.proxy}")
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=120, proxies=proxies, verify=self.verify_ssl)
            print(f"  -> Status code: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  -> Request failed: {type(e).__name__}: {e}")
            return {"error": str(e)}

    def extract_content(self, response: Dict[str, Any]) -> str:
        try:
            choices = response.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return ""
        except (KeyError, IndexError):
            return ""