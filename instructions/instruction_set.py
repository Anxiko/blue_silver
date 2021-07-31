from typing import Set, Type

from interfaces import IInstruction
from .arithmetic import Addition
from .data import CopyRegister, SwapRegisters
from .flow import NoOperation
from .memory import LoadFromMemory, StoreIntoMemory

INSTRUCTION_SET: Set[Type[IInstruction]] = {
	Addition,
	CopyRegister,
	SwapRegisters,
	NoOperation,
	LoadFromMemory,
	StoreIntoMemory
}
