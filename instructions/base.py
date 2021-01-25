from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from binary_types import as_byte
from interfaces import InstructionSymbol
from registers import Registers
from interfaces import IInstruction, CodeOp


@dataclass
class RegisterInInstruction:
	bitmask: bytes
	right_shift: int

	def parse_register(self, code: bytes) -> Registers:
		register_index: int = code[0] & self.bitmask[0] >> self.right_shift
		return Registers(register_index)


class NRegisterInstruction(IInstruction, ABC):
	_FIRST_REGISTER: RegisterInInstruction = RegisterInInstruction(as_byte(0b00000111), 0)
	_SECOND_REGISTER: RegisterInInstruction = RegisterInInstruction(as_byte(0b00111000), 3)

	@classmethod
	@abstractmethod
	def get_text_code(cls) -> str:
		pass

	@classmethod
	@abstractmethod
	def get_byte_code(cls) -> bytes:
		pass

	@classmethod
	@abstractmethod
	def get_bitmask(cls) -> bytes:
		pass

	@classmethod
	@abstractmethod
	def get_n_registers(cls) -> int:
		pass

	@classmethod
	def get_codeop(cls) -> CodeOp:
		return CodeOp(
			cls.get_text_code(), [InstructionSymbol.REGISTER] * cls.get_n_registers(),
			cls.get_byte_code(), cls.get_bitmask()
		)


class SingleRegisterInstruction(NRegisterInstruction, ABC):
	@classmethod
	def get_n_registers(cls) -> int:
		return 1

	@classmethod
	def get_bitmask(cls) -> bytes:
		return as_byte(0b11111000)

	def get_register(self) -> Registers:
		return type(self)._FIRST_REGISTER.parse_register(self.code)


class DoubleRegisterInstruction(NRegisterInstruction, ABC):
	@classmethod
	def get_n_registers(cls) -> int:
		return 2

	@classmethod
	def get_bitmask(cls) -> bytes:
		return as_byte(0b11000000)

	def get_first_register(self) -> Registers:
		return type(self)._FIRST_REGISTER.parse_register(self.code)

	def get_second_register(self) -> Registers:
		return type(self)._SECOND_REGISTER.parse_register(self.code)
