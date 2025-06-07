from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

class OpenRouterLLM(BaseChatModel):
    model: str = "mistralai/mistral-7b-instruct:free"

    def _llm_type(self) -> str:
        return "openrouter"

    def _generate(self, messages: List[BaseMessage], stop=None, **kwargs) -> ChatResult:
        formatted_messages = [
            {"role": "system" if m.type == "system" else "user", "content": m.content}
            for m in messages
        ]

        response = client.chat.completions.create(
            model=self.model,
            messages=formatted_messages
        )

        content = response.choices[0].message.content
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    def get_num_tokens(self, text: str) -> int:
        return len(text.split())
