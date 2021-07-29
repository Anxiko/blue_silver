from enum import Enum
from math import log

BITS_PER_REGISTER: int = 3


# TODO: redefine enum so all values are auto() and start at zero?
class Registers(Enum):
	ZERO = 0  # Reads always return 0, writes are discarded
	PC = 1  # Program counter
	STATE = 2  # CPU state bitfield
	HEAP = 3  # Heap pointer
	SP = 4  # Stack pointer
	ACC = 5  # Accumulator, stores the result of many operations
	ADDR = 6  # Address used in memory access instructions
	DAT = 7  # Free purpose register


assert log(len(Registers), 2) <= BITS_PER_REGISTER, "Cannot fit all registers into the allocated number of bits"
