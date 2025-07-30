from secrets import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from typing import List


def generate(length: int, upper: bool, nums: bool, special: bool, exclude: str) -> str:
	"""Generates a secure random password based on parameters."""

	if length < 0:
		raise ValueError('Length must be non-negative')

	charRandomizer = SystemRandom()
	multiplier = 1
	charlist = [*ascii_lowercase]
	if upper:
		multiplier += 1
		charlist.extend(list(ascii_uppercase))
	if nums:
		multiplier += 1
		charlist.extend(list(digits))
	if special:
		multiplier += 1
		charlist.extend(list(punctuation))
	if exclude:
		exclude = ''.join(set([*exclude]))
		if len(exclude) >= len(charlist):
			raise ValueError('Excluded chars surpasses valid charlist')
		cleaned: List[str] = []
		for c in charlist:
			if c not in exclude:
				cleaned.append(c)
		charlist = cleaned

	rand_chars = [charRandomizer.choice(charlist) for _ in range(length * multiplier)]

	return ''.join(charRandomizer.sample(rand_chars, k=length))


if __name__ == '__main__':
	print(generate(12, True, True, True, '\'"`/\\\\'))
