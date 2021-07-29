from typing import Set, Type

from interfaces import IInstruction
from .arithmetic import Addition
from .data import CopyRegister, SwapRegisters
from .flow import NoOperation

INSTRUCTION_SET: Set[Type[IInstruction]] = {
	Addition,
	CopyRegister,
	SwapRegisters,
	NoOperation,
}
