from abc import ABC
from dataclasses import dataclass

from binary_types import as_byte
from registers import Registers
from interfaces import IInstruction


@dataclass
class RegisterInInstruction:
	bitmask: bytes
	right_shift: int

	def parse_register(self, code: bytes) -> Registers:
		register_index: int = code[0] & self.bitmask[0] >> self.right_shift
		return Registers(register_index)


class BaseInstruction(IInstruction, ABC):
	_FIRST_REGISTER: RegisterInInstruction = RegisterInInstruction(as_byte(0b00000111), 0)
	_SECOND_REGISTER: RegisterInInstruction = RegisterInInstruction(as_byte(0b00111000), 3)

	code: bytes

	def __init__(self, code: bytes):
		self.code = code

	def get_first_register(self) -> Registers:
		return type(self)._FIRST_REGISTER.parse_register(self.code)

	def get_second_register(self) -> Registers:
		return type(self)._SECOND_REGISTER.parse_register(self.code)
