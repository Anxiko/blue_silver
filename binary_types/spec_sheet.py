from dataclasses import dataclass
from typing import Tuple

from .conversions import int_to_bytes, bytes_to_int
from .endianness import Endianness
from .operations import b_add, b_increase, b_sub


@dataclass
class SpecSheet:
	endianness: Endianness
	word_size: int
	instruction_size: int
	address_size: int

	def int_to_word(self, v: int, *, signed: bool = False) -> bytes:
		return int_to_bytes(v, self.word_size, self.endianness, signed=signed)

	def word_to_int(self, w: bytes, *, signed: bool = False) -> int:
		return bytes_to_int(w, self.endianness, signed=signed)

	def w_add(self, w1: bytes, w2: bytes) -> Tuple[bool, bytes]:
		return b_add(w1, w2, self.endianness)

	def w_sub(self, w1: bytes, w2: bytes) -> Tuple[bool, bytes]:
		return b_sub(w1, w2, self.endianness)

	def w_increase(self, w: bytes, v: int) -> Tuple[bool, bytes]:
		return b_increase(w, v, self.endianness)

	def get_least_significant_bytes(self, w: bytes, n_bytes: int) -> bytes:
		if len(w) != self.word_size:
			raise ValueError(f"Given word size length ({len(w)}) doesn't match specified word size ({len(w)})")

		if n_bytes < 0:
			raise ValueError(f"Number of bytes ({n_bytes}) must be positive")

		if n_bytes > len(w):
			raise ValueError(f"Number of bytes ({n_bytes}) exceeds word size ({len(w)})")

		if self.endianness == Endianness.BIG_ENDIAN:
			return w[len(w) - n_bytes:len(w)]
		elif self.endianness == Endianness.LITTLE_ENDIAN:
			return w[0:n_bytes]
		else:
			raise ValueError(f"Unknown endianness ({self.endianness})")

	def left_pad(self, b: bytes) -> bytes:
		if len(b) > self.word_size:
			raise ValueError(f"Given value is longer ({len(b)}) than word size ({self.word_size})")
		if self.endianness == Endianness.BIG_ENDIAN:
			return b'\x00' * (self.word_size - len(b)) + b
		elif self.endianness == Endianness.LITTLE_ENDIAN:
			return b + b'\x00' * (self.word_size - len(b))
		raise ValueError(f"Unknown endianness ({self.endianness})")
