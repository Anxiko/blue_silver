from typing import Set, Type

from interfaces import IInstruction
from .arithmetic import Addition
from .arithmetic.sub import Subtraction
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
	StoreIntoMemory
}
