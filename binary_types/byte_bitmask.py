from .conversions import from_byte, as_byte


class ByteBitmask:
	n_bits: int
	right_shift: int

	_bitmask: int

	def __init__(self, n_bits: int, right_shift: int):
		self.n_bits = n_bits
		self.right_shift = right_shift

		if self.right_shift < 0:
			raise ValueError("Right shift can't be < 0")
		if self.n_bits < 1:
			raise ValueError("Number of bits has to be > 1")
		if self.n_bits + self.right_shift > 8:
			raise ValueError(
				f"Specified right shift ({self.right_shift}) and number of bits ({self.n_bits}) won't fit in a byte")

		self._bitmask = 0
		for idx in range(self.n_bits):
			self._bitmask |= 1 << idx

	def extract_from_byte(self, b: bytes) -> bytes:
		n: int = from_byte(b) >> self.right_shift
		return as_byte(self._bitmask & n)

	def to_masked_byte(self, b: bytes) -> bytes:
		n: int = from_byte(b) & self._bitmask
		return as_byte(n << self.right_shift)
