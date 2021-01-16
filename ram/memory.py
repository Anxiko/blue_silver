from math import log


class Memory:
	_ENDIANNESS: str = 'big'

	_data: bytearray

	_data_bus_size: int
	_address_bus_size: int

	def __init__(self, size: int, data_bus_size: int, address_bus_size: int):
		if log(size, 2 ** 8) > address_bus_size:
			raise ValueError(f"Address size ({address_bus_size}) can't cover requested memory size ({size})")

		self._data = bytearray(size)
		self._data_bus_size = data_bus_size
		self._address_bus_size = address_bus_size

	def _get_address_int(self, address: bytes) -> int:
		if len(address) != self._address_bus_size:
			raise ValueError(f"Given address ({address}) does not match address bus size ({self._address_bus_size})")

		idx: int = int.from_bytes(address, type(self)._ENDIANNESS)
		if idx % self._data_bus_size != 0:
			raise ValueError(f"Address ({address}) is misaligned with data bus size ({self._data_bus_size})")

		if idx >= len(self._data):
			raise ValueError(f"Address ({address}) is out of bounds")

		return idx

	def read(self, address: bytes) -> bytes:
		index: int = self._get_address_int(address)

		return bytes(self._data[index:index + self._data_bus_size])

	def write(self, address: bytes, value: bytes) -> None:
		index: int = self._get_address_int(address)

		if len(value) != self._data_bus_size:
			raise ValueError(f"Given data size ({value}) does not match data bus size ({self._data_bus_size})")

		self._data[index:index + self._data_bus_size] = value

	def __len__(self) -> int:
		return len(self._data)

	def get_data(self) -> bytearray:
		return self._data
