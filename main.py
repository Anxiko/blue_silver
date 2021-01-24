from binary_types import SpecSheet, Endianness
from cpu import Processor
from memory import VolatileMemory
from registers import Registers

ENDIANNESS: Endianness = Endianness.BIG_ENDIAN
WORD_SIZE: int = 4
INSTRUCTION_SIZE: int = 1

REGISTER_BANK_SIZE_WORDS: int = len(Registers)
RAM_SIZE_BYTES: int = 2 ** (8 * 2)

ADDR_BUS_SIZE_REGISTERS: int = 1
ADDR_BUS_SIZE_RAM: int = 2

if __name__ == '__main__':
	ram: VolatileMemory = VolatileMemory(
		RAM_SIZE_BYTES, WORD_SIZE, ADDR_BUS_SIZE_RAM, ENDIANNESS)
	register_bank: VolatileMemory = VolatileMemory(
		REGISTER_BANK_SIZE_WORDS * WORD_SIZE, WORD_SIZE, ADDR_BUS_SIZE_REGISTERS, ENDIANNESS)

	cpu: Processor = Processor(SpecSheet(ENDIANNESS, WORD_SIZE, INSTRUCTION_SIZE), register_bank, ram)
