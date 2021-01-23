from dataclasses import dataclass
from typing import Tuple

from .conversions import int_to_bytes, bytes_to_int
from .endianness import Endianness
from .operations import b_add, b_increase


@dataclass
class SpecSheet:
	endianness: Endianness

	word_size: int

	register_bank_size_words: int
	ram_size_words: int

	ram_address_bus_size: int
	register_address_bus_size: int

	def int_to_word(self, v: int) -> bytes:
		return int_to_bytes(v, self.word_size, self.endianness)

	def word_to_int(self, b: bytes) -> int:
		return bytes_to_int(b, self.endianness)

	def w_add(self, w1: bytes, w2: bytes) -> Tuple[bool, bytes]:
		return b_add(w1, w2, self.endianness)

	def w_increase(self, w: bytes, v: int) -> Tuple[bool, bytes]:
		return b_increase(w, v, self.endianness)
