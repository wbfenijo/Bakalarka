import requests
from openai_client import OpenAIClient

OPENAI_MODELS = {
    "gpt-4o-mini",
    "gpt-5"
}

OLLAMA_MODELS = {
    "llama3.1:8b",
    "mistral"
}

EXTERNAL_MODELS = {
    "azure/gpt-4.1",
    "azure/gpt-4.1-mini",
    "azure/gpt-4o",
    "azure/gpt-5.1",
    "devstral-small-2",
    "Gemma3-27b",
    "google/claude-haiku-4-5",
    "google/claude-sonnet-4-5",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-pro",
    "GPT-oss-120b",
    "GPT-oss-20b",
    "Granite-4.0-tiny",
    "Llama-3.1-70b",
    "minimax-m2.1",
    "Ministral-3-14B-Instruct",
    "Mistral-Small-3.2-24B-Instruct",
    "ollama-embedding-qwen3-06",
    "vision/Qwen3-32b-VL"
}




OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11435

def query_ollama(model_name: str, prompt: str) -> str:
    url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/generate"
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    try:
        resp = requests.post(url, json=payload, timeout=120)
        data = resp.json()
        if "response" in data:
            return data["response"]
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]
        return str(data)
    except Exception as e:
        return f"Error querying {model_name}: {e}"




def query_external_model(model_name: str, prompt: str) -> str: #Lukas

    return ...




def query_model(model_name: str, prompt: str) -> str:

    if model_name in OPENAI_MODELS:
        client = OpenAIClient(model_name)
        return client.query(prompt)

    elif model_name in OLLAMA_MODELS:
        return query_ollama(model_name, prompt)

    elif model_name in EXTERNAL_MODELS:
        return query_external_model(model_name, prompt)

    else:
        raise ValueError(f"Unknown model: {model_name}")