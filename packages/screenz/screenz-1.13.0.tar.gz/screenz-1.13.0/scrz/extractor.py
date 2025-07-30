import collections.abc
import concurrent.futures
import contextlib
import dataclasses
import enum
import json
import os
import pathlib
import random
import subprocess
import typing

import PIL.Image

from .progress import StepProgress, make_progress
from .scanner import Extensions, Scanner, StrPath
from .swapper import simple_loader

T = typing.TypeVar('T')

IMAGES: collections.abc.Container[str] = Extensions(
	'.bmp', '.gif', '.jpe', '.jpg', '.jpeg', '.png', '.webp'
)
VIDEOS: collections.abc.Container[str] = Extensions(
	'.3gp',
	'.asf',
	'.avi',
	'.f4v',
	'.flv',
	'.m4v',
	'.mkv',
	'.mov',
	'.mpg',
	'.mpeg',
	'.mp4',
	'.mts',
	'.ts',
	'.webm',
	'.wmv',
)
OFFSET = 1.0 / 3.0
PRECISION = 3


@dataclasses.dataclass(eq=False, kw_only=True)
class Information:
	name: str
	size: typing.Optional[int] = None
	duration: typing.Optional[float] = None
	resolution: typing.Optional[tuple[int, int]] = None
	frame_rate: typing.Optional[float] = None
	video_codec: typing.Optional[str] = None
	video_rate: typing.Optional[int] = None
	audio_codec: typing.Optional[str] = None
	audio_rate: typing.Optional[int] = None


class Order(enum.Enum):
	NONE = enum.auto()
	DEFAULT = enum.auto()
	REVERSE = enum.auto()
	SHORTEST = enum.auto()
	LONGEST = enum.auto()
	RANDOM = enum.auto()


class Verbosity(enum.IntEnum):
	QUIET = -8
	PANIC = 0
	FATAL = 8
	ERROR = 16
	WARNING = 24
	INFO = 32
	VERBOSE = 40
	DEBUG = 48
	TRACE = 56


class Scale(enum.Enum):
	BOX = enum.auto()
	WIDTH = enum.auto()
	HEIGHT = enum.auto()
	OVER = enum.auto()
	CROP = enum.auto()


@dataclasses.dataclass(eq=False, kw_only=True)
class Extractor:
	scanner: Scanner = dataclasses.field(default_factory=Scanner)
	count: int = 0
	order: Order = Order.NONE
	window: typing.Optional[slice] = None
	offset: float = OFFSET
	size: typing.Optional[int] = None
	scale: Scale = Scale.BOX
	ffmpeg: typing.Optional[StrPath] = None
	ffprobe: typing.Optional[StrPath] = None
	root: typing.Optional[StrPath] = None
	environ: typing.Optional[dict[str, str]] = None
	loader: typing.Optional[typing.Callable[[bytes, str], PIL.Image.Image]] = None
	progress: typing.Optional[typing.Callable[[str, float], None]] = None
	debug: typing.Optional[typing.Callable[[tuple[str, ...]], None]] = None
	verbosity: typing.Optional[Verbosity] = None
	executor: typing.Optional[concurrent.futures.Executor] = None
	randomizer: typing.Optional[random.Random] = None

	@contextlib.contextmanager
	def step(
		self, progress: typing.Optional[typing.Callable[[str, float], None]]
	) -> collections.abc.Iterator[None]:
		previous = self.progress
		try:
			self.progress = progress
			yield None
		finally:
			self.progress = previous


Frame = typing.Optional[PIL.Image.Image]
Frames = list[tuple[float, Frame]]


def extract_information(extractor: Extractor, path: StrPath) -> Information:
	path = os.fspath(path)
	result = Information(name=os.path.basename(path))

	try:
		result.size = os.path.getsize(path)
	except OSError:
		pass

	verbosity = extractor.verbosity
	if verbosity is None:
		verbosity = Verbosity.QUIET

	args = [
		'ffprobe',
		'-v',
		verbosity.name.lower(),
		'-print_format',
		'json',
		'-show_entries',
		'format=duration:stream=codec_type,codec_name,bit_rate,avg_frame_rate,width,height',
		'-i',
		path,
	]

	if extractor.debug is not None:
		extractor.debug(tuple(args))

	process = subprocess.run(
		args=args,
		executable=extractor.ffprobe,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL if verbosity < 0 else None,
		cwd=extractor.root,
		env=extractor.environ,
		encoding='utf-8',
	)

	if process.returncode:
		return result

	try:
		data: object = json.loads(process.stdout)
	except json.JSONDecodeError:
		return result

	empty_dict: dict[str, object] = {}

	def ensure_dict(input: object) -> dict[str, object]:
		return input if isinstance(input, dict) else empty_dict

	empty_list: list[object] = []

	def ensure_list(input: object) -> list[object]:
		return input if isinstance(input, list) else empty_list

	TValue = typing.TypeVar('TValue', str, int, float, bool)

	def ensure_value(type: typing.Type[TValue], input: object) -> typing.Optional[TValue]:
		if not isinstance(input, (str, int, float, bool)):
			return None
		try:
			return type(input)
		except ValueError:
			return None

	def ensure_rate(input: object) -> typing.Optional[float]:
		if isinstance(input, (int, float, bool)):
			return float(input)
		elif not isinstance(input, str):
			return None

		split = input.split('/', 1)
		if len(split) == 1:
			split.append('1')
		elif len(split) != 2:
			return None

		try:
			numerator = int(split[0])
			denominator = int(split[1])
		except ValueError:
			return None

		try:
			return numerator / denominator
		except ZeroDivisionError:
			return None

	info = ensure_dict(data)
	format = ensure_dict(info.get('format'))
	streams = ensure_list(info.get('streams'))

	result.duration = ensure_value(float, format.get('duration'))

	video_stream = empty_dict
	audio_stream = empty_dict

	for stream in map(ensure_dict, streams):
		codec_type = stream.get('codec_type')
		if codec_type == 'video' and video_stream is empty_dict:
			video_stream = stream
		elif codec_type == 'audio' and audio_stream is empty_dict:
			audio_stream = stream

	width = ensure_value(int, video_stream.get('width'))
	height = ensure_value(int, video_stream.get('height'))
	if width is not None and height is not None and (width or height):
		result.resolution = (width, height)

	result.frame_rate = ensure_rate(video_stream.get('avg_frame_rate'))

	result.video_codec = ensure_value(str, video_stream.get('codec_name'))
	result.video_rate = ensure_value(int, video_stream.get('bit_rate'))
	result.audio_codec = ensure_value(str, audio_stream.get('codec_name'))
	result.audio_rate = ensure_value(int, audio_stream.get('bit_rate'))

	return result


def seek_indexed(
	duration: typing.Optional[float], index: int, count: int
) -> typing.Optional[float]:
	return None if duration is None else round((index + 0.5) * (duration / count), PRECISION)


def seek_offset(duration: typing.Optional[float], offset: float = OFFSET) -> typing.Optional[float]:
	return None if duration is None else round(duration * offset, PRECISION)


def extract_frame(
	extractor: Extractor, path: StrPath, seek: typing.Optional[float] = None
) -> Frame:
	path = os.fspath(path)

	filters: list[str] = []
	if extractor.size is not None:
		if extractor.scale == Scale.BOX:
			filters.append(
				'scale={0}:{0}:force_original_aspect_ratio=decrease'.format(extractor.size)
			)
		elif extractor.scale == Scale.WIDTH:
			filters.append('scale={}:-1'.format(extractor.size))
		elif extractor.scale == Scale.HEIGHT:
			filters.append('scale=-1:{}'.format(extractor.size))
		elif extractor.scale == Scale.OVER:
			filters.append(
				'scale={0}:{0}:force_original_aspect_ratio=increase'.format(extractor.size)
			)
		elif extractor.scale == Scale.CROP:
			filters.extend(['crop=min(iw\\,ih):min(iw\\,ih)', 'scale={}:-1'.format(extractor.size)])

	filters.extend(['format=rgb24', 'setsar=1', 'setdar=a'])

	verbosity = extractor.verbosity
	if verbosity is None:
		verbosity = Verbosity.ERROR

	args = [
		'ffmpeg',
		'-hide_banner',
		'-nostats',
		'-loglevel',
		verbosity.name.lower(),
		'-threads',
		'1',
		'-filter_threads',
		'1',
	]

	if seek is not None:
		args.extend(('-ss', str(seek)))

	args.extend(
		(
			'-an',
			'-sn',
			'-dn',
			'-i',
			path,
			'-map_metadata',
			'-1',
			'-filter:v',
			','.join(filters),
			'-frames:v',
			'1',
			'-codec:v',
			'ppm',
			'-f',
			'image2pipe',
			'-',
		)
	)

	if extractor.debug is not None:
		extractor.debug(tuple(args))

	process = subprocess.run(
		args,
		executable=extractor.ffmpeg,
		stdin=subprocess.DEVNULL,
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL if verbosity < 0 else None,
		cwd=extractor.root,
		env=extractor.environ,
	)

	if process.returncode or not process.stdout:
		return None

	loader = extractor.loader
	if loader is None:
		loader = simple_loader

	return loader(process.stdout, 'PPM')


def extract_frames(
	extractor: Extractor, path: StrPath, *, duration: typing.Optional[float] = None
) -> Frames:
	def callback(index: int) -> tuple[float, Frame]:
		seek = seek_indexed(duration, index, extractor.count)
		image = extract_frame(extractor, path, seek)
		return seek or 0.0, image

	mapper = map if extractor.executor is None else extractor.executor.map
	iterator = mapper(callback, range(extractor.count))

	if extractor.progress is None:
		return list(iterator)

	name = os.path.basename(path)
	extractor.progress(name, 0.0)

	result: list[tuple[float, Frame]] = []
	for index, frame in enumerate(iterator):
		extractor.progress(name, make_progress(index + 1, extractor.count))
		result.append(frame)

	return result


def extract_directory_paths(extractor: Extractor, path: StrPath) -> list[pathlib.Path]:
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	iterator = extractor.scanner.scan(path)
	return finalize_result(extractor, iterator, lambda x: (x.name, 0.0))


def extract_directory_infos(
	extractor: Extractor, path: StrPath
) -> list[tuple[pathlib.Path, Information]]:
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	def callback(path: pathlib.Path) -> tuple[pathlib.Path, Information]:
		info = extract_information(extractor, path)
		return path, info

	extended = is_extended_order(extractor.order)
	with override_order(extractor, Order.NONE, None, extended):
		files = extract_directory_paths(extractor, path)

	mapper = map if extractor.executor is None else extractor.executor.map
	iterator = mapper(callback, files)

	result: list[tuple[pathlib.Path, Information]] = []
	for index, data in enumerate(iterator):
		if extractor.progress is not None:
			extractor.progress(data[0].name, make_progress(index + 1, len(files)))
		result.append(data)

	if extended:
		result = finalize_result(extractor, result, lambda x: (x[0].name, x[1].duration or 0.0))

	return result


def extract_directory_frames(
	extractor: Extractor, path: StrPath
) -> list[tuple[pathlib.Path, Information, Frames]]:
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	def callback(
		path: pathlib.Path, info: Information, index: int
	) -> tuple[pathlib.Path, float, Frame]:
		seek = seek_indexed(info.duration, index, extractor.count)
		image = extract_frame(extractor, path, seek)
		return path, seek or 0.0, image

	steps = StepProgress.create(extractor.progress, 1, extractor.count)
	with extractor.step(steps[0]), extractor.scanner.specialize(VIDEOS):
		videos = extract_directory_infos(extractor, path)

	mapper = map if extractor.executor is None else extractor.executor.map
	work = ((path, info, index) for (path, info) in videos for index in range(extractor.count))
	iterator = mapper(callback, *zip(*work))
	del work

	result: dict[pathlib.Path, tuple[Information, Frames]] = {
		path: (info, []) for (path, info) in videos
	}

	for index, data in enumerate(iterator):
		if steps[1] is not None:
			steps[1](data[0].name, make_progress(index + 1, len(videos) * extractor.count))
		result[data[0]][1].append(data[1:])

	return [(path, info, frames) for (path, (info, frames)) in result.items()]


def extract_directory_videos(
	extractor: Extractor, path: StrPath
) -> list[tuple[pathlib.Path, Information, Frame]]:
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	def callback(path: pathlib.Path) -> tuple[pathlib.Path, Information, Frame]:
		info = extract_information(extractor, path)
		seek = seek_offset(info.duration, extractor.offset)
		image = extract_frame(extractor, path, seek)
		return path, info, image

	extended = is_extended_order(extractor.order)
	with (
		override_order(extractor, Order.NONE, None, extended),
		extractor.scanner.specialize(VIDEOS),
	):
		videos = extract_directory_paths(extractor, path)

	mapper = map if extractor.executor is None else extractor.executor.map
	iterator = mapper(callback, videos)

	result: list[tuple[pathlib.Path, Information, Frame]] = []
	for index, data in enumerate(iterator):
		if extractor.progress is not None:
			extractor.progress(data[0].name, make_progress(index + 1, len(videos)))
		result.append(data)

	if extended:
		result = finalize_result(extractor, result, lambda x: (x[0].name, x[1].duration or 0.0))

	return result


def extract_directory_images(
	extractor: Extractor, path: StrPath
) -> list[tuple[pathlib.Path, Frame]]:
	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	def callback(path: pathlib.Path) -> tuple[pathlib.Path, Frame]:
		image = extract_frame(extractor, path)
		return path, image

	with extractor.scanner.specialize(IMAGES):
		images = extract_directory_paths(extractor, path)

	mapper = map if extractor.executor is None else extractor.executor.map
	iterator = mapper(callback, images)

	if extractor.progress is None:
		return list(iterator)

	result: list[tuple[pathlib.Path, Frame]] = []
	for index, data in enumerate(iterator):
		extractor.progress(data[0].name, make_progress(index + 1, len(images)))
		result.append(data)

	return result


def is_extended_order(order: Order) -> bool:
	return order in (Order.SHORTEST, Order.LONGEST)


@contextlib.contextmanager
def override_order(
	extractor: Extractor, order: Order, window: typing.Optional[slice], override: bool
) -> collections.abc.Iterator[None]:
	order_old = extractor.order
	window_old = extractor.window
	try:
		if override:
			extractor.order = order
			extractor.window = window

		yield None
	finally:
		extractor.window = window_old
		extractor.order = order_old


def finalize_result(
	extractor: Extractor,
	result: collections.abc.Iterable[T],
	converter: typing.Callable[[T], tuple[str, float]],
) -> list[T]:
	def name_key(item: T) -> tuple[str, str]:
		data = converter(item)
		return data[0].casefold(), data[0]

	def duration_key0(item: T) -> tuple[float, str, str]:
		data = converter(item)
		return data[1], data[0].casefold(), data[0]

	def duration_key1(item: T) -> tuple[float, str, str]:
		data = converter(item)
		return -data[1], data[0].casefold(), data[0]

	if extractor.order == Order.NONE:
		result = list(result)
	elif extractor.order == Order.DEFAULT:
		result = sorted(result, key=name_key)
	elif extractor.order == Order.REVERSE:
		result = sorted(result, key=name_key, reverse=True)
	elif extractor.order == Order.SHORTEST:
		result = sorted(result, key=duration_key0)
	elif extractor.order == Order.LONGEST:
		result = sorted(result, key=duration_key1)
	elif extractor.order == Order.RANDOM:
		shuffle = random.shuffle if extractor.randomizer is None else extractor.randomizer.shuffle
		result = list(result)
		shuffle(result)
	else:
		typing.assert_never(extractor.order)

	if extractor.window is not None:
		result = result[extractor.window]

	return result
