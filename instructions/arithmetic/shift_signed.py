from interfaces import ICpu
from registers import Registers
from ..base import NoArgumentsInstruction


class LeftShiftSigned(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SHLS'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		from binary_types import as_byte
		return as_byte(0b00001110)

	def execute(self, cpu: ICpu) -> None:
		n_bits: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.DAT))
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))

		sign: int = (1 << 32) & v

		v = ((v << n_bits) & ((1 << 31) - 1)) | sign
		cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))


class RightShiftSigned(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SHRS'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		from binary_types import as_byte
		return as_byte(0b00001111)

	def execute(self, cpu: ICpu) -> None:
		n_bits: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.DAT))
		v: int = cpu.get_spec_sheet().word_to_int(cpu.read_register(Registers.ACC))

		sign: int = (1 << 31) & v

		v = (v >> n_bits) | sign
		cpu.write_register(Registers.ACC, cpu.get_spec_sheet().int_to_word(v))
