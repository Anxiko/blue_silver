from typing import Set, Dict, List, Type, TextIO, BinaryIO

from interfaces import IInstruction


class Assembler:
	instruction_set: Set[Type[IInstruction]]
	mapped_instructions: Dict[str, Type[IInstruction]]

	@staticmethod
	def _map_instruction_set(instruction_set: Set[Type[IInstruction]]) -> Dict[str, Type[IInstruction]]:
		rv: Dict[str, Type[IInstruction]] = {}

		for instruction in instruction_set:
			text_code: str = instruction.get_codeop().text_code
			if text_code in rv:
				raise ValueError(f"Text code {text_code} from {instruction} already in mapping")
			rv[text_code] = instruction

		return rv

	def __init__(self, instruction_set: Set[Type[IInstruction]]):
		self.instruction_set = instruction_set
		self.mapped_instructions = type(self)._map_instruction_set(instruction_set)

	def _process_line(self, line: str) -> IInstruction:
		line_parts: List[str] = list(map(str.strip, line.split()))
		text_code: str = line_parts[0]
		arguments: List[str] = line_parts[1:]

		instruction_type: Type[IInstruction] = self.mapped_instructions[text_code.upper()]
		instruction: IInstruction = instruction_type.from_assembly(text_code, arguments)

		return instruction

	def _assemble_file_into_instructions(self, src_file: TextIO) -> List[IInstruction]:
		rv: List[IInstruction] = []

		for line in src_file:
			rv.append(self._process_line(line))

		return rv

	def assemble_file(self, src_file: TextIO, destination: BinaryIO) -> None:
		compiled_instructions: List[IInstruction] = self._assemble_file_into_instructions(src_file)
		for compiled_instruction in compiled_instructions:
			destination.write(compiled_instruction.code)
