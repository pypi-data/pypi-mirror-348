import dataclasses
import enum
import pathlib
import typing

import PIL.Image

from .extractor import Scale
from .font import load as load_font
from .layout import Layout
from .types import Color, Font


class Header(enum.IntEnum):
	NONE = 0
	BASIC = 1
	ADVANCED = 2
	TECHNICAL = 3


class Options(typing.Protocol):
	@property
	def background(self) -> typing.Union[Color, pathlib.Path, None]: ...
	@property
	def foreground(self) -> typing.Optional[Color]: ...
	@property
	def accent(self) -> typing.Optional[Color]: ...
	@property
	def font(self) -> typing.Optional[str]: ...
	@property
	def font_size(self) -> typing.Optional[int]: ...
	@property
	def header(self) -> typing.Optional[Header]: ...
	@property
	def size(self) -> typing.Optional[int]: ...
	@property
	def scale(self) -> typing.Optional[Scale]: ...
	@property
	def layout(self) -> typing.Optional[Layout]: ...
	@property
	def columns(self) -> typing.Optional[int]: ...
	@property
	def count(self) -> typing.Optional[int]: ...
	@property
	def padding(self) -> typing.Optional[int]: ...


@dataclasses.dataclass(eq=False, kw_only=True)
class Configuration:
	background: typing.Union[Color, PIL.Image.Image]
	foreground: Color
	accent: Color
	font0: Font
	header: Header
	size: int
	scale: Scale
	font1: Font
	layout: Layout
	columns: typing.Optional[int]
	count: int
	font2: Font
	padding: tuple[int, int]


def configure_video() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.ADVANCED,
		size=300,
		scale=Scale.WIDTH,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=None,
		count=16,
		font2=load_font('8x16n'),
		padding=(8, 8),
	)


def configure_video_collage() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.NONE,
		size=192,
		scale=Scale.CROP,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=5,
		count=30,
		font2=load_font('8x16n'),
		padding=(0, 0),
	)


def configure_image_collage() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.NONE,
		size=192,
		scale=Scale.HEIGHT,
		font1=load_font('8x14n'),
		layout=Layout.VARIABLE,
		columns=8,
		count=64,
		font2=load_font('8x16n'),
		padding=(0, 0),
	)


def configure_histogram() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='#00ff00',
		font0=load_font('8x16n'),
		header=Header.NONE,
		size=96,
		scale=Scale.HEIGHT,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=None,
		count=94,
		font2=load_font('8x16b'),
		padding=(8, 2),
	)


def update(configuration: Configuration, options: Options) -> Configuration:
	if options.background is not None:
		if isinstance(options.background, pathlib.Path):
			configuration.background = PIL.Image.open(options.background)
			configuration.background.load()
		else:
			configuration.background = options.background

	if options.foreground is not None:
		configuration.foreground = options.foreground

	if options.accent is not None:
		configuration.accent = options.accent

	if options.font is not None:
		configuration.font2 = configuration.font1 = configuration.font0 = (
			load_font(options.font)
			if options.font_size is None
			else load_font(options.font, options.font_size)
		)

	if options.header is not None:
		configuration.header = options.header

	if options.size is not None:
		configuration.size = options.size

	if options.scale is not None:
		configuration.scale = options.scale

	if options.layout is not None:
		configuration.layout = options.layout

	if options.columns is not None:
		configuration.columns = options.columns

	if options.count is not None:
		configuration.count = options.count

	if options.padding is not None:
		configuration.padding = (options.padding, options.padding)

	return configuration
