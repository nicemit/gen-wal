import base64
import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt: str, seed: int, config: dict, width: int, height: int):
    base_url = config.get("base_url", "http://localhost:1234/v1")
    model = config.get("model", "local-model")
    api_key = config.get("api_key", "sk-dummy")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Common OpenAI compatible payload
    payload = {
        "prompt": prompt,
        "model": model,
        "n": 1,
        "response_format": "b64_json",
        "size": f"{width}x{height}"
    }
    
    endpoint = f"{base_url.rstrip('/')}/images/generations"
    print(f"  ➜ Requesting OpenAI-compatible API at {endpoint}...")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
    except Exception as e:
        error_msg = response.text if 'response' in locals() else str(e)
        raise RuntimeError(f"OpenAI compatible API error: {error_msg}")
        
    data = response.json()
    b64_data = data["data"][0].get("b64_json")
    
    if not b64_data:
        # Fallback if the API returned an image URL instead of b64
        url = data["data"][0].get("url")
        if url:
            img_res = requests.get(url)
            return Image.open(BytesIO(img_res.content))
        raise RuntimeError("API returned neither b64_json nor url")
        
    image_data = base64.b64decode(b64_data)
    return Image.open(BytesIO(image_data))

def generate_text(prompt: str, seed: int, config: dict):
    base_url = config.get("base_url", "http://localhost:1234/v1")
    model = config.get("model", "local-model")
    api_key = config.get("api_key", "sk-dummy")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    endpoint = f"{base_url.rstrip('/')}/chat/completions"
    print(f"  ➜ Requesting OpenAI-compatible text API at {endpoint}...")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
    except Exception as e:
        error_msg = response.text if 'response' in locals() else str(e)
        raise RuntimeError(f"OpenAI compatible text API error: {error_msg}")
        
    data = response.json()
    return data["choices"][0]["message"]["content"].strip('"\' \n')

