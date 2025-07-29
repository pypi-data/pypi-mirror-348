"""
	A version of timetools built on Pendulum. Pendulum has a number of great features, but suffers from the
	same drawbacks as other Date/time modules when creating an object from another object or uncommon format.
	Pendulum also does not offer convienience methods for some datetime representations (ex. ISO durations).
	Ex. pandas.Timestamp is not compatible with pendulum.datetime.
"""

import datetime
import re
from typing import *

import pendulum
from loguru import logger

STuple = Tuple[int, ...]
TTuple = Tuple[int, int, int]

MONTHS_SHORT = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
MONTHS_LONG = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]


def _attempt_to_get_attribute(obj: Any, key: str, default = 0):
	try:
		attribute = getattr(obj, key)
	except AttributeError:
		attribute = default
	return attribute


def _parse_datetime_dict(data: Dict[str, int | float | str]) -> Dict[str, int]:
	year = int(data['year'])
	month = data['month']
	day = int(data['day'])

	hour = 0 if data['hour'] is None else int(data['hour'])
	minute = 0 if data['minute'] is None else int(data['minute'])
	second = 0 if data['second'] is None else float(data['second'])
	second = int(second)

	year = _parse_year(year)
	month = _convert_month_to_integer(month)

	data = {
		'day':    day,
		'month':  month,
		'year':   year,
		'hour':   hour,
		'minute': minute,
		'second': second
	}
	return data


def _convert_month_to_integer(month: int | str) -> int:
	""" Attempts to convert the input string into an integer representing the month """
	# Check if the month value eneeds to be converted in the first place.

	if isinstance(month, str):
		if month.isdigit():
			month = int(month)
		else:
			month = month.lower()
			if len(month) == 3:
				month = MONTHS_SHORT.index(month) + 1
			else:
				month = MONTHS_LONG.index(month) + 1
	return month


def _parse_year(year: int | str, cutoff: int = 50) -> int:
	""" Checks if the year was formatted as a two-digit number or a four-digit number. If it is a two-digit number, try to guess the actual year. """
	year = int(year)
	if year < 1900:
		if year > cutoff:  # "Close to the midpoint of the century."
			year += 1900
		else:
			year += 2000
	return year


class Timestamp(pendulum.DateTime):
	def __new__(cls, *args, **kwargs):
		if len(args) == 1:
			value = args[0]
		elif len(args) > 1:
			return cls.from_values(*args)
		else:
			value = None
		if value is not None:
			return cls.parse(value)
		result = super().__new__(cls, **kwargs)
		return result

	def __repr__(self) -> str:
		""" This changes what repr() returns for Timestamp objects so they are shown with ISO timestamps.
		ex. "Timestamp(2013, 10, 23, 0, 0, 0)" -> "Timestamp('2013-10-23T00:00:00')"
		"""
		iso_string = self.to_iso()
		result = f"Timestamp('{iso_string}')"
		return result

	def __eq__(self, other):
		return self.year == other.year and self.month == other.month and self.day == other.day and self.hour == other.hour and self.minute == other.minute and self.second == other.second

	def __float__(self) -> float:
		""" Converts the timestamp to a floating point representation.
			Ex. float(Timestamp('2018-06-31')) -> 2018.5
		"""
		return self.year + (self.day_of_year / 365)

	@classmethod
	def parse(cls, value: Any) -> 'Timestamp':
		if isinstance(value, str):
			result = cls.from_string(value)
		elif isinstance(value, (list, tuple)):
			result = cls.from_tuple(value)
		elif isinstance(value, dict):
			result = cls.from_keys(value)
		else:
			result = cls.from_object(value)
		return result

	@classmethod
	def from_dict(cls, **kwargs) -> 'Timestamp':
		result = cls(**kwargs)
		return result

	@classmethod
	def from_keys(cls, keys: Dict[str, int]) -> 'Timestamp':
		return cls.from_dict(**keys)

	@classmethod
	def from_tuple(cls, value: Union[STuple, TTuple]) -> 'Timestamp':
		if len(value) == 3:
			year, month, day = value
			hour, minute, second = 0, 0, 0
			other = []
		else:
			year, month, day, hour, minute, second, *other = value

		data = {
			'year':   year,
			'month':  month,
			'day':    day,
			'hour':   hour,
			'minute': minute,
			'second': second
		}
		if len(other) > 0:
			data['microsecond'] = other[0]
		else:
			data['microsecond'] = 0
		return cls.from_dict(**data)

	@classmethod
	def from_object(cls, obj: Any) -> 'Timestamp':
		"""
			Attempts to create a pendulum.DateTime object from another datetime object from a
			different module.
		Parameters
		----------
		obj: Any
			Should have .year, .month, and .day methods, but may also have .hour, .minute, .hour, .tz attributes.

		Returns
		-------
		Timestamp
		"""
		year = obj.year
		month = obj.month
		day = obj.day

		hour = _attempt_to_get_attribute(obj, 'hour', 0)
		minute = _attempt_to_get_attribute(obj, 'minute', 0)
		second = _attempt_to_get_attribute(obj, 'second', 0)
		microsecond = _attempt_to_get_attribute(obj, 'microsecond', 0)

		result = cls.from_values(year, month, day, hour, minute, second, microsecond)

		return result

	@classmethod
	def from_american_date(cls, value: str) -> pendulum.DateTime:
		"""
			Parses a date formatted as DD/MM/YY(YY), as is common in the US.

		Parameters
		----------
		value:str

		Returns
		-------
		pendulum.DateTime
		"""
		if ' ' in value:
			dates, times = value.split(' ')
		elif 'T' in value:
			dates, times = value.split('T')
		else:
			dates = value
			times = ""

		month, day, year = list(map(int, dates.split('/')))
		# Need to fix the year value if it's only two digits
		year = _parse_year(year)
		if times:
			hour, minute, second, *_ = list(map(int, times.split(':')))
		else:
			hour, minute, second = 0, 0, 0

		keys = {
			'year':   year,
			'month':  month,
			'day':    day,
			'hour':   hour,
			'minute': minute,
			'second': second
		}

		return cls.from_dict(**keys)

	@classmethod
	def from_string(cls, value: str) -> 'Timestamp':

		try:
			obj = pendulum.parse(value)
		except ValueError:
			if value.replace('.', '').isdigit():
				obj = cls.from_numeric_string(value)
			else:
				try:
					obj = cls.from_american_date(value)
				except ValueError:
					obj = cls.from_regex(value)

		return cls.from_object(obj)

	@classmethod
	def from_numeric_string(cls, value) -> 'Timestamp':
		""" Converts dates stored as 20250406 or 2025.04.06 """

		if '.' in value:
			year, month, day = value.split('.')
		else:
			year = int(value[:4])
			month = int(value[4:6])
			day = int(value[6:])

		year = _parse_year(year)
		month = _convert_month_to_integer(month)
		day = int(day)

		return cls(year = year, month = month, day = day)

	@classmethod
	def from_regex(cls, value: str, regex: str = None) -> 'Timestamp':
		""" Uses regular expressions to parse the input timestamp.
			Each regular expression should return a dictionary with the keys 'year', 'month', and 'day', and optionally 'hour', 'minute', and 'second'.
			Ex. '(?P<month>[a-z]+)\s(?P<day>[\d]+)[\s,]+(?P<year>[\d]{4})'
		"""
		pattern_time = "(?P<hour>[\d]+)?[:]?(?P<minute>[\d]+)?[:]?(?P<second>[\d]+)?"
		pattern_date_verbal_month_first = "(?P<month>[a-z]+)\s(?P<day>[\d]+)[\s,]+(?P<year>[\d]{4})" + "[\s]?" + pattern_time
		pattern_date_verbal_day_first = "(?P<day>[\d]+)[\s,]+(?P<month>[a-z]+)[.]?\s(?P<year>[\d]{4})" + "[\s]?" + pattern_time
		pattern_date_american = "(?P<month>[\d]+)[/](?P<day>[\d]+)[/](?P<year>[\d]{2,4})" + "[\sT]?" + pattern_time
		pattern_date_numeric = "(?P<year>[\d]{4})[.]?(?P<month>[\d]{2})[.]?(?P<day>[\d]{2})"
		regexes = [
			# American Dates. Ex. 04/06/2025 17:18:19
			# pattern_date_american, # Currently implemented as `cls.from_american_date`, which is faster.

			# 'Sun, 06 Apr 2025 16:00:33' or '17 Dec 2012'
			pattern_date_verbal_month_first,
			pattern_date_verbal_day_first,

			# '13 Sep. 2005', '1 Dec. 2021', "20 Apr. 2022"
			"(?P<day>[\d]{1,2})\s(?P<month>(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))[.]?\s(?P<year>[\d]{4})"
		]
		if regex is not None:
			regexes = [regex] + regexes

		# Ignore capitalization
		value = value.lower()
		for regex in regexes:
			match = re.search(regex, value)
			if match: break
		else:
			match = None

		if match:
			match = match.groupdict()
			match = _parse_datetime_dict(match)
			obj = cls.from_dict(**match)
		else:
			logger.debug(f"Regex failed: {value=}\t{match=}")
			obj = None
		return obj

	@classmethod
	def from_values(cls, year, month, day, hour = 0, minute = 0, second = 0, microsecond = 0, timezone = None) -> 'Timestamp':
		result = dict(
			year = year,
			month = month,
			day = day,
			hour = hour,
			minute = minute,
			second = second,
			microsecond = microsecond
		)
		return cls.from_dict(**result)

	def to_iso(self) -> str:
		return self.to_iso8601_string()

	def to_datetime(self) -> datetime.datetime:
		return datetime.datetime(
			year = self.year, month = self.month, day = self.day,
			hour = self.hour, minute = self.minute, second = self.second, microsecond = self.microsecond
		)


def main():
	import time
	values = [
		"4/6/25",
		"04/06/2025",
		"04/06/2025 17:18:19",
		"04/06/2025T17:18:19",
	]

	iterations = 1_000_000

	start = time.time()
	for _ in range(iterations):
		for value in values:
			date = Timestamp.from_american_date(value)
	duration = time.time() - start
	print(f"Finished in {duration:.02f} seconds")

	start = time.time()
	for _ in range(iterations):
		for value in values:
			date = Timestamp.from_regex(value)
	duration = time.time() - start
	print(f"Finished in {duration:.02f} seconds")


if __name__ == "__main__":
	main()
