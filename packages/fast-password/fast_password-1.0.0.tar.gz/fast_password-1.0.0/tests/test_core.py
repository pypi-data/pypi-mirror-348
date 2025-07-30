from string import ascii_lowercase, punctuation

import pytest

from fast_password.core import generate


def test_generate_length():
	"""Test that the generated string has the correct length."""
	result = generate(length=10, upper=False, nums=False, special=False, exclude='')
	assert len(result) == 10
	result = generate(length=0, upper=False, nums=False, special=False, exclude='')
	assert len(result) == 0


def test_only_lowercase():
	"""Test that only lowercase letters are included when upper, nums, and special are False."""
	result = generate(length=100, upper=False, nums=False, special=False, exclude='')
	assert all(c.islower() for c in result), 'String contains non-lowercase characters'
	assert all(c in ascii_lowercase for c in result), 'String contains invalid characters'


def test_uppercase_included():
	"""Test that uppercase letters are included when upper=True."""
	result = generate(length=1000, upper=True, nums=False, special=False, exclude='')
	assert any(c.isupper() for c in result), 'No uppercase letters found'
	assert all(c.isalpha() for c in result), 'String contains non-alphabetic characters'


def test_numbers_included():
	"""Test that numbers are included when nums=True."""
	result = generate(length=1000, upper=False, nums=True, special=False, exclude='')
	assert any(c.isdigit() for c in result), 'No digits found'
	assert all(c.islower() or c.isdigit() for c in result), 'String contains invalid characters'


def test_special_characters_included():
	"""Test that special characters are included when special=True."""
	special_chars = punctuation
	result = generate(length=1000, upper=False, nums=False, special=True, exclude='')
	assert any(c in special_chars for c in result), 'No special characters found'
	assert all(c.islower() or c in special_chars for c in result), 'String contains invalid characters'


def test_exclude_characters():
	"""Test that excluded characters are not included in the generated string."""
	result = generate(length=1000, upper=False, nums=False, special=False, exclude=ascii_lowercase[:4])
	assert all(c not in 'abc' for c in result), 'Excluded characters found in string'
	assert all(c in ascii_lowercase[4:] for c in result), 'String contains invalid characters'


def test_all_character_types():
	"""Test that all specified character types are included when all flags are True."""
	result = generate(length=1000, upper=True, nums=True, special=True, exclude='')
	assert any(c.islower() for c in result), 'No lowercase letters found'
	assert any(c.isupper() for c in result), 'No uppercase letters found'
	assert any(c.isdigit() for c in result), 'No digits found'
	assert any(not c.isalnum() for c in result), 'No special characters found'


def test_exclude_all_lowercase():
	"""Test behavior when all lowercase letters are excluded."""
	result = generate(length=100, upper=True, nums=True, special=True, exclude=ascii_lowercase)
	assert all(not c.islower() for c in result), 'Lowercase letters found despite exclusion'
	assert all(c.isupper() or c.isdigit() or not c.isalnum() for c in result), 'Invalid characters found'


def test_invalid_length():
	"""Test that an invalid (negative) length raises an appropriate error."""
	with pytest.raises(ValueError, match='Length must be non-negative'):
		generate(length=-1, upper=False, nums=False, special=False, exclude='')


def test_no_valid_characters():
	"""Test when all possible characters are excluded or no character types are allowed."""
	with pytest.raises(ValueError, match='Excluded chars surpasses valid charlist'):
		generate(length=10, upper=False, nums=False, special=False, exclude=ascii_lowercase)


def test_randomness():
	"""Test that two calls with the same parameters produce different strings."""
	result1 = generate(length=50, upper=True, nums=True, special=True, exclude='')
	result2 = generate(length=50, upper=True, nums=True, special=True, exclude='')
	assert result1 != result2, 'Generated strings are identical, randomness issue'
