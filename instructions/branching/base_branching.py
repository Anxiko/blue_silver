from abc import abstractmethod

from interfaces import ICpu
from registers import Registers
from ..base import NoArgumentsInstruction


class BaseBranchingInstruction(NoArgumentsInstruction):
	@classmethod
	@abstractmethod
	def _operands_are_signed(cls) -> bool:
		pass

	@classmethod
	@abstractmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		pass

	def execute(self, cpu: ICpu) -> None:
		w1: bytes = cpu.read_register(Registers.ACC)
		w2: bytes = cpu.read_register(Registers.DAT)

		v1: int = cpu.get_spec_sheet().word_to_int(w1, signed=type(self)._operands_are_signed())
		v2: int = cpu.get_spec_sheet().word_to_int(w2, signed=type(self)._operands_are_signed())

		if type(self)._branch(v1, v2):
			cpu.write_register(Registers.PC, cpu.read_register(Registers.ADDR))
