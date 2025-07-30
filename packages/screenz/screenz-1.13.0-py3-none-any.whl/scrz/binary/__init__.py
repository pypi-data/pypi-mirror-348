import dataclasses
import errno
import functools
import importlib.abc
import importlib.resources
import os
import pathlib
import shutil
import sys
import tempfile
import typing

ROOT = importlib.resources.files(__package__)
PREFIX = 'scrz-'
FFMPEG = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'
FFPROBE = 'ffprobe.exe' if sys.platform == 'win32' else 'ffprobe'


@dataclasses.dataclass
class Binaries:
	ffmpeg: pathlib.Path
	ffprobe: pathlib.Path
	root: typing.Optional[pathlib.Path] = None
	environ: typing.Optional[dict[str, str]] = None
	temporary: bool = False

	def close(self) -> None:
		cleanup(self)


def prepare() -> Binaries:
	root = ROOT / sys.platform

	ffmpeg: typing.Union[importlib.abc.Traversable, pathlib.Path, str, None]
	ffprobe: typing.Union[importlib.abc.Traversable, pathlib.Path, str, None]

	ffmpeg = root / FFMPEG
	ffprobe = root / FFPROBE

	packaged = root.is_dir() and ffmpeg.is_file() and ffprobe.is_file()
	if not packaged:
		ffmpeg = shutil.which(FFMPEG)
		if ffmpeg is None:
			raise_missing(FFMPEG)
		ffmpeg = pathlib.Path(ffmpeg)

		ffprobe = shutil.which(FFPROBE)
		if ffprobe is None:
			raise_missing(FFPROBE)
		ffprobe = pathlib.Path(ffprobe)

		return Binaries(ffmpeg=ffmpeg, ffprobe=ffprobe)

	if isinstance(root, pathlib.Path):
		if typing.TYPE_CHECKING:
			assert isinstance(ffmpeg, pathlib.Path)
			assert isinstance(ffprobe, pathlib.Path)

		return Binaries(ffmpeg=ffmpeg, ffprobe=ffprobe, root=root, environ=make_environ(root))

	tmproot = pathlib.Path(tempfile.mkdtemp(prefix=PREFIX))
	try:
		extract(root, tmproot)

		ffmpeg = tmproot / FFMPEG
		ffprobe = tmproot / FFPROBE

		return Binaries(
			ffmpeg=ffmpeg,
			ffprobe=ffprobe,
			root=tmproot,
			environ=make_environ(tmproot),
			temporary=True,
		)

	except:
		shutil.rmtree(tmproot, ignore_errors=True)
		raise


def raise_missing(name: str) -> typing.NoReturn:
	raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), name)


def extract(source: importlib.abc.Traversable, destination: pathlib.Path) -> None:
	if source.is_dir():
		destination.mkdir(exist_ok=True)
		for src in source.iterdir():
			dst = destination / src.name
			extract(src, dst)

	elif source.is_file():
		opener = functools.partial(os.open, mode=0o0755)
		with source.open('rb') as fp_src, open(destination, 'xb', opener=opener) as fp_dst:
			shutil.copyfileobj(fp_src, fp_dst)


def make_environ(root: typing.Union[os.PathLike[str], str]) -> dict[str, str]:
	root = os.fspath(root)
	result = dict(os.environ)

	key = 'PATH'
	value = result.get(key)
	if value:
		value = root + os.pathsep + value
	else:
		value = root

	result[key] = value

	if sys.platform == 'win32':
		return result
	elif sys.platform == 'darwin':
		key = 'DYLD_FALLBACK_LIBRARY_PATH'
	else:
		key = 'LD_LIBRARY_PATH'

	value = result.get(key)
	if value:
		value = root + os.pathsep + value
	else:
		value = root

	result[key] = value
	return result


def cleanup(binaries: Binaries) -> None:
	if binaries.root is not None and binaries.temporary:
		shutil.rmtree(binaries.root, ignore_errors=True)
