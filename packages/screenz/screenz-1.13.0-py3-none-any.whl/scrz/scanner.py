import collections.abc
import contextlib
import dataclasses
import fnmatch
import os
import pathlib
import typing

TPathObject = typing.TypeVar('TPathObject', bound=pathlib.PurePath)
StrPath = typing.Union[os.PathLike[str], str]


class Star(collections.abc.Container[str]):
	def __contains__(self, x: object, /) -> bool:
		return isinstance(x, str)

	def __str__(self) -> str:
		return '*'

	def __repr__(self) -> str:
		return repr('*')


class Extensions(collections.abc.Set[str]):
	def __init__(self, *extensions: str) -> None:
		self.raw = frozenset(map(str.casefold, extensions))

	def __len__(self) -> int:
		return len(self.raw)

	def __iter__(self) -> collections.abc.Iterator[str]:
		return iter(self.raw)

	def __contains__(self, x: object, /) -> bool:
		return isinstance(x, str) and x.casefold() in self.raw

	def __str__(self) -> str:
		return ';'.join('*' + extension for extension in sorted(self.raw))

	def __repr__(self) -> str:
		return '{}({})'.format(self.__class__.__name__, ', '.join(map(repr, sorted(self.raw))))


@dataclasses.dataclass(eq=False, kw_only=True)
class Scanner:
	extensions: collections.abc.Container[str] = Star()
	follow_symlinks: bool = False
	ignore_patterns: collections.abc.Iterable[str] = ()
	recurse: bool = True

	@contextlib.contextmanager
	def specialize(
		self, extensions: collections.abc.Container[str]
	) -> collections.abc.Iterator[None]:
		previous = self.extensions
		try:
			if isinstance(self.extensions, Star):
				self.extensions = extensions

			yield None
		finally:
			self.extensions = previous

	@typing.overload
	def scan(self, path: TPathObject) -> collections.abc.Iterator[TPathObject]: ...

	@typing.overload
	def scan(self, path: os.PathLike[str]) -> collections.abc.Iterator[os.PathLike[str]]: ...

	@typing.overload
	def scan(self, path: str) -> collections.abc.Iterator[str]: ...

	def scan(self, path: StrPath) -> collections.abc.Iterator[StrPath]:
		return scan(self, path)


@typing.overload
def scan(scanner: Scanner, path: TPathObject) -> collections.abc.Iterator[TPathObject]: ...


@typing.overload
def scan(
	scanner: Scanner, path: os.PathLike[str]
) -> collections.abc.Iterator[os.PathLike[str]]: ...


@typing.overload
def scan(scanner: Scanner, path: str) -> collections.abc.Iterator[str]: ...


def scan(scanner: Scanner, path: StrPath) -> collections.abc.Iterator[StrPath]:
	for entry in os.scandir(path):
		if any(fnmatch.fnmatchcase(entry.name, pattern) for pattern in scanner.ignore_patterns):
			continue

		sub_path: StrPath
		if isinstance(path, pathlib.PurePath):
			sub_path = path / entry.name
		elif isinstance(path, os.PathLike):
			sub_path = entry
		elif isinstance(path, str):
			sub_path = os.fspath(entry)
		else:
			typing.assert_never(path)

		if entry.is_dir(follow_symlinks=scanner.follow_symlinks):
			if scanner.recurse:
				yield from scanner.scan(sub_path)

		elif (
			entry.is_file(follow_symlinks=scanner.follow_symlinks)
			and os.path.splitext(entry.name)[1] in scanner.extensions
		):
			yield sub_path
