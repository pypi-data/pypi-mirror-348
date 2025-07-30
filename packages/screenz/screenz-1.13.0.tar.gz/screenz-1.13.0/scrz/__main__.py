import argparse
import enum
import functools
import importlib.metadata
import os
import pathlib
import sys
import types
import typing

import PIL.Image
import PIL.ImageColor

from .configuration import Header
from .driver import Type, create_context
from .driver import execute as execute_context
from .extractor import Order, Scale, Verbosity
from .layout import Layout
from .scanner import Extensions
from .types import Color

TEnum = typing.TypeVar('TEnum', bound=enum.Enum)


def parse_path(input: str) -> pathlib.Path:
	try:
		return pathlib.Path(os.path.normpath(os.path.abspath(input)))
	except Exception as e:
		raise argparse.ArgumentTypeError('invalid path value') from e


def enum_choices(type: typing.Type[TEnum]) -> tuple[str, ...]:
	return tuple(map(str.lower, type.__members__.keys()))


def enum_parser(type: typing.Type[TEnum]) -> typing.Callable[[str], TEnum]:
	return functools.partial(parse_enum, type)


def parse_enum(type: typing.Type[TEnum], input: str) -> TEnum:
	try:
		return type.__members__[input.upper()]
	except KeyError as e:
		raise argparse.ArgumentTypeError('invalid {} value'.format(type.__name__.lower())) from e


def parse_extensions(input: str) -> Extensions:
	if not input:
		return Extensions()

	return Extensions(
		*(
			extension if extension.startswith('.') else '.{}'.format(extension)
			for extension in input.split(';')
			if extension
		)
	)


def parse_ignore(input: str) -> tuple[str, ...]:
	if not input:
		return ()

	return tuple(input.split(';'))


def parse_background(input: str) -> typing.Union[Color, pathlib.Path]:
	if input.startswith('image:'):
		return parse_path(input[6:])
	else:
		return parse_color(input)


def parse_color(input: str) -> Color:
	try:
		return PIL.ImageColor.getrgb(input)
	except ValueError as e:
		raise argparse.ArgumentTypeError('invalid color value') from e


def parse_slice(input: str) -> typing.Optional[slice]:
	try:
		return slice(*(int(part) if part else None for part in input.split(':')))
	except (TypeError, ValueError) as e:
		raise argparse.ArgumentTypeError('invalid slice value') from e


class CustomParser(argparse.ArgumentParser):
	def _check_value(self, action: argparse.Action, value: object) -> None:
		pass


def create_parser() -> argparse.ArgumentParser:
	parser = CustomParser(description='Generates screenshots from videos and images')
	parser.add_argument('input', type=parse_path)
	parser.add_argument('output', type=parse_path)

	parser.add_argument(
		'-V', '--version', action='version', version=importlib.metadata.version('screenz')
	)

	parser.add_argument(
		'-t', '--type', type=enum_parser(Type), choices=enum_choices(Type), help='generation type'
	)

	parser.add_argument(
		'-e',
		'--extensions',
		type=parse_extensions,
		help='semicolon-separated list of file extensions to consider when recursing',
	)

	parser.add_argument(
		'-L',
		'--follow',
		action=argparse.BooleanOptionalAction,
		help='follow symbolic links when recursing',
	)

	parser.add_argument(
		'-i',
		'--ignore',
		type=parse_ignore,
		help='semicolon-separated list of patterns to ignore when recursing',
	)

	parser.add_argument(
		'-v',
		'--verbosity',
		type=enum_parser(Verbosity),
		choices=enum_choices(Verbosity),
		help='ffmpeg output verbosity',
	)

	parser.add_argument(
		'-b',
		'--background',
		type=parse_background,
		help='color or image of the background (use image:PATH to specify image)',
	)

	parser.add_argument(
		'-f', '--foreground', type=parse_color, help='color of the foreground and borders'
	)

	parser.add_argument(
		'-a', '--accent', type=parse_color, help='color of the timestamps and histogram bars'
	)

	parser.add_argument('-F', '--font', type=str, help='font name')
	parser.add_argument('-z', '--font-size', type=int, help='font height')

	parser.add_argument(
		'-H',
		'--header',
		type=enum_parser(Header),
		choices=enum_choices(Header),
		help='level of information in the header',
	)

	parser.add_argument('-s', '--size', type=int, help='size of the cells')

	parser.add_argument(
		'-S',
		'--scale',
		type=enum_parser(Scale),
		choices=enum_choices(Scale),
		help='how to compute the size of the cells',
	)

	parser.add_argument(
		'-l',
		'--layout',
		type=enum_parser(Layout),
		choices=enum_choices(Layout),
		help='cell layout mode',
	)

	parser.add_argument('-C', '--columns', type=int, help='number of columns')
	parser.add_argument('-c', '--count', type=int, help='number of cells')
	parser.add_argument('-p', '--padding', type=int, help='padding between cells')

	parser.add_argument(
		'-o',
		'--order',
		type=enum_parser(Order),
		choices=enum_choices(Order),
		help='order of files when recursing',
	)

	parser.add_argument('-Z', '--seed', type=int, help='seed for random order')
	parser.add_argument('-w', '--window', type=parse_slice, help='create a window over the results')
	parser.add_argument('-n', '--filename', type=str, help='default image filename format')

	parser.add_argument('-T', '--threads', type=int, help='number of threads')

	parser.add_argument(
		'-P', '--progress', action=argparse.BooleanOptionalAction, help='show progress'
	)

	parser.add_argument(
		'-d',
		'--debug',
		action=argparse.BooleanOptionalAction,
		help='show command lines and layout item bounds',
	)

	return parser


def exception_handler(
	exc_type: typing.Type[BaseException],
	exc_value: BaseException,
	exc_traceback: typing.Optional[types.TracebackType],
) -> None:
	if not issubclass(exc_type, Exception):
		return

	sys.stderr.write('{}: {}\n'.format(exc_type.__name__, exc_value))


def execute() -> None:
	parser = create_parser()
	options = parser.parse_args()

	with create_context(options) as context:
		execute_context(context)


def main() -> None:
	if 'debugpy' in sys.modules:
		execute()

	elif getattr(sys, 'frozen', False):
		try:
			execute()
		except:
			exception_handler(*sys.exc_info())
			sys.exit(1)

	else:
		sys.excepthook = exception_handler
		execute()


if __name__ == '__main__':
	main()
