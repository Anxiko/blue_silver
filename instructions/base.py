from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from binary_types import as_byte
from binary_types.byte_bitmask import ByteBitmask
from binary_types.conversions import from_byte
from interfaces import InstructionSymbol
from registers import Registers
from interfaces import IInstruction, CodeOp


class NRegisterInstruction(IInstruction, ABC):
	_FIRST_REGISTER: ByteBitmask = ByteBitmask(3, 3)  # Reading left to right, first register in instruction
	_SECOND_REGISTER: ByteBitmask = ByteBitmask(3, 0)  # Appears on both 1 and 2 registers instructions

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

	def _extract_register(self, register: ByteBitmask) -> Registers:
		register_number: int = from_byte(register.extract_from_byte(self.code))
		rv: Registers = Registers(register_number)

		return rv

	@classmethod
	def from_assembly(cls, text_code: str, arguments: List[str]) -> 'IInstruction':
		if text_code != cls.get_codeop().text_code:
			raise ValueError(f"Text code {text_code} doesn't match the instruction's text code")

		if len(arguments) != cls.get_n_registers():
			raise ValueError(f"Number of arguments doesn't match expected number of registers")

		code: int = from_byte(cls.get_codeop().byte_code)
		registers_in_instruction: List[ByteBitmask] = [cls._FIRST_REGISTER, cls._SECOND_REGISTER]

		"""
		If there are less arguments than possible registers, the registers to be used should be the latest,
		since those are the ones located in the less significant bits inside the instruction.
		
		If there is only one register, for example, it isn't the first one, it is the last one.
		That's because registers are written towards the less significant bits inside the instruction,
		while being read left to right. The first register to be read, will be writen towards the most significant bits,
		and the last will form the least significant bits.
		
		In short, register bits are written within the machine code left to right, exactly as their written.
		"""
		if len(arguments) < len(registers_in_instruction):
			# Beware of changing this to use a negative index here, it won't behave nicely if there are 0 arguments!
			registers_in_instruction = registers_in_instruction[len(registers_in_instruction) - len(arguments):]

		for argument, register_in_instruction in zip(arguments, registers_in_instruction):
			register: Registers = Registers[argument.upper()]
			register_number: int = register.value
			register_code: bytes = register_in_instruction.to_masked_byte(as_byte(register_number))
			code |= from_byte(register_code)

		return cls(as_byte(code))


class SingleRegisterInstruction(NRegisterInstruction, ABC):
	@classmethod
	def get_n_registers(cls) -> int:
		return 1

	@classmethod
	def get_bitmask(cls) -> bytes:
		return as_byte(0b11111000)

	def get_register(self) -> Registers:
		return self._extract_register(type(self)._SECOND_REGISTER)


class DoubleRegisterInstruction(NRegisterInstruction, ABC):
	@classmethod
	def get_n_registers(cls) -> int:
		return 2

	@classmethod
	def get_bitmask(cls) -> bytes:
		return as_byte(0b11000000)

	def get_first_register(self) -> Registers:
		return self._extract_register(type(self)._FIRST_REGISTER)

	def get_second_register(self) -> Registers:
		return self._extract_register(type(self)._SECOND_REGISTER)
