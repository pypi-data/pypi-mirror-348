import collections.abc
import concurrent.futures
import contextlib
import dataclasses
import enum
import os
import pathlib
import random
import shlex
import subprocess
import sys
import types
import typing

from .binary import prepare as prepare_binaries
from .configuration import Options as BaseOptions
from .configuration import (
	configure_histogram,
	configure_image_collage,
	configure_video,
	configure_video_collage,
)
from .configuration import update as update_configuration
from .extractor import Extractor, Order, Verbosity
from .generator import (
	Generator,
	compose,
	generate_histogram,
	generate_image_collage,
	generate_video,
	generate_video_collage,
	generate_video_recursive,
)
from .progress import ConsoleProgress, SimpleProgress, StepProgress, make_progress
from .scanner import Scanner
from .swapper import Swapper


class Type(enum.Enum):
	SINGLE = enum.auto()
	RECURSIVE = enum.auto()
	VIDEOS = enum.auto()
	IMAGES = enum.auto()
	HISTOGRAM = enum.auto()


class Options(BaseOptions, typing.Protocol):
	@property
	def input(self) -> pathlib.Path: ...
	@property
	def output(self) -> pathlib.Path: ...
	@property
	def type(self) -> typing.Optional[Type]: ...
	@property
	def extensions(self) -> typing.Optional[collections.abc.Container[str]]: ...
	@property
	def follow(self) -> typing.Optional[bool]: ...
	@property
	def ignore(self) -> typing.Optional[collections.abc.Iterable[str]]: ...
	@property
	def verbosity(self) -> typing.Optional[Verbosity]: ...
	@property
	def order(self) -> typing.Optional[Order]: ...
	@property
	def seed(self) -> typing.Optional[int]: ...
	@property
	def window(self) -> typing.Optional[slice]: ...
	@property
	def filename(self) -> typing.Optional[str]: ...
	@property
	def threads(self) -> typing.Optional[int]: ...
	@property
	def progress(self) -> typing.Optional[bool]: ...
	@property
	def debug(self) -> typing.Optional[bool]: ...


@dataclasses.dataclass(eq=False, kw_only=True)
class Context(contextlib.AbstractContextManager['Context']):
	generator: Generator
	type: Type
	input: pathlib.Path
	output: pathlib.Path
	filename_format: str
	close: typing.Optional[list[typing.Callable[[], None]]] = None

	def __enter__(self) -> typing.Self:
		return self

	def __exit__(
		self,
		exc_type: typing.Optional[typing.Type[BaseException]],
		exc_value: typing.Optional[BaseException],
		traceback: typing.Optional[types.TracebackType],
	) -> None:
		if self.close is None:
			return None

		close = self.close
		self.close = None
		for callable in close:
			callable()
		return None


def print_args(args: tuple[str, ...]) -> None:
	if sys.platform == 'win32':
		print(subprocess.list2cmdline(args), file=sys.stderr)
	else:
		print(' '.join(map(shlex.quote, args)), file=sys.stderr)


def create_context(options: Options) -> Context:
	type = options.type
	if type is None:
		type = Type.SINGLE

	if type == Type.SINGLE or type == Type.RECURSIVE:
		configuration = configure_video()
	elif type == Type.VIDEOS:
		configuration = configure_video_collage()
	elif type == Type.IMAGES:
		configuration = configure_image_collage()
	elif type == Type.HISTOGRAM:
		configuration = configure_histogram()
	else:
		typing.assert_never(type)

	scanner = Scanner()
	if options.extensions is not None:
		scanner.extensions = options.extensions
	if options.follow is not None:
		scanner.follow_symlinks = options.follow
	if options.ignore is not None:
		scanner.ignore_patterns = options.ignore

	update_configuration(configuration, options)

	close: list[typing.Callable[[], None]] = []

	order = options.order
	if order is None:
		order = Order.DEFAULT

	binaries = prepare_binaries()
	if binaries.temporary:
		close.append(binaries.close)

	extractor = Extractor(
		scanner=scanner,
		count=configuration.count,
		order=order,
		window=options.window,
		size=configuration.size,
		scale=configuration.scale,
		ffmpeg=binaries.ffmpeg,
		ffprobe=binaries.ffprobe,
		root=binaries.root,
		environ=binaries.environ,
		verbosity=options.verbosity,
	)

	if type != Type.SINGLE:
		extractor.loader = Swapper()

	stream = sys.stderr
	interactive = stream.isatty()

	progress = options.progress
	if progress is None:
		progress = interactive

	if progress:
		if interactive:
			extractor.progress = ConsoleProgress(stream)
			close.insert(0, extractor.progress.close)
		else:
			extractor.progress = SimpleProgress(stream)

	debug = options.debug
	if debug is None:
		debug = False

	if debug:
		extractor.debug = print_args

	threads = options.threads
	if threads is None:
		threads = min(32, os.process_cpu_count() or 1)

	if threads > 1:
		extractor.executor = concurrent.futures.ThreadPoolExecutor(threads)
		close.append(extractor.executor.shutdown)

	if options.seed is None:
		extractor.randomizer = random.SystemRandom()
	else:
		extractor.randomizer = random.Random(options.seed)

	generator = Generator(configuration=configuration, extractor=extractor, debug=debug)

	if type == Type.SINGLE:
		filename_format = '{filename}.jpg'
	elif type == Type.RECURSIVE:
		filename_format = os.path.join('{directory}', '{filename}.jpg')
	elif type == Type.VIDEOS:
		filename_format = '{name}_{index:02d}.jpg'
	elif type == Type.IMAGES:
		filename_format = '{name}_{index:02d}.jpg'
	elif type == Type.HISTOGRAM:
		filename_format = '{filename}.jpg'
	else:
		typing.assert_never(type)

	if options.filename is not None:
		filename_format = options.filename

	concurrent.futures.ThreadPoolExecutor()
	return Context(
		generator=generator,
		type=type,
		input=options.input,
		output=options.output,
		filename_format=filename_format,
		close=close,
	)


def make_output(outputs: set[pathlib.Path], directory: pathlib.Path, filename: str) -> pathlib.Path:
	index = 0
	split: typing.Optional[tuple[str, str]] = None
	output = directory / filename

	while output in outputs:
		index += 1
		if split is None:
			split = os.path.splitext(filename)
		output = directory / '{}[{}]{}'.format(split[0], index, split[1])

	outputs.add(output)
	return output


def execute_video(context: Context) -> None:
	generator = context.generator
	extractor = generator.extractor

	steps = StepProgress.create(extractor.progress, extractor.count, 1)

	with extractor.step(steps[0]):
		vignette = generate_video(generator, context.input)

	image = compose(generator, vignette)
	image.save(context.output)

	if steps[1] is not None:
		steps[1](context.output.name, 1.0)


def execute_recursive(context: Context) -> None:
	generator = context.generator
	extractor = generator.extractor

	steps = StepProgress.create(extractor.progress, extractor.count + 1, 1)

	with extractor.step(steps[0]):
		vignettes = list(generate_video_recursive(generator, context.input))

	outputs: set[pathlib.Path] = set()
	for index, (input, vignette) in enumerate(vignettes):
		relative_input = input.relative_to(context.input)

		values: dict[str, object] = {
			'directory': os.fspath(relative_input.parent),
			'filename': input.stem,
			'name': input.name,
			'index': index,
			'ordinal': index + 1,
			'count': len(vignettes),
		}

		output = make_output(outputs, context.output, context.filename_format.format(**values))
		os.makedirs(output.parent, exist_ok=True)

		image = compose(generator, vignette)
		image.save(output)

		del image

		if steps[1] is not None:
			steps[1](output.name, make_progress(index + 1, len(vignettes)))


def execute_video_collage(context: Context) -> None:
	generator = context.generator
	extractor = generator.extractor

	steps = StepProgress.create(extractor.progress, extractor.count, 1)

	with extractor.step(steps[0]):
		vignettes = list(generate_video_collage(generator, context.input))

	outputs: set[pathlib.Path] = set()
	for index, vignette in enumerate(vignettes):
		values: dict[str, object] = {
			'directory': '',
			'filename': '',
			'name': context.input.name,
			'index': index,
			'ordinal': index + 1,
			'count': len(vignettes),
		}

		output = make_output(outputs, context.output, context.filename_format.format(**values))
		os.makedirs(output.parent, exist_ok=True)

		image = compose(generator, vignette)
		image.save(output)

		del image

		if steps[1] is not None:
			steps[1](output.name, make_progress(index + 1, len(vignettes)))


def execute_image_collage(context: Context) -> None:
	generator = context.generator
	extractor = generator.extractor

	steps = StepProgress.create(extractor.progress, extractor.count, 1)

	with extractor.step(steps[0]):
		vignettes = list(generate_image_collage(generator, context.input))

	outputs: set[pathlib.Path] = set()
	for index, vignette in enumerate(vignettes):
		values: dict[str, object] = {
			'directory': '',
			'filename': '',
			'name': context.input.name,
			'index': index,
			'ordinal': index + 1,
			'count': len(vignettes),
		}

		output = make_output(outputs, context.output, context.filename_format.format(**values))
		os.makedirs(output.parent, exist_ok=True)

		image = compose(generator, vignette)
		image.save(output)

		del image

		if steps[1] is not None:
			steps[1](output.name, make_progress(index + 1, len(vignettes)))


def execute_histogram(context: Context) -> None:
	generator = context.generator
	extractor = generator.extractor

	steps = StepProgress.create(extractor.progress, 99, 1)

	with extractor.step(steps[0]):
		vignette = generate_histogram(context.generator, context.input)

	image = compose(context.generator, vignette)
	image.save(context.output)

	del image

	if steps[1] is not None:
		steps[1](context.output.name, 1.0)


def execute(context: Context) -> None:
	if context.type == Type.SINGLE:
		execute_video(context)
	elif context.type == Type.RECURSIVE:
		execute_recursive(context)
	elif context.type == Type.VIDEOS:
		execute_video_collage(context)
	elif context.type == Type.IMAGES:
		execute_image_collage(context)
	elif context.type == Type.HISTOGRAM:
		execute_histogram(context)
	else:
		typing.assert_never(context.type)
