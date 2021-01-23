from enum import Enum

from binary_types import as_byte


class StateRegisterBitmask(Enum):
	OVERFLOW = as_byte(1 << 0)
