from .endianness import Endianness


def bytes_to_int(b: bytes, endianness: Endianness, *, signed: bool = False) -> int:
	return int.from_bytes(b, endianness.value, signed=signed)


def int_to_bytes(v: int, sz: int, endianness: Endianness, *, signed: bool = False) -> bytes:
	return v.to_bytes(sz, endianness.value, signed=signed)


def as_byte(v: int) -> bytes:
	return int_to_bytes(v, 1, Endianness.BIG_ENDIAN)  # Endianness doesn't matter for a single byte


def from_byte(b: bytes) -> int:
	return bytes_to_int(b, Endianness.BIG_ENDIAN)  # Endianness doesn't matter for a single byte
