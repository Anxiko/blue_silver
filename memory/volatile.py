from math import log
from typing import Optional

from binary_types import bytes_to_int, Endianness


class VolatileMemory:
	_data: bytearray

	data_bus_size: int
	address_bus_size: int
	endianness: Endianness

	def __init__(
			self, size: int, data_bus_size: int, address_bus_size: int, endianness: Endianness,
			initial: Optional[bytes] = None
	):
		if size % data_bus_size != 0:
			raise ValueError(f"Requested size ({size}) misaligned with given address bus size ({address_bus_size})")

		if log(size, 2 ** 8) > address_bus_size:
			raise ValueError(f"Address bus size ({address_bus_size}) can't cover requested memory size ({size})")

		self._data = bytearray(size)
		if initial is not None:
			if len(initial) > size:
				raise ValueError(
					f"Initial memory contents are greater {len(initial)} than the memory's capacity {size}")
			self._data[:len(initial)] = initial

		self.data_bus_size = data_bus_size
		self.address_bus_size = address_bus_size
		self.endianness = endianness

	def _get_address_int(self, address: bytes) -> int:
		if len(address) != self.address_bus_size:
			raise ValueError(f"Given address ({address}) does not match address bus size ({self.address_bus_size})")

		idx: int = bytes_to_int(address, self.endianness)
		if idx % self.data_bus_size != 0:
			raise ValueError(f"Address ({address}) is misaligned with data bus size ({self.data_bus_size})")

		if idx >= len(self._data):
			raise ValueError(f"Address ({address}) is out of bounds")

		return idx

	def read(self, address: bytes) -> bytes:
		index: int = self._get_address_int(address)

		return bytes(self._data[index:index + self.data_bus_size])

	def write(self, address: bytes, value: bytes) -> None:
		index: int = self._get_address_int(address)

		if len(value) != self.data_bus_size:
			raise ValueError(f"Given data size ({value}) does not match data bus size ({self.data_bus_size})")

		self._data[index:index + self.data_bus_size] = value

	def __len__(self) -> int:
		return len(self._data)

	def get_data(self) -> bytearray:
		return self._data
