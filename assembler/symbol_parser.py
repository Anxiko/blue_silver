from abc import ABC, abstractmethod

from binary_types import as_byte
from registers import Registers


class SymbolParser(ABC):
	raw: str

	def __init__(self, raw: str):
		self.raw = raw

	@classmethod
	@abstractmethod
	def bit_length(cls) -> int:
		pass

	@abstractmethod
	def parse(self) -> bytes:
		pass


class RegisterParser(SymbolParser):
	@classmethod
	def bit_length(cls) -> int:
		return 3  # TODO: calculate length based on register bank size?

	def parse(self) -> bytes:
		reg: Registers = Registers[self.raw]
		reg_byte: bytes = as_byte(reg.value)
		return reg_byte
