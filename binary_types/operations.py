from typing import Tuple, Callable

from .conversions import int_to_bytes, bytes_to_int
from .endianness import Endianness


def b_add(b1: bytes, b2: bytes, endianness: Endianness) -> Tuple[bool, bytes]:
	if len(b1) != len(b2):
		raise ValueError(f"Operands ({b1}, {b2}) have different sizes")

	sz: int = len(b1)
	i_added: int = bytes_to_int(b1, endianness) + bytes_to_int(b2, endianness)

	try:
		b_added: bytes = int_to_bytes(i_added, sz, endianness)
		return False, b_added
	except OverflowError:
		# In case of overflow, only one additional bit is needed to hold the entire number of the addition

		b_added: bytes = int_to_bytes(i_added, sz + 1, endianness)
		return True, b_added[1:]  # Discard the first bit, since it contains the overflowed part


def b_increase(b1: bytes, v: int, endianness: Endianness) -> Tuple[bool, bytes]:
	b2: bytes = int_to_bytes(v, len(b1), endianness)

	return b_add(b1, b2, endianness)


def bitwise_and(b1: int, b2: int) -> int:
	return b1 & b2


def bitwise_or(b1: int, b2: int) -> int:
	return b1 | b2


def bitwise_xor(b1: int, b2: int) -> int:
	return b1 ^ b2


def apply_binary_operation(bytes1: bytes, bytes2: bytes, op: Callable[[int, int], int]) -> bytes:
	return bytes(op(b1, b2) for b1, b2 in zip(bytes1, bytes2))
