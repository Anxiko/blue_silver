from binary_types import as_byte
from instructions.branching.base_branching import BaseBranchingInstruction


class BranchIfLesser(BaseBranchingInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'BLT'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010100)

	@classmethod
	def _operands_are_signed(cls) -> bool:
		return True

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 < v2


class BranchIfLesserUnsigned(BaseBranchingInstruction):
	@classmethod
	def _get_text_code(cls) -> str:
		return 'BLTU'

	@classmethod
	def _get_byte_code(cls) -> bytes:
		return as_byte(0b00010101)

	@classmethod
	def _operands_are_signed(cls) -> bool:
		return False

	@classmethod
	def _branch(cls, v1: int, v2: int) -> bool:
		return v1 < v2
