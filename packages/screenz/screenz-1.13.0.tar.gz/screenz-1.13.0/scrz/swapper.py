import io
import mmap
import os
import sys
import threading
import typing

import PIL.Image

from .tempfile import create as create_file

# because keeping tens of thousands of loaded PIL images at once uses too much memory in VMs and
# on seedboxes, do some magic(tm) to have them backed by file mappings...

PREFIX = 'scrz-'
SUFFIX = '.bin'
CHUNK_SIZE = 256 * 1024**2  # 256MB


class Swapper:
	__slots__ = ('lock', 'directory', 'mapping', 'view')

	def __init__(self, directory: typing.Union[os.PathLike[str], str, None] = None) -> None:
		self.lock = threading.Lock()
		self.directory = directory
		self.mapping: typing.Optional[mmap.mmap] = None
		self.view: typing.Optional[memoryview] = None

	def __call__(self, data: bytes, format: str) -> PIL.Image.Image:
		return swapped_loader(self, data, format)


def simple_loader(data: bytes, format: str) -> PIL.Image.Image:
	with io.BytesIO(data) as fp:
		image = PIL.Image.open(fp, formats=(format,))
		image.load()

	return image


def swapped_loader(swapper: Swapper, data: bytes, format: str) -> PIL.Image.Image:
	image = simple_loader(data, format)

	if image.mode == 'RGB':
		image = image.convert('RGBX')
	elif image.mode not in PIL.Image._MAPMODES:
		image = image.convert('RGBA')

	mode = image.mode
	size = image.size
	data = image.tobytes()
	del image

	view = allocate_view(swapper, data)
	del data

	return PIL.Image.frombuffer(mode, size, view)


def allocate_view(swapper: Swapper, data: bytes) -> memoryview:
	if not data or len(data) > CHUNK_SIZE:
		return memoryview(data)

	with swapper.lock:
		while True:
			if swapper.mapping is None:
				swapper.mapping = create_mapping(CHUNK_SIZE, swapper.directory)

			if swapper.view is None:
				swapper.view = memoryview(swapper.mapping)

			position = swapper.mapping.tell()
			size = len(swapper.view)

			if size - position >= len(data):
				break

			swapper.view = None
			swapper.mapping = None

		length = swapper.mapping.write(data)
		assert length == len(data)

		return swapper.view[position : position + length]


def create_mapping(
	size: int, directory: typing.Union[os.PathLike[str], str, None] = None
) -> mmap.mmap:
	fd = create_file(SUFFIX, PREFIX, directory)
	try:
		os.truncate(fd, size)
		if sys.platform == 'win32':
			return mmap.mmap(fd, 0)
		else:
			return mmap.mmap(fd, 0, trackfd=False)
	finally:
		os.close(fd)
