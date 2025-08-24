#Large Language Models (LLMs) such as OpenAI, Gemini, DeepSeek and other reasoning models

import OpenAI
import Gemini
import DeepSeek 
import ReasoningModel
import os
import sys
import json
import time
import logging
import requests
from typing import List, Dict, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from requests.exceptions import RequestException
from openai.error import OpenAIError, RateLimitError, APIConnectionError, Timeout, ServiceUnavailableError
from gemini.error import GeminiError, GeminiRateLimitError, GeminiAPIConnectionError
from deepseek.error import DeepSeekError, DeepSeekRateLimitError, DeepSeekAPIConnection
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("gemini").setLevel(logging.WARNING)
logging.getLogger("deepseek").setLevel(logging.WARNING)
logging.getLogger("reasoningmodel").setLevel(logging.WARNING)
# Abstract base class for LLM clients
class LLMClient(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        pass    
# OpenAI Client
class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        OpenAI.api_key = self.api_key
    @retry(retry=retry_if_exception_type((RateLimitError, APIConnectionError, Timeout, ServiceUnavailableError)),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = OpenAI.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
# Gemini Client
class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-1.5"):
        self.api_key = api_key
        self.model = model
        Gemini.api_key = self.api_key
    @retry(retry=retry_if_exception_type((GeminiRateLimitError, GeminiAPIConnectionError)),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = Gemini.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except GeminiError as e:
            logger.error(f"Gemini API error: {e}")
            raise
# DeepSeek Client
class DeepSeekClient(LLMClient):
    def __init__(self, api_key: str, model: str = "deepseek-1.0"):
        self.api_key = api_key
        self.model = model
        DeepSeek.api_key = self.api_key
    @retry(retry=retry_if_exception_type((DeepSeekRateLimitError, DeepSeekAPIConnection)),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = DeepSeek.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except DeepSeekError as e:
            logger.error(f"DeepSeek API error: {e}")
            raise
# Reasoning Model Client
class ReasoningModelClient(LLMClient):  
    def __init__(self, api_key: str, model: str = "reasoningmodel-1.0"):
        self.api_key = api_key
        self.model = model
        ReasoningModel.api_key = self.api_key
    @retry(retry=retry_if_exception_type(RequestException),
           wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
    def generate_text(self, prompt: str, **kwargs) -> str:
        try:
            response = ReasoningModel.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message['content'].strip()
        except ReasoningModel.Error as e:
            logger.error(f"ReasoningModel API error: {e}")
            raise
# Factory to create LLM clients
class LLMClientFactory:
    @staticmethod
    def get_client(provider: str, api_key: str, model: str) -> LLMClient:
        if provider == "openai":
            return OpenAIClient(api_key, model)
        elif provider == "gemini":
            return GeminiClient(api_key, model)
        elif provider == "deepseek":
            return DeepSeekClient(api_key, model)
        elif provider == "reasoningmodel":
            return ReasoningModelClient(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
# Main function to demonstrate usage
def main():
    providers = [
        {"name": "openai", "api_key": os.getenv("OPENAI_API_KEY"), "model": "gpt-4"},
        {"name": "gemini", "api_key": os.getenv("GEMINI_API_KEY"), "model": "gemini-1.5"},
        {"name": "deepseek", "api_key": os.getenv("DEEPSEEK_API_KEY"), "model": "deepseek-1.0"},
        {"name": "reasoningmodel", "api_key": os.getenv("REASONINGMODEL_API_KEY"), "model": "reasoningmodel-1.0"}
    ]
    prompt = "Explain the theory of relativity in simple terms."
    results = {}
    with ThreadPoolExecutor(max_workers=len(providers)) as executor:
        future_to_provider = {
            executor.submit(
                LLMClientFactory.get_client(p["name"], p["api_key"], p["model"]).generate_text, prompt
            ): p["name"] for p in providers
        }
        for future in as_completed(future_to_provider):
            provider = future_to_provider[future]
            try:
                result = future.result()
                results[provider] = result
                logger.info(f"{provider} response: {result}")
            except Exception as e:
                logger.error(f"{provider} generated an exception: {e}")
    # Save results to a JSON file
    with open("llm_responses.json", "w") as f:
        json.dump(results, f, indent=4)
if __name__ == "__main__":
    main()  
#build a router to route requests to different LLMs based on the prompt content, user preferences, or other criteria.
class LLMRouter:
    def __init__(self, clients: Dict[str, LLMClient]):
        self.clients = clients
    def route_request(self, prompt: str, user_preferences: Dict[str, Any] = None) -> str:
        # Simple routing logic based on keywords in the prompt
        if "math" in prompt.lower():
            client = self.clients.get("reasoningmodel")
        elif user_preferences and user_preferences.get("preferred_provider"):
            preferred = user_preferences["preferred_provider"]
            client = self.clients.get(preferred, self.clients.get("openai"))
        else:
            client = self.clients.get("openai")
        if not client:
            raise ValueError("No suitable LLM client found.")
        return client.generate_text(prompt)
# Example usage of LLMRouter
def router_example():
    clients = {
        "openai": LLMClientFactory.get_client("openai", os.getenv("OPENAI_API_KEY"), "gpt-4"),
        "gemini": LLMClientFactory.get_client("gemini", os.getenv("GEMINI_API_KEY"), "gemini-1.5"),
        "deepseek": LLMClientFactory.get_client("deepseek", os.getenv("DEEPSEEK_API_KEY"), "deepseek-1.0"),
        "reasoningmodel": LLMClientFactory.get_client("reasoningmodel", os.getenv("REASONINGMODEL_API_KEY"), "reasoningmodel-1.0")
    }
    router = LLMRouter(clients)
    prompt = "Can you solve this math problem: What is the integral of x^2?"
    user_preferences = {"preferred_provider": "reasoningmodel"}
    response = router.route_request(prompt, user_preferences)
    logger.info(f"Routed response: {response}")

router_example()

