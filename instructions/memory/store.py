from binary_types import as_byte
from interfaces import ICpu
from registers import Registers
from ..base import NoArgumentsInstruction


class StoreIntoMemory(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'ST'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010001)

	def execute(self, cpu: ICpu) -> None:
		full_address: bytes = cpu.read_register(Registers.ADDR)
		address: bytes = cpu.get_spec_sheet().get_least_significant_bytes(
			full_address, cpu.get_spec_sheet().address_size)

		w: bytes = cpu.read_register(Registers.ACC)
		cpu.write_ram(address, w)
