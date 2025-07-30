import string
from random import SystemRandom
from typing import List

import click
from click import Context, pass_context

from .core import generate

MIN_LENGTH = 8
MAX_LENGTH = 24
BOOL_CHOICES = [True, False]
EXCLUSION_VALUE = 0.3


@click.command(name='generate')
@click.option('-l', '--length', default=8, type=int, help='Length of password.')
@click.option('-u', '--upper', is_flag=True, help='Password can contain uppercase chars.')
@click.option('-n', '--nums', is_flag=True, help='Password can contain digits.')
@click.option('-s', '--special', is_flag=True, help='Password can contain special chars.')
@click.option('-e', '--exclude', default='', type=str, help='Exclude chars from password.')
@click.option('-a', '--auto', is_flag=True, help="Randomly selects option's value which are not specified.")
@pass_context
def main(ctx: Context, length: int, upper: bool, nums: bool, special: bool, exclude: str, auto: bool):
	randomizer = SystemRandom()
	ctx = click.get_current_context()
	options = ['length', 'upper', 'nums', 'special', 'exclude']
	explicit_options: List[str] = []
	for param in options:
		source = ctx.get_parameter_source(param)
		if source == click.core.ParameterSource.COMMANDLINE:
			explicit_options.append(param)

	if auto:
		msg = ['AutoOption(']
		if 'length' not in explicit_options:
			length = randomizer.randint(MIN_LENGTH, MAX_LENGTH)
			msg.append(f'length: {length}')
		if 'upper' not in explicit_options:
			upper = randomizer.choice(BOOL_CHOICES)
			msg.append(f'upper: {upper}')
		if 'nums' not in explicit_options:
			nums = randomizer.choice(BOOL_CHOICES)
			msg.append(f'nums: {nums}')
		if 'special' not in explicit_options:
			special = randomizer.choice(BOOL_CHOICES)
			msg.append(f'special: {special}')

		if 'exclude' not in explicit_options:
			charlist = [string.ascii_lowercase]
			if upper:
				charlist.append(string.ascii_uppercase)
			if nums:
				charlist.append(string.digits)
			if special:
				charlist.append(string.punctuation)

			exclude_count = randomizer.randint(0, int(len(charlist) * EXCLUSION_VALUE))
			exclude = ''.join(randomizer.sample(''.join(charlist), k=exclude_count))
			msg.append(f"exclude({exclude_count}): '{exclude}'")

		print(' '.join(msg), ')')

	try:
		password = generate(length=length, upper=upper, nums=nums, special=special, exclude=exclude)
		print(password)
	except ValueError as e:
		click.echo(f'Error: {e}', err=True)
		raise click.Abort()


if __name__ == '__main__':
	main()
