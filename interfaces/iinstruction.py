from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from binary_types import apply_binary_operation, bitwise_and
from .icpu import ICpu
from .symbols import InstructionSymbol


@dataclass
class CodeOp:
	text_code: str
	arguments: List[InstructionSymbol]

	byte_code: bytes
	bitmask: bytes

	def __post_init__(self):
		if len(self.byte_code) != len(self.bitmask):
			raise ValueError(f"Length of byte code {self.byte_code} and bitmask {self.bitmask} don't match up")

	def instruction_matches(self, instruction: bytes) -> bool:
		if len(instruction) != len(self.byte_code):
			raise ValueError(f"Length of instruction {instruction} and byte code {self.byte_code} don't match up")

		instruction_masked: bytes = apply_binary_operation(instruction, self.bitmask, bitwise_and)
		return instruction_masked == self.byte_code


class IInstruction(ABC):
	code: bytes

	def __init__(self, code: bytes):
		self.code = code

	@classmethod
	@abstractmethod
	def get_codeop(cls) -> CodeOp:
		pass

	@abstractmethod
	def execute(self, cpu: ICpu) -> None:
		pass
