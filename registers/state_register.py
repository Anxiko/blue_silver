from enum import IntFlag


class StateRegisterBitmask(IntFlag):
	OVERFLOW = 1 << 0
	HALT = 1 << 7

