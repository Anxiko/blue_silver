from abc import abstractmethod, ABC

from binary_types import as_byte, b_not, apply_binary_operation, bitwise_and, bitwise_or
from interfaces import ICpu
from registers import Registers
from ..base import DataNibbleInstruction


class DataNibbleCopy(DataNibbleInstruction, ABC):
	@classmethod
	@abstractmethod
	def _left_shift(cls) -> int:
		pass

	@classmethod
	def _get_bitmask(cls) -> bytes:
		return as_byte(0b1111 << 4)

	def execute(self, cpu: ICpu) -> None:
		bitmask: bytes = cpu.get_spec_sheet().int_to_word(0b1111 << type(self)._left_shift())
		negated_bitmask: bytes = b_not(bitmask)

		v: int = self.get_immediate_value() << type(self)._left_shift()
		w: bytes = cpu.get_spec_sheet().int_to_word(v)

		target: bytes = cpu.read_register(Registers.ACC)
		target = apply_binary_operation(target, negated_bitmask, bitwise_and)
		target = apply_binary_operation(target, w, bitwise_or)
		cpu.write_register(Registers.ACC, target)


class LowDataNibbleCopy(DataNibbleCopy):
	@classmethod
	def _left_shift(cls) -> int:
		return 0

	@classmethod
	def _get_text_code(cls) -> str:
		return 'LNBL'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b0010 << 4)


class HighDataNibbleCopy(DataNibbleCopy):
	@classmethod
	def _left_shift(cls) -> int:
		return 4

	@classmethod
	def _get_text_code(cls) -> str:
		return 'HNBL'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b0011 << 4)
