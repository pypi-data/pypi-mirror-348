import pytest

import os
from pathlib import Path
import sys

repo_root = str(Path(__file__).resolve().parents[1])
sys.path.insert(0, repo_root)
from strath import\
	ensure_path_is_pathlib,\
	ensure_path_is_str
sys.path.remove(repo_root)
del repo_root


_ERROR_MSG =\
	"The path must be of type str or pathlib.Path. None is not allowed."
_ERROR_MSG_NONE =\
	"The path must be None or of type str or pathlib.Path."


def test_pathlib_to_pathlib():
	some_path = Path(__file__).resolve()
	converted_path = ensure_path_is_pathlib(some_path, False)

	assert isinstance(converted_path, Path)
	assert converted_path == some_path
	assert converted_path is some_path


def test_pathlib_to_str():
	some_path = Path(__file__).resolve()
	converted_path = ensure_path_is_str(some_path, False)

	assert isinstance(converted_path, str)
	assert Path(converted_path) == some_path
	assert converted_path is not some_path


def test_str_to_pathlib():
	some_path = os.path.abspath(__file__)
	converted_path = ensure_path_is_pathlib(some_path, False)

	assert isinstance(converted_path, Path)
	assert str(converted_path) == some_path
	assert converted_path is not some_path


def test_str_to_str():
	some_path = os.path.abspath(__file__)
	converted_path = ensure_path_is_str(some_path, False)

	assert isinstance(converted_path, str)
	assert converted_path == some_path
	assert converted_path is some_path


def test_none_allowed_pathlib():
	none_path = ensure_path_is_pathlib(None, True)
	assert none_path is None


def test_none_disallowed_pathlib():
	with pytest.raises(TypeError, match=_ERROR_MSG):
		ensure_path_is_pathlib(None, False)


def test_none_allowed_str():
	none_path = ensure_path_is_str(None, True)
	assert none_path is None


def test_none_disallowed_str():
	with pytest.raises(TypeError, match=_ERROR_MSG):
		ensure_path_is_str(None, False)


def test_incorrect_type_none_allowed_pathlib():
	with pytest.raises(TypeError, match=_ERROR_MSG_NONE):
		ensure_path_is_pathlib(3.14159, True)


def test_incorrect_type_none_disallowed_pathlib():
	with pytest.raises(TypeError, match=_ERROR_MSG):
		ensure_path_is_pathlib(3.14159, False)


def test_incorrect_type_none_allowed_str():
	with pytest.raises(TypeError, match=_ERROR_MSG_NONE):
		ensure_path_is_str(3.14159, True)


def test_incorrect_type_none_disallowed_str():
	with pytest.raises(TypeError, match=_ERROR_MSG):
		ensure_path_is_str(3.14159, False)
