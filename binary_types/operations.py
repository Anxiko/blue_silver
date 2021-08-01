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


def b_sub(b1: bytes, b2: bytes, endianness: Endianness) -> Tuple[bool, bytes]:
	if len(b1) != len(b2):
		raise ValueError(f"Operands ({b1}, {b2}) have different sizes")

	sz: int = len(b1)
	i_subtracted: int = bytes_to_int(b1, endianness, signed=True) - bytes_to_int(b2, endianness, signed=True)
	try:
		b_subtracted: bytes = int_to_bytes(i_subtracted, sz, endianness, signed=True)
		return False, b_subtracted
	except OverflowError:
		# In case of overflow, only one additional bit is needed to hold the entire number of the subtraction

		b_subtracted: bytes = int_to_bytes(i_subtracted, sz + 1, endianness)
		return True, b_subtracted[1:]  # Discard the first bit, since it contains the overflowed part


def b_increase(b1: bytes, v: int, endianness: Endianness) -> Tuple[bool, bytes]:
	b2: bytes = int_to_bytes(v, len(b1), endianness)

	return b_add(b1, b2, endianness)


def b_flip_sign(b: bytes, endianness: Endianness) -> bytes:
	"""
	Returns the flipped sign integer value. Because it is possible to overflow flipping the sign,
	the return value has a byte more than the given value.
	"""
	v: int = bytes_to_int(b, endianness, signed=True)

	"""
	In very specific cases, the result of this operation no longer fits in the same number of bytes it originally fit in.
	In particular, the lowest possible signed integer in X bytes, requires X+1 bytes when the sign is flipped.
	For example, -128 (0xFF), when flipped, becomes 128 (0x0080). The leading zeroes are necessary,
	since the most significant bit is reserved for the sign.
	
	In order to remain consistent, the function will always return the result in 1 more byte than it was given.
	"""
	v = -v
	return int_to_bytes(v, len(b) + 1, endianness, signed=True)


def bitwise_and(b1: int, b2: int) -> int:
	return b1 & b2


def bitwise_or(b1: int, b2: int) -> int:
	return b1 | b2


def bitwise_xor(b1: int, b2: int) -> int:
	return b1 ^ b2


def apply_binary_operation(bytes1: bytes, bytes2: bytes, op: Callable[[int, int], int]) -> bytes:
	return bytes(op(b1, b2) for b1, b2 in zip(bytes1, bytes2))
