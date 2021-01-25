from typing import Set, Dict, List

from interfaces import IInstruction


class Assembler:
	instruction_set: Set[IInstruction]
	mapped_instructions: Dict[str, IInstruction]

	@staticmethod
	def _map_instruction_set(instruction_set: Set[IInstruction]) -> Dict[str, IInstruction]:
		rv: Dict[str, IInstruction] = {}

		for instruction in instruction_set:
			text_code: str = instruction.get_codeop().text_code
			if text_code in rv:
				raise ValueError(f"Text code {text_code} from {instruction} already in mapping")

		return rv

	def __init__(self, instruction_set: Set[IInstruction]):
		self.instruction_set = instruction_set
		self.mapped_instructions = type(self)._map_instruction_set(instruction_set)

	def _process_line(self, line: str):
		line_parts: List[str] = list(map(str.strip, line.split()))
		text_code: str = line_parts[0]
		arguments: List[str] = line_parts[1:]
