from typing import Set, Type

from interfaces import IInstruction
from .arithmetic import Addition

INSTRUCTION_SET: Set[Type[IInstruction]] = {
	Addition
}
