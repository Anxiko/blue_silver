from binary_types import as_byte
from interfaces import ICpu
from registers import Registers
from ..base import NoArgumentsInstruction


class LeftShiftUnsigned(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SHLU'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00001100)

	def execute(self, cpu: ICpu) -> None:
		n_bits: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.DAT))
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))
		v = (v << n_bits) & ((1 << 32) - 1)
		cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))


class RightShiftUnsigned(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SHRU'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00001101)

	def execute(self, cpu: ICpu) -> None:
		n_bits: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.DAT))
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))
		v = (v >> n_bits)
		cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))
