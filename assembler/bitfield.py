from dataclasses import dataclass


@dataclass
class BitField:
	bit_length: int
	bits: bytes

	def __post_init__(self):
		if self.bit_length > len(self.bits) * 8:
			raise ValueError(f"Specified bit length doesn't fit in given bits")
