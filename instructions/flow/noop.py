from binary_types import as_byte
from interfaces import ICpu
from ..base import NoArgumentsInstruction


class NoOperation(NoArgumentsInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'NOOP'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00000000)

	def execute(self, cpu: ICpu) -> None:
		pass
