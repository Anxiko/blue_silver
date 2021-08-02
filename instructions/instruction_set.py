from typing import Set, Type

from interfaces import IInstruction
from .arithmetic import Addition
from .arithmetic.sub import Subtraction
from .branching import BranchIfEqual, BranchIfNotEqual, BranchIfGreater, BranchIfGreaterUnsigned, BranchIfLesser, \
	BranchIfLesserUnsigned
from .data import CopyRegister, SwapRegisters, LowDataNibbleCopy, HighDataNibbleCopy
from .flow import NoOperation
from .memory import LoadFromMemory, StoreIntoMemory

INSTRUCTION_SET: Set[Type[IInstruction]] = {
	Addition,
	Subtraction,

	CopyRegister,
	SwapRegisters,

	LowDataNibbleCopy,
	HighDataNibbleCopy,

	NoOperation,

	LoadFromMemory,
	StoreIntoMemory,

	BranchIfEqual,
	BranchIfNotEqual,

	BranchIfGreater,
	BranchIfGreaterUnsigned,

	BranchIfLesser,
	BranchIfLesserUnsigned
}

"""
- 1XAA ABBB (2 registers)
	- 10AA ABBB (CPY)
	- 11AA ABBB (SWP)
- 01XX XBBB (1 register)
	- 0100 XBBB (basic arithmetic)
		- 0100 0BBB (ADD)
		- 0100 1BBB (SUB)
- 001X IIII (1 immediate)
	- 0010 IIII (LNBL)
	- 0011 IIII (HNBL)
- 000X XXXX (no arguments)
	- 0000 0000 (NOOP)
	- 0000 100X (memory load/store)
		- 0000 1000 (LD)
		- 0000 1001 (ST)
	- 0001 XXXX (branching and jumping)
		- 0001 000X (equality)
			- 0001 0000 (BEQ)
			- 0001 0001 (BNEQ)
		- 0001 001X (greater than)
			- 0001 0010 (BGT)
			- 0001 0011 (BGTU)
		- 0001 010X (lesser than)
			- 0001 0100 (BLT)
			- 0001 0101 (BLTU)
"""
