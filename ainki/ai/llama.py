import os
import requests
import openai
import logging
from ainki import secrets


def _generate_llama(
    prompt: str, model: str) -> openai.openai_object.OpenAIObject:
    s = requests.Session()
    token = secrets.ANYSCALE_API_KEY
    api_base = "https://api.endpoints.anyscale.com/v1"
    url = f"{api_base}/chat/completions"
    body = {
      "model": model,
      "messages": [
           {"role": "system", "content": "Your output will be used directly in a program by an advanced developer. Provide no pre-ambles, no ad-lib, no translation, no explanations."},
           {"role": "user", "content": prompt}
      ],
    }

    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        return resp.json()


def generate_llama_7b(prompt: str) -> str:
    return _generate_llama(prompt, model="meta-llama/Llama-2-7b-chat-hf")["choices"][0]["message"]["content"]


def generate_llama_13b(prompt: str) -> str:
    return _generate_llama(prompt, model="meta-llama/Llama-2-13b-chat-hf")["choices"][0]["message"]["content"]


def generate_llama_70b(prompt: str) -> str:
    return _generate_llama(prompt, model="meta-llama/Llama-2-70b-chat-hf")["choices"][0]["message"]["content"]
