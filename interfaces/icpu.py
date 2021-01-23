from abc import ABC, abstractmethod

from binary_types import SpecSheet
from registers import Registers, StateRegisterBitmask


class ICpu(ABC):
	@abstractmethod
	def get_spec_sheet(self) -> SpecSheet:
		pass

	@abstractmethod
	def read_register(self, r: Registers) -> bytes:
		pass

	@abstractmethod
	def write_register(self, r: Registers, data: bytes) -> None:
		pass

	@abstractmethod
	def read_state(self, state: StateRegisterBitmask) -> bool:
		pass

	@abstractmethod
	def write_state(self, state: StateRegisterBitmask, v: bool) -> None:
		pass
