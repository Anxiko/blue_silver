import sys

from assembler import Assembler
from instructions import INSTRUCTION_SET


def main() -> None:
	if not (2 <= len(sys.argv) <= 3):
		print(f"Usage: {sys.argv[0]} input.slv [output.slb]")
		return

	input_filename: str = sys.argv[1]
	output_filename: str = sys.argv[2] if len(sys.argv) >= 3 else 'output.slb'

	with open(input_filename) as input_file, open(output_filename, mode='wb') as output_file:
		assembler: Assembler = Assembler(INSTRUCTION_SET)
		assembler.assemble_file(input_file, output_file)


if __name__ == '__main__':
	main()
