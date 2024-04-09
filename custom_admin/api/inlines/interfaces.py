from abc import ABC, abstractmethod


class InlineResultInterface(ABC):
    @abstractmethod
    def asdict(self) -> dict:
        pass
