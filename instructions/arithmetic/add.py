from binary_types import as_byte
from interfaces import ICpu
from ..base import SingleRegisterInstruction
from registers import StateRegisterBitmask, Registers


class Addition(SingleRegisterInstruction):
	@classmethod
	def get_text_code(cls) -> str:
		return 'ADD'

	@classmethod
	def get_byte_code(cls) -> bytes:
		return as_byte(0b10000000)

	def execute(self, cpu: ICpu) -> None:
		acc: bytes = cpu.read_register(Registers.ACC)
		operand_register: Registers = self.get_register()
		operand: bytes = cpu.read_register(operand_register)

		overflow: bool
		result: bytes
		overflow, result = cpu.get_spec_sheet().w_add(acc, operand)

		cpu.write_state(StateRegisterBitmask.OVERFLOW, overflow)
		cpu.write_register(Registers.ACC, result)
