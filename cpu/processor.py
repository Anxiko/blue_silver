from typing import Union

from binary_types import SpecSheet, as_byte
from interfaces import ICpu
from memory import VolatileMemory
from registers import Registers


class Processor(ICpu):
	_spec_sheet: SpecSheet
	register_bank: VolatileMemory
	ram: VolatileMemory

	def __init__(self, spec_sheet: SpecSheet):
		self._spec_sheet = spec_sheet
		self.register_bank = VolatileMemory(
			self._spec_sheet.word_size * self._spec_sheet.register_bank_size_words,
			self._spec_sheet.word_size,
			self._spec_sheet.register_address_bus_size
		)

		self.ram = VolatileMemory(
			self._spec_sheet.word_size * self._spec_sheet.ram_size_words,
			self._spec_sheet.word_size,
			self._spec_sheet.ram_address_bus_size
		)

	def read_register(self, r: Registers) -> bytes:
		if r == Registers.ZERO:
			return as_byte(0) * self._spec_sheet.word_size
		return self.register_bank.read(r.value)

	def write_register(self, r: Registers, data: bytes) -> None:
		if r == Registers.ZERO:
			pass
		self.register_bank.write(r.value, data)

	def get_spec_sheet(self) -> SpecSheet:
		return self._spec_sheet

	def _reg_as_address(self, reg_or_idx: Union[Registers, int]) -> bytes:
		idx: int = reg_or_idx.value if isinstance(reg_or_idx, Registers) else reg_or_idx
		return self._spec_sheet.int_to_word(idx)

	def cycle(self) -> None:
		instruction_address: bytes = self.register_bank.read(self._reg_as_address(Registers.PC))
		next_instruction_address: bytes = self._spec_sheet.w_increase(
			instruction_address, self._spec_sheet.word_size)[1]
		self.register_bank.write(self._reg_as_address(Registers.PC), next_instruction_address)

		instruction: bytes = self.ram.read(self._reg_as_address(Registers.PC))
		self._run_instruction(instruction)

	def _run_instruction(self, instruction: bytes) -> None:
		pass  # TODO: decode and run instruction
