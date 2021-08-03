from binary_types import as_byte
from interfaces import ICpu
from registers import Registers
from ..base import NoArgumentsInstruction


class LeftShiftByte(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SBL'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00001010)

	def execute(self, cpu: ICpu) -> None:
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))
		v = (v << 8) & ((1 << 32) - 1)
		return cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))


class RightShiftByte(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SBR'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00001011)

	def execute(self, cpu: ICpu) -> None:
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))
		v = v >> 8
		return cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))
