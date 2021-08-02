from binary_types import as_byte
from .base_branching import BaseBranchingInstruction


class BranchIfGreater(BaseBranchingInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'BGT'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010010)

	@classmethod
	def _operands_are_signed(cls) -> bool:
		return True

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 > v2


class BranchIfGreaterUnsigned(BaseBranchingInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'BGTU'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010011)

	@classmethod
	def _operands_are_signed(cls) -> bool:
		return False

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 > v2
