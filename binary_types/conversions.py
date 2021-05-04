from .endianness import Endianness


def bytes_to_int(b: bytes, endianness: Endianness) -> int:
	return int.from_bytes(b, endianness.value)


def int_to_bytes(v: int, sz: int, endianness: Endianness) -> bytes:
	return v.to_bytes(sz, endianness.value)


def as_byte(v: int) -> bytes:
	return int_to_bytes(v, 1, Endianness.BIG_ENDIAN)  # Endianness doesn't matter for a single byte


def from_byte(b: bytes) -> int:
	return bytes_to_int(b, Endianness.BIG_ENDIAN) # Endianness doesn't matter for a single byte
