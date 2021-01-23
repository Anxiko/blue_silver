from binary_types import as_byte
from interfaces.iinstruction import CodeOp
from registers import StateRegisterBitmask
from ..base import BaseInstruction
from interfaces.icpu import ICpu
from registers.registers import Registers


class Addition(BaseInstruction):
	@classmethod
	def get_codeop(cls) -> CodeOp:
		return CodeOp('add', as_byte(0b01000))

	def execute(self, cpu: ICpu) -> None:
		acc: bytes = cpu.read_register(Registers.ACC)
		operand_register: Registers = self.get_first_register()
		operand: bytes = cpu.read_register(operand_register)

		overflow: bool
		result: bytes
		overflow, result = cpu.get_spec_sheet().w_add(acc, operand)

		cpu.write_state(StateRegisterBitmask.OVERFLOW, overflow)
		cpu.write_register(Registers.ACC, result)
