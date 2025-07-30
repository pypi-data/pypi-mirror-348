import collections.abc
import dataclasses
import math
import os
import pathlib
import typing

import PIL.Image

from .configuration import Configuration, Header
from .extractor import (
	VIDEOS,
	Extractor,
	Frame,
	Information,
	extract_directory_frames,
	extract_directory_images,
	extract_directory_infos,
	extract_directory_videos,
	extract_frames,
	extract_information,
)
from .format import (
	format_information,
	format_information_ex,
	format_name_size,
	format_size,
	format_time,
)
from .histogram import (
	Distribution,
	extract_bands,
	extract_distribution,
	render_histogram,
	trim_distribution,
)
from .layout import layout, split
from .renderer import render
from .scanner import StrPath
from .types import Color
from .vignette import Alignment, Cell, Label, Vignette


@dataclasses.dataclass(eq=False, kw_only=True)
class Generator:
	configuration: Configuration
	extractor: Extractor
	debug: bool = False
	width: typing.Optional[int] = None


def make_video_header(configuration: Configuration, information: Information) -> list[Label]:
	result: list[Label] = []

	if configuration.header == Header.BASIC:
		result.append(
			make_header_label(
				configuration,
				format_name_size(information.name, information.size),
				alignment=Alignment.NEAR,
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	elif configuration.header == Header.ADVANCED:
		result.append(make_header_label(configuration, information.name, alignment=Alignment.NEAR))
		result.append(
			make_header_label(configuration, format_size(information.size), alignment=Alignment.FAR)
		)
		result.append(
			make_header_label(
				configuration, format_information(information), alignment=Alignment.NEAR
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	elif configuration.header == Header.TECHNICAL:
		result.append(make_header_label(configuration, information.name, alignment=Alignment.NEAR))
		result.append(
			make_header_label(configuration, format_size(information.size), alignment=Alignment.FAR)
		)
		result.append(
			make_header_label(
				configuration, format_information_ex(information), alignment=Alignment.NEAR
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	return result


def make_histogram_footer(configuration: Configuration, distribution: Distribution) -> list[Label]:
	return [
		make_footer_label(
			configuration,
			format_time(distribution.minimum, converter=math.floor),
			alignment=Alignment.NEAR,
		),
		make_footer_label(
			configuration,
			format_time(distribution.maximum, converter=math.ceil),
			alignment=Alignment.FAR,
		),
	]


def make_collage_header(
	configuration: Configuration, path: StrPath, page_index: int, page_count: int
) -> list[Label]:
	if configuration.header == Header.NONE:
		return []

	return [
		make_header_label(configuration, os.path.basename(path), alignment=Alignment.NEAR),
		make_header_label(
			configuration, '{}/{}'.format(page_index + 1, page_count), alignment=Alignment.FAR
		),
	]


def make_header_label(
	configuration: Configuration, text: typing.Optional[str], *, alignment: Alignment
) -> Label:
	return Label(
		text=text,
		font=configuration.font0,
		halignment=alignment,
		valignment=Alignment.MIDDLE,
		color=configuration.foreground,
		border='black' if isinstance(configuration.background, PIL.Image.Image) else None,
	)


def make_footer_label(
	configuration: Configuration, text: typing.Optional[str], *, alignment: Alignment
) -> Label:
	return Label(
		text=text,
		font=configuration.font2,
		halignment=alignment,
		valignment=Alignment.MIDDLE,
		color=configuration.foreground,
		border='black' if isinstance(configuration.background, PIL.Image.Image) else None,
	)


def make_frame_cell(configuration: Configuration, timestamp: float, image: Frame) -> Cell:
	return Cell(
		image=image,
		label=Label(
			text=format_time(timestamp, converter=math.floor),
			font=configuration.font1,
			halignment=Alignment.FAR,
			valignment=Alignment.FAR,
			color=configuration.accent,
			border='black',
		),
	)


def make_video_cell(
	configuration: Configuration, duration: typing.Optional[float], image: Frame
) -> Cell:
	if duration is None:
		return Cell(image=image)

	return Cell(
		image=image,
		label=Label(
			text=format_time(duration, converter=round),
			font=configuration.font1,
			halignment=Alignment.FAR,
			valignment=Alignment.FAR,
			color=configuration.accent,
			border='black',
		),
	)


def make_histogram_cell(configuration: Configuration, distribution: Distribution) -> Cell:
	bands = extract_bands(distribution, configuration.count)

	if configuration.columns is None:
		width = configuration.count * (8 + configuration.padding[1]) + 1
	else:
		width = configuration.columns * configuration.size

	background: Color
	if isinstance(configuration.background, PIL.Image.Image):
		background = 'black'
	else:
		background = configuration.background

	return Cell(
		image=render_histogram(
			bands,
			width=width,
			height=configuration.size,
			background=background,
			axis=configuration.foreground,
			bar_color=configuration.accent,
			spacing=configuration.padding[1],
		)
	)


def generate_video(generator: Generator, path: StrPath) -> Vignette:
	information = extract_information(generator.extractor, path)
	frames = extract_frames(generator.extractor, path, duration=information.duration)

	headers = make_video_header(generator.configuration, information)
	cells = [
		make_frame_cell(generator.configuration, timestamp, image) for timestamp, image in frames
	]

	return Vignette(
		background=generator.configuration.background,
		border=generator.configuration.foreground,
		headers=headers,
		cells=cells,
	)


def generate_video_recursive(
	generator: Generator, path: StrPath
) -> collections.abc.Iterator[tuple[pathlib.Path, Vignette]]:
	result = extract_directory_frames(generator.extractor, path)

	for vpath, information, frames in result:
		headers = make_video_header(generator.configuration, information)
		cells = [
			make_frame_cell(generator.configuration, timestamp, image)
			for timestamp, image in frames
		]

		yield (
			vpath,
			Vignette(
				background=generator.configuration.background,
				border=generator.configuration.foreground,
				headers=headers,
				cells=cells,
			),
		)


def generate_video_collage(
	generator: Generator, path: StrPath
) -> collections.abc.Iterator[Vignette]:
	frames = [f for f in extract_directory_videos(generator.extractor, path) if f[2] is not None]

	chunks, generator.width = split(
		frames,
		lambda f: None if f[2] is None else f[2].width,
		chunk_size=generator.configuration.count,
		mode=generator.configuration.layout,
		columns=generator.configuration.columns,
		spacing=generator.configuration.padding,
	)

	for index, chunk in enumerate(chunks):
		headers = make_collage_header(generator.configuration, path, index, len(chunks))
		cells = [
			make_video_cell(generator.configuration, info.duration, image)
			for _, info, image in chunk
		]

		yield Vignette(
			background=generator.configuration.background,
			border=generator.configuration.foreground,
			headers=headers,
			cells=cells,
		)


def generate_image_collage(
	generator: Generator, path: StrPath
) -> collections.abc.Iterator[Vignette]:
	frames = [f for f in extract_directory_images(generator.extractor, path) if f[1] is not None]

	chunks, generator.width = split(
		frames,
		lambda f: None if f[1] is None else f[1].width,
		chunk_size=generator.configuration.count,
		mode=generator.configuration.layout,
		columns=generator.configuration.columns,
		spacing=generator.configuration.padding,
	)

	for index, chunk in enumerate(chunks):
		headers = make_collage_header(generator.configuration, path, index, len(chunks))
		cells = [Cell(image=image) for _, image in chunk]

		yield Vignette(
			background=generator.configuration.background,
			border=generator.configuration.foreground,
			headers=headers,
			cells=cells,
		)


def generate_histogram(generator: Generator, path: StrPath) -> Vignette:
	with generator.extractor.scanner.specialize(VIDEOS):
		informations = [f[1] for f in extract_directory_infos(generator.extractor, path)]

	distribution_raw = extract_distribution(informations)
	distribution = trim_distribution(distribution_raw)

	footers = make_histogram_footer(generator.configuration, distribution)
	cells = [make_histogram_cell(generator.configuration, distribution)]

	return Vignette(
		background=generator.configuration.background, border=None, cells=cells, footers=footers
	)


def compose(generator: Generator, vignette: Vignette) -> PIL.Image.Image:
	items = layout(
		vignette,
		mode=generator.configuration.layout,
		columns=generator.configuration.columns,
		width=generator.width,
		spacing=generator.configuration.padding,
	)

	return render(background=generator.configuration.background, items=items, debug=generator.debug)
