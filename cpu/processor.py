from typing import Union, Optional

from binary_types import SpecSheet, as_byte, apply_binary_operation, bitwise_and, bitwise_xor
from interfaces import ICpu, IInstruction
from memory import VolatileMemory
from registers import Registers, StateRegisterBitmask
from .dispatcher import Dispatcher


class Processor(ICpu):
	_spec_sheet: SpecSheet
	register_bank: VolatileMemory
	ram: VolatileMemory
	dispatcher: Dispatcher

	_instruction_buffer: Optional[bytes]
	_cached_instruction_word_addr: Optional[bytes]

	def __init__(self, spec_sheet: SpecSheet, register_bank: VolatileMemory, ram: VolatileMemory):
		self._spec_sheet = spec_sheet
		self.register_bank = register_bank
		self.ram = ram

		self._instruction_buffer = None
		self._cached_instruction_word_addr = None

		if (
				(self._spec_sheet.instruction_size > self._spec_sheet.word_size)
				or
				(self._spec_sheet.word_size % self._spec_sheet.instruction_size != 0)
		):
			raise ValueError(
				f"Instruction size {self._spec_sheet.instruction_size} incompatible with word size {self._spec_sheet.word_size}"
			)

		if len({self._spec_sheet.word_size, self.register_bank.data_bus_size, self.ram.data_bus_size}) != 1:
			raise ValueError(
				f"RAM {self.ram} or registers {self.register_bank} do not match word size {self._spec_sheet}")

		if len({self._spec_sheet.endianness, self.register_bank.endianness, self.ram.endianness}) != 1:
			raise ValueError(
				f"RAM {self.ram} or registers {self.register_bank} do not match endianness {self._spec_sheet}")

	def read_register(self, r: Registers) -> bytes:
		if r == Registers.ZERO:
			return as_byte(0) * self._spec_sheet.word_size
		return self.register_bank.read(as_byte(r.value))

	def write_register(self, r: Registers, data: bytes) -> None:
		if r == Registers.ZERO:
			pass
		self.register_bank.write(r.value, data)

	def read_ram(self, addr: bytes) -> bytes:
		return self.ram.read(addr)

	def write_ram(self, addr: bytes, w: bytes) -> None:
		self.ram.write(addr, w)

	def read_state(self, state: StateRegisterBitmask) -> bool:
		state_register: bytes = self.read_register(Registers.STATE)
		state_mask: bytes = state.value

		masked_state: bytes = apply_binary_operation(state_register, state_mask, bitwise_and)

		return bool(masked_state)

	def write_state(self, state: StateRegisterBitmask, v: bool) -> None:
		if self.read_state(state) != v:
			register: bytes = self.read_register(Registers.STATE)
			register = apply_binary_operation(register, state.value, bitwise_xor)
			self.write_register(Registers.STATE, register)

	def get_spec_sheet(self) -> SpecSheet:
		return self._spec_sheet

	def _reg_as_address(self, reg_or_idx: Union[Registers, int]) -> bytes:
		idx: int = reg_or_idx.value if isinstance(reg_or_idx, Registers) else reg_or_idx
		return self._spec_sheet.int_to_word(idx)

	def run(self) -> None:
		while True:  # TODO: halt execution when certain flag is set in state register
			self.cycle()

	def cycle(self) -> None:
		instruction: bytes = self._fetch_instruction()
		self._run_instruction(instruction)

	def _run_instruction(self, instruction: bytes) -> None:
		decoded_instruction: IInstruction = self.dispatcher.dispatch(instruction)
		decoded_instruction.execute(self)

	def _fetch_instruction(self) -> bytes:
		pc_register: bytes = self.read_register(Registers.PC)
		self.write_register(
			Registers.PC, self._spec_sheet.w_increase(pc_register, self._spec_sheet.instruction_size)[1])

		instruction_address: int = self._spec_sheet.word_to_int(pc_register)
		instruction_word_address: int = self._spec_sheet.word_size * (instruction_address // self._spec_sheet.word_size)

		if self._cached_instruction_word_addr != instruction_word_address:
			self._cached_instruction_word_addr = self._spec_sheet.int_to_word(instruction_word_address)
			self._instruction_buffer = self.read_ram(self._cached_instruction_word_addr)

		instruction_in_word_offset: int = instruction_address % self._spec_sheet.instruction_size
		return (
			self._instruction_buffer
			[instruction_in_word_offset:instruction_in_word_offset + self._spec_sheet.instruction_size]
		)
