import os
import json
from typing import List
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer


class suggestionEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

        # Constants
        self.DATA_DIR = "data"
        self.PERSIST_DIR = "kgn_index"
        self.user_memory_store = {}

        # Load or Create Llama Index
        if not os.path.exists(self.PERSIST_DIR):
            documents = SimpleDirectoryReader(self.DATA_DIR).load_data()
            self.vector_index = VectorStoreIndex.from_documents(documents)
            self.vector_index.storage_context.persist(persist_dir=self.PERSIST_DIR)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.PERSIST_DIR)
            self.vector_index = load_index_from_storage(storage_context)

    def get_user_memory(self, user: str) -> ChatMemoryBuffer:
        if user not in self.user_memory_store:
            self.user_memory_store[user] = ChatMemoryBuffer.from_defaults(token_limit=1500)
        return self.user_memory_store[user]

    def clear_user_memory(self, user: str):
        print("Memory Clear...")
        if user in self.user_memory_store:
            self.user_memory_store[user] = ChatMemoryBuffer.from_defaults(token_limit=1500)

    # Suggestion Logic
    async def get_strategy_recommendation(self, scenario: str, user: str) -> dict:
        # system_prompt = (
        #     "You are an AI assistant that processes user input to identify context and complete missing data in a JSON structure. "
        #     "If the input appears to be casual or friendly (e.g., greetings, general conversation), set 'intent': 'chitchat' and respond with a user-friendly message in 'prompt'. "
        #     "Otherwise, analyze the input to extract relevant information and populate the JSON. "
        #     "If any required values are missing, set 'intent': 'missing_value' and provide a prompt asking the user to supply the missing information. "
        #     "If all values are present, set 'intent': 'done' and return the completed JSON in 'data'. "
        #     "onces Data gets gathred promot back user with for conformatiosn and set isValidatedbyUser to true and intent will be 'conformations'"
        #     "during conformation user may change the Value Update actual_json accordingly"
        #     "Output format: { intent: '...', prompt: '...', data: { ...actual_json... }, isValidatedbyUser: Default false }"
        # )
        system_prompt = (
            "You are an AI assistant that processes user input to identify context and complete missing data in a JSON structure. "
            "Always include a user-friendly 'prompt' in every response to guide the next step. "
            "If the input is casual or friendly (e.g., greetings or small talk), set 'intent': 'chitchat' and provide a conversational message in 'prompt'. "
            "If the input requires structured data, analyze it and populate the JSON accordingly. "
            "If any required values are missing, set 'intent': 'missing_value', fill in available data, and use 'prompt' to ask the user for the missing fields. "
            "If all required values are filled, move to confirmation by setting 'intent': 'confirmation' and 'isValidatedbyUser': false. "
            "In the confirmation step, return the gathered data and ask the user to review or update any values using 'prompt'. "
            "Only when the user confirms the data (i.e., 'isValidatedbyUser' is true), set 'intent': 'done' and return the finalized JSON. "
            "Response format: { intent: '...', prompt: '...', data: { ...actual_json... }, isValidatedbyUser: true or false }"
        )






        memory = self.get_user_memory(user)

        chat_engine = self.vector_index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=system_prompt
        )

        content = chat_engine.chat(scenario)

        print("content.response", content.response)

        try:
            parsed = json.loads(content.response)
        except json.JSONDecodeError:
            raise ValueError("Model response could not be parsed as valid JSON.")

        intent = parsed.get("intent")

        # Handle memory clearing for specific intents
        if intent == "done":
            self.clear_user_memory(user)

        return parsed
