from binary_types import as_byte
from .base_branching import BaseBranchingInstruction


class BranchIfEqual(BaseBranchingInstruction):
	@classmethod
	def _operands_are_signed(cls) -> bool:
		return False

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 == v2

	@classmethod
	def _get_text_code(cls) -> str:
		return 'BEQ'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010000)


class BranchIfNotEqual(BaseBranchingInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'BNEQ'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010001)

	@classmethod
	def _operands_are_signed(cls) -> bool:
		return False

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 != v2
