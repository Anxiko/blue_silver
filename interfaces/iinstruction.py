from abc import ABC, abstractmethod
from dataclasses import dataclass

from interfaces.icpu import ICpu


@dataclass
class CodeOp:
	text_code: str
	byte_code: bytes

	def __post_init__(self):
		if len(self.byte_code) != 1:
			raise ValueError(f"Byte code {self.byte_code} must have a length of 1")


class IInstruction(ABC):
	@classmethod
	@abstractmethod
	def get_codeop(cls) -> CodeOp:
		pass

	@abstractmethod
	def execute(self, cpu: ICpu) -> None:
		pass
