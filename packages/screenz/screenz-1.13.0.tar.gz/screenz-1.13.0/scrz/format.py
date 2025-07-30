import typing

from .extractor import Information


def format_name_size(name: str, size: typing.Optional[int]) -> str:
	if size is None:
		return name

	return '{} ({})'.format(name, format_size(size))


@typing.overload
def format_size(size: None) -> None: ...


@typing.overload
def format_size(size: int) -> str: ...


def format_size(size: typing.Optional[int]) -> typing.Optional[str]:
	if size is None:
		return None
	elif size < 1024:
		return '{} B'.format(size)
	elif size < 1048576:
		return '{} KB'.format(size // 1024)
	elif size < 1073741824:
		return '{:.1f} MB'.format(round(size / 1048576, 1))
	else:
		return '{:.2f} GB'.format(round(size / 1073741824, 2))


@typing.overload
def format_time(time: None, *, converter: typing.Callable[[float], int]) -> None: ...


@typing.overload
def format_time(time: float, *, converter: typing.Callable[[float], int]) -> str: ...


def format_time(
	time: typing.Optional[float], *, converter: typing.Callable[[float], int]
) -> typing.Optional[str]:
	if time is None:
		return None

	s = converter(time)
	h, s = divmod(s, 3600)
	m, s = divmod(s, 60)

	return ('{0:d}:{1:02d}:{2:02d}' if h else '{1:02d}:{2:02d}').format(h, m, s)


@typing.overload
def format_resolution(resolution: None) -> None: ...


@typing.overload
def format_resolution(resolution: tuple[int, int]) -> str: ...


def format_resolution(resolution: typing.Optional[tuple[int, int]]) -> typing.Optional[str]:
	if resolution is None:
		return None

	return '{}x{}'.format(*resolution)


@typing.overload
def format_frame_rate(rate: None) -> None: ...


@typing.overload
def format_frame_rate(rate: float) -> str: ...


def format_frame_rate(rate: typing.Optional[float]) -> typing.Optional[str]:
	if rate is None:
		return None

	return '{:.2f} FPS'.format(round(rate, 2))


@typing.overload
def format_bit_rate(rate: None) -> None: ...


@typing.overload
def format_bit_rate(rate: int) -> str: ...


def format_bit_rate(rate: typing.Optional[int]) -> typing.Optional[str]:
	if rate is None:
		return None

	return '{}kbps'.format(rate // 1024)


def format_information(information: Information) -> typing.Optional[str]:
	return format_fields(
		format_resolution(information.resolution),
		information.video_codec,
		information.audio_codec,
		separator='/',
	)


def format_information_ex(information: Information) -> typing.Optional[str]:
	return format_fields(
		format_fields(
			format_resolution(information.resolution),
			format_frame_rate(information.frame_rate),
			separator='@',
		),
		format_fields(
			information.video_codec, format_bit_rate(information.video_rate), separator='@'
		),
		format_fields(
			information.audio_codec, format_bit_rate(information.audio_rate), separator='@'
		),
		separator='/',
	)


def format_fields(*fields: typing.Optional[str], separator: str) -> typing.Optional[str]:
	filtered = [f for f in fields if f is not None]
	if not filtered:
		return None

	return ' {} '.format(separator).join(filtered)
