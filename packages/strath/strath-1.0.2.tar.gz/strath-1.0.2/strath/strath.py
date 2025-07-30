# __all__ declared at the module's end

from pathlib import Path


_ERROR_MSG: str =\
	"The path must be of type str or pathlib.Path. None is not allowed."
_ERROR_MSG_NONE: str =\
	"The path must be None or of type str or pathlib.Path."


def _raise_type_error(is_none_allowed: bool) -> None:
	message = _ERROR_MSG_NONE if is_none_allowed else _ERROR_MSG
	raise TypeError(message)


def ensure_path_is_pathlib(
		some_path: Path | str | None,
		is_none_allowed: bool
	) -> Path:
	"""
	If argument some_path is a string, this function converts it to a
	pathlib.Path instance, which it returns. If some_path is a pathlib.Path
	instance, this function returns some_path.

	If argument some_path is None and argument is_none_allowed is True, this
	function returns None. However, if is_none_allowed is False, a TypeError is
	raised.

	If argument some_path is not None nor an instance of str or pathlib.Path,
	a TypeError is raised.

	Parameters:
		some_path: the path to a file or directory.
		is_none_allowed: determines whether some_path can be None.

	Returns:
		pathlib.Path: the path to a file or directory, possibly None.

	Raises:
		TypeError: if some_path is of a wrong type.
	"""
	if isinstance(some_path, str):
		some_path = Path(some_path)

	elif some_path is None:
		if not is_none_allowed:
			_raise_type_error(is_none_allowed)

	elif not isinstance(some_path, Path):
		_raise_type_error(is_none_allowed)

	return some_path


def ensure_path_is_str(
		some_path: Path | str | None,
		is_none_allowed: bool
	) -> str:
	"""
	If argument some_path is a pathlib.Path instance, this function converts
	it to a string, which it returns. If some_path is a string, this function
	returns some_path.

	If argument some_path is None and argument is_none_allowed is True, this
	function returns None. However, if is_none_allowed is False, a TypeError is
	raised.

	If argument some_path is not None nor an instance of str or pathlib.Path,
	a TypeError is raised.

	Parameters:
		some_path: the path to a file or directory.
		is_none_allowed: determines whether some_path can be None.

	Returns:
		str: the path to a file or directory, possibly None.

	Raises:
		TypeError: if some_path is of a wrong type.
	"""
	if isinstance(some_path, Path):
		some_path = str(some_path)

	elif some_path is None:
		if not is_none_allowed:
			_raise_type_error(is_none_allowed)

	elif not isinstance(some_path, str):
		_raise_type_error(is_none_allowed)

	return some_path


__all__ = [
	ensure_path_is_pathlib.__name__,
	ensure_path_is_str.__name__
]
