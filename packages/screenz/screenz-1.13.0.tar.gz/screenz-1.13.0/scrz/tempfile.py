import os
import sys
import tempfile
import typing

if sys.platform == 'win32':
	import ctypes
	import ctypes.wintypes
	import msvcrt

	_create_file = ctypes.WinDLL('KERNEL32', use_last_error=True).CreateFileW
	_create_file.restype = ctypes.wintypes.HANDLE
	_create_file.argtypes = (
		ctypes.wintypes.LPCWSTR,
		ctypes.wintypes.DWORD,
		ctypes.wintypes.DWORD,
		ctypes.wintypes.LPVOID,
		ctypes.wintypes.DWORD,
		ctypes.wintypes.DWORD,
		ctypes.wintypes.HANDLE,
	)

	def create(
		suffix: str = '',
		prefix: str = '',
		directory: typing.Union[os.PathLike[str], str, None] = None,
	) -> int:
		while True:
			path = tempfile.mktemp(suffix, prefix, directory)
			handle: int = _create_file(
				path,
				0xC0000000,  # GENERIC_READ | GENERIC_WRITE
				1,  # FILE_SHARE_READ
				None,
				1,  # CREATE_NEW
				0x04000100,  # FILE_FLAG_DELETE_ON_CLOSE | FILE_ATTRIBUTE_TEMPORARY,
				None,
			)

			if handle != -1:
				break

			error = ctypes.get_last_error()
			if error == 80:  # ERROR_FILE_EXISTS
				continue

			raise ctypes.WinError(error)

		return msvcrt.open_osfhandle(handle, os.O_RDWR | os.O_NOINHERIT)

else:

	def create(
		suffix: str = '',
		prefix: str = '',
		directory: typing.Union[os.PathLike[str], str, None] = None,
	) -> int:
		fd, path = tempfile.mkstemp(suffix, prefix, directory)

		try:
			os.unlink(path)
		except:
			os.close(fd)
			raise

		return fd
