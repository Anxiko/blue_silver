from typing import List

from interfaces import IInstruction, ICpu, CodeOp


class NoOperation(IInstruction):
	@classmethod
	def get_codeop(cls) -> CodeOp:
		return CodeOp('NOOP', [], b'\x00', b'\xff')

	@classmethod
	def from_assembly(cls, text_code: str, arguments: List[str]) -> 'IInstruction':
		if text_code != cls.get_codeop().text_code:
			raise ValueError(f"Text code {text_code} doesn't match the instruction's text code")

		return cls(cls.get_codeop().byte_code)

	def execute(self, cpu: ICpu) -> None:
		pass
