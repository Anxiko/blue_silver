from abc import ABC, abstractmethod
from typing import List

from binary_types import as_byte, ByteBitmask, from_byte
from interfaces import IInstruction, CodeOp, InstructionSymbol
from registers import Registers

"""
Instruction decoding guide:
(): codeop
[]: register
{}: immediate value

(1X) [XXX] [XXX]: 2 registers in instruction
(01XXX) [XXX]: 1 register in instruction
(001X) {XXXX}: 1 immediate value in instruction
(000X XXXX): no arguments, all instruction
"""


class BaseInstruction(IInstruction, ABC):
	@classmethod
	@abstractmethod
	def _get_text_code(cls) -> str:
		pass

	@classmethod
	@abstractmethod
	def _get_byte_code(cls) -> bytes:
		pass

	@classmethod
	@abstractmethod
	def _get_bitmask(cls) -> bytes:
		pass

	@classmethod
	@abstractmethod
	def _get_arguments(cls) -> List[InstructionSymbol]:
		pass

	@classmethod
	def get_codeop(cls) -> CodeOp:
		return CodeOp(
			cls._get_text_code(),
			cls._get_arguments(),
			cls._get_byte_code(),
			cls._get_bitmask()
		)

	@classmethod
	def from_assembly(cls, text_code: str, arguments: List[str]) -> 'IInstruction':
		if text_code != cls.get_codeop().text_code:
			raise ValueError(f"Text code {text_code} doesn't match the instruction's text code")

		if len(arguments) != len(cls._get_arguments()):
			raise ValueError(f"Number of arguments doesn't match expected number of arguments")

		return cls._from_assembly(text_code, arguments)

	@classmethod
	@abstractmethod
	def _from_assembly(cls, _: str, arguments: List[str]) -> 'IInstruction':
		pass


class NRegisterInstruction(BaseInstruction, ABC):
	_FIRST_REGISTER: ByteBitmask = ByteBitmask(3, 3)  # Reading left to right, first register in instruction
	_SECOND_REGISTER: ByteBitmask = ByteBitmask(3, 0)  # Appears on both 1 and 2 registers instructions

	@classmethod
	@abstractmethod
	def _get_n_registers(cls) -> int:
		pass

	@classmethod
	def _get_arguments(cls) -> List[InstructionSymbol]:
		return [InstructionSymbol.REGISTER] * cls._get_n_registers()

	def _extract_register(self, register: ByteBitmask) -> Registers:
		register_number: int = from_byte(register.extract_from_byte(self.code))
		rv: Registers = Registers(register_number)

		return rv

	@classmethod
	def _from_assembly(cls, _: str, arguments: List[str]) -> 'IInstruction':
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
	def _get_n_registers(cls) -> int:
		return 1

	@classmethod
	def _get_bitmask(cls) -> bytes:
		return as_byte(0b11111 << 3)

	def get_register(self) -> Registers:
		return self._extract_register(type(self)._SECOND_REGISTER)


class DoubleRegisterInstruction(NRegisterInstruction, ABC):
	@classmethod
	def _get_n_registers(cls) -> int:
		return 2

	@classmethod
	def _get_bitmask(cls) -> bytes:
		return as_byte(0b11 << 6)

	def get_first_register(self) -> Registers:
		return self._extract_register(type(self)._FIRST_REGISTER)

	def get_second_register(self) -> Registers:
		return self._extract_register(type(self)._SECOND_REGISTER)


class DataNibbleInstruction(BaseInstruction, ABC):
	@classmethod
	def _get_arguments(cls) -> List[InstructionSymbol]:
		return [InstructionSymbol.IMMEDIATE]

	@classmethod
	def _get_bitsmask(cls):
		return as_byte(0b1111 << 4)

	@classmethod
	def _from_assembly(cls, _: str, arguments: List[str]) -> 'IInstruction':
		code: int = from_byte(cls.get_codeop().byte_code)

		immediate_value: int
		try:
			immediate_value = int(arguments[0], 0)  # Base specified as 0 means it will be guessed from the value
		except ValueError:
			raise ValueError(f"Expected immediate value, but could not parse {arguments[0]} as int")

		if not (0 <= immediate_value < 2 ** 4):
			raise ValueError(f"Given immediate value {immediate_value} is outside valid range")

		code |= immediate_value

		return cls(as_byte(code))

	def get_immediate_value(self) -> int:
		code_value: int = from_byte(self.code)
		masked_value: int = code_value & 0b1111
		return masked_value


class NoArgumentsInstruction(BaseInstruction, ABC):
	@classmethod
	def _get_bitmask(cls) -> bytes:
		return as_byte(0b11111111)

	@classmethod
	def _get_arguments(cls) -> List[InstructionSymbol]:
		return list()

	@classmethod
	def _from_assembly(cls, _: str, arguments: List[str]) -> 'IInstruction':
		return cls(cls.get_codeop().byte_code)
