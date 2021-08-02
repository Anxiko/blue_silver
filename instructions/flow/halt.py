from binary_types import as_byte
from interfaces import ICpu
from registers import StateRegisterBitmask
from ..base import NoArgumentsInstruction

"""
This will probably have to be redone in another way, raising exceptions. It should do for now.
"""


class Halt(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'HALT'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00000001)

	def execute(self, cpu: ICpu) -> None:
		cpu.write_state(StateRegisterBitmask.HALT, True)
