from binary_types import Endianness
from memory import VolatileMemory

memory: VolatileMemory = VolatileMemory(2 ** (8 * 2), 4, 2, Endianness.BIG_ENDIAN)
