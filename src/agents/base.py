from abc import ABC, abstractmethod
from src.llm.base import BaseLLMClient


class BaseAgent(ABC):
    def __init__(self, llm: BaseLLMClient):
        self.llm = llm

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError
