from typing import Set, Type, Dict, Iterable

from binary_types import apply_binary_operation, bitwise_and
from interfaces import IInstruction, CodeOp
from .arithmetic import Addition

INSTRUCTION_SET: Set[Type[IInstruction]] = {
	Addition
}


class Dispatcher:
	mapped_bitmask_instructions: Dict[bytes, Dict[bytes, Type[IInstruction]]]

	def __init__(self, instructions: Iterable[Type[IInstruction]]):
		self.mapped_bitmask_byte_code_instructions = {}

		for instruction in instructions:
			codeop: CodeOp = instruction.get_codeop()

			mapped_byte_code_instruction: Dict[bytes, Type[IInstruction]] = \
				self.mapped_bitmask_byte_code_instructions.setdefault(codeop.bitmask, {})

			if codeop.byte_code in mapped_byte_code_instruction:
				raise KeyError(f"Repeated instructions for {codeop}")

			mapped_byte_code_instruction[codeop.byte_code] = instruction

	def dispatch(self, code: bytes) -> IInstruction:
		for bitmask, mapped_byte_code_instruction in self.mapped_bitmask_byte_code_instructions.items():
			bitmasked_code: bytes = apply_binary_operation(code, bitmask, bitwise_and)

			try:
				instruction_type: Type[IInstruction] = mapped_byte_code_instruction[bitmasked_code]
				return instruction_type(code)
			except KeyError:
				pass
		raise KeyError(f"No instruction found for {code}")
