from binary_types import as_byte
from registers import Registers
from ..base import DoubleRegisterInstruction
from interfaces import ICpu


class SwapRegisters(DoubleRegisterInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'SWP'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b11 << 6)

	def execute(self, cpu: ICpu) -> None:
		r1: Registers = self.get_first_register()
		r2: Registers = self.get_second_register()

		v1: bytes = cpu.read_register(r1)
		v2: bytes = cpu.read_register(r2)

		cpu.write_register(r1, v2)
		cpu.write_register(r2, v1)
