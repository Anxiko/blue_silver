from enum import Enum
from math import log

BITS_PER_REGISTER: int = 3


class Registers(Enum):
	ZERO = 0
	PC = 1
	RESERVED_2 = 2
	STATE = 3
	SP = 4
	ACC = 5
	ADDR = 6
	D0 = 6
	D1 = 7


assert log(len(Registers), 2) <= BITS_PER_REGISTER, "Cannot fit all registers into the allocated number of bits"
