from binary_types import as_byte
from interfaces import ICpu
from registers import Registers
from ..base import DoubleRegisterInstruction


class CopyRegister(DoubleRegisterInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'CPY'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b10 << 6)

	def execute(self, cpu: ICpu) -> None:
		src_reg: Registers = self.get_first_register()
		dst_reg: Registers = self.get_second_register()

		v: bytes = cpu.read_register(src_reg)
		cpu.write_register(dst_reg, v)


