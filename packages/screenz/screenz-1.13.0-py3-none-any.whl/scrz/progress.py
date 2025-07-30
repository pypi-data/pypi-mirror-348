import importlib
import sys
import time
import typing


def normalize(value: float) -> float:
	if value < 0.0:
		return 0.0
	elif value > 1.0:
		return 1.0
	else:
		return value


def make_progress(position: int, total: int) -> float:
	if total:
		return normalize(position / total)
	else:
		return 0.0


class SimpleProgress:
	def __init__(self, stream: typing.TextIO) -> None:
		self.stream = stream

	def __call__(self, text: str, value: float) -> None:
		value = normalize(value) * 100.0
		self.stream.write('[{:5.1f}%] {}\n'.format(value, text))
		self.stream.flush()


class ConsoleProgress:
	def __init__(self, stream: typing.TextIO) -> None:
		if sys.platform == 'win32':
			colorama = importlib.import_module('colorama')
			colorama.just_fix_windows_console()

		self.stream: typing.Optional[typing.TextIO] = stream
		self.last: typing.Optional[float] = None

	def __call__(self, text: str, value: float) -> None:
		if self.stream is None:
			return

		now = time.monotonic()
		value = normalize(value) * 100.0
		update = self.last is None or now - self.last >= 0.1 or value >= 100.0

		if not update:
			return

		self.stream.write('\r\x1b[2K\x1b[1m[{:5.1f}%]\x1b[0m {}'.format(value, text))
		self.stream.flush()
		self.last = now

	def close(self) -> None:
		if self.stream is None:
			return

		if self.last is not None:
			self.stream.write('\r\x1b[2K')
			self.stream.flush()

		self.last = None
		self.stream = None


class StepProgress:
	def __init__(
		self, parent: typing.Callable[[str, float], None], scale: float, offset: float
	) -> None:
		self.parent = parent
		self.scale = scale
		self.offset = offset

	def __call__(self, text: str, value: float) -> None:
		value = normalize(value)
		value = value * self.scale + self.offset
		value = normalize(value)
		self.parent(text, value)

	@classmethod
	def create(
		cls,
		parent: typing.Optional[typing.Callable[[str, float], None]] = None,
		*weight: typing.Union[int, float],
	) -> list[typing.Optional[typing.Self]]:
		if not weight:
			return []
		if parent is None:
			return [None] * len(weight)

		total = sum(weight)
		offset = 0.0

		result: list[typing.Optional[typing.Self]] = []
		for w in weight:
			scale = w / total
			result.append(cls(parent, scale, offset))
			offset += scale

		return result
