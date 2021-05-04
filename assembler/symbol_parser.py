import re
from abc import ABC, abstractmethod
from lib2to3.pygram import Symbols
from math import ceil, log
from re import Pattern, Match
from typing import Dict, Type

from binary_types import as_byte
from interfaces import InstructionSymbol
from registers import Registers


class SymbolParser(ABC):
	_raw: str

	def __init__(self, raw: str):
		self._raw = raw

	@classmethod
	@abstractmethod
	def bit_length(cls) -> int:
		pass

	@abstractmethod
	def parse(self) -> bytes:
		pass


class RegisterParser(SymbolParser):
	_PATTERN: Pattern = re.compile(r'\.(\w+)')

	@classmethod
	def bit_length(cls) -> int:
		return ceil(
			log(len(Registers), 2)
		)

	def _extract_register_name(self) -> str:
		match: Match = type(self)._PATTERN.match(self._raw)
		if match is None:
			raise ValueError(f"Given register {self._raw} does not match pattern {type(self)._PATTERN}")
		return match.group(1)

	def parse(self) -> bytes:
		reg: Registers = Registers[self._extract_register_name()]
		reg_byte: bytes = as_byte(reg.value)
		return reg_byte


SYMBOL_PARSER_MAPPING: Dict[InstructionSymbol, Type[SymbolParser]] = {
	InstructionSymbol.REGISTER: RegisterParser
}
