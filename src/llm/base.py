from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, system: str, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        raise NotImplementedError
