"""
	A suite of tests to ensure timetools.Timestamp is operating properly.
"""
import datetime

import pandas
import pendulum
import pytest

from infotools import timetools


@pytest.fixture
def timestamp():
	key = "2019-05-06 00:14:26.246155"
	ts = datetime.datetime(2019, 5, 6, 0, 14, 26, 246155)
	return pendulum.parse("2019-05-06 00:14:26.246155Z")


@pytest.mark.parametrize(
	"value, expected",
	[
		("January", 1),
		("May", 5),
		("september", 9),
		("sep", 9),
		("dec", 12),
		(9, 9),
		("9", 9),
		("09", 9)
	]
)
def test_convert_month_to_integer(value, expected):
	assert timetools._timestamp._convert_month_to_integer(value) == expected


@pytest.mark.parametrize(
	"value, expected",
	[
		("1992", 1992),
		("92", 1992),
		("2025", 2025),
		("25", 2025),
		(25, 2025),
		(45, 2045),
		(51, 1951),
		(40, 2040),
		(70, 1970)
	]
)
def test_parse_year(value, expected):
	assert timetools._timestamp._parse_year(value) == expected


@pytest.mark.parametrize(
	"data",
	[
		"05/06/2019",
		{'year': 2019, 'month': 5, 'day': 6},
		{'year': 2019, 'month': 5, 'day': 6, 'hour': 0, 'minute': 14, 'second': 26, 'microsecond': 246155},
		(2019, 5, 6),
		(2019, 5, 6, 0, 14, 26, 246155),
		"may 6, 2019",
		"06 may 2019",
		pandas.Timestamp(year = 2019, month = 5, day = 6)
	]
)
def test_parse_timestamp_date(data, timestamp):
	result = timetools.Timestamp(data).date()

	assert result == timestamp.date()


@pytest.mark.parametrize(
	"data",
	[
		{'year': 2019, 'month': 5, 'day': 6, 'hour': 0, 'minute': 14, 'second': 26, 'microsecond': 246155},
		(2019, 5, 6, 0, 14, 26, 246155),
		datetime.datetime(2019, 5, 6, 0, 14, 26, 246155),

	]
)
def test_parse_timestamp_datetime(data, timestamp):
	result = timetools.Timestamp(data)
	assert result == timestamp


def test_to_float():
	ts = timetools.Timestamp((2019, 2, 13))
	expected = 2019 + (44 / 365)
	assert float(ts) == expected


def test_to_iso(timestamp):
	expected = timestamp.to_iso8601_string().split('+')[0][:-1]  # Remove the timezone
	result = timetools.Timestamp(timestamp.to_iso8601_string()).to_iso()

	assert result == expected


@pytest.mark.parametrize(
	"value, expected",
	[
		("03/01/20", "2020-03-01")
	]
)
def test_misc(value, expected):
	result = timetools.Timestamp(value)

	assert result.to_iso().split('T')[0] == expected


@pytest.mark.parametrize(
	"string, expected",
	[
		('2016-11-16 22:32:05', datetime.datetime(2016, 11, 16, hour = 22, minute = 32, second = 5)),
		('2010-11-12', datetime.datetime(year = 2010, month = 11, day = 12)),
		('Thu, 31 Mar 2022 22:59:00 -0000', datetime.datetime(year = 2022, month = 3, day = 31, hour = 22, minute = 59, second = 0)),
		('Thu, 31 Mar 2022 22:59:00 -0000', datetime.datetime(year = 2022, month = 3, day = 31, hour = 22, minute = 59, second = 0)),
		("20 Apr. 2022", datetime.datetime(year = 2022, month = 4, day = 20)),
		('13 Sep. 2005', datetime.datetime(year = 2005, month = 9, day = 13)),
		('1 Dec. 2021', datetime.datetime(year = 2021, month = 12, day = 1)),
		('22 Dec. 2019', datetime.datetime(year = 2019, month = 12, day = 22))
	]
)
def test_to_datetime(string, expected):
	# '2016-11-16 22:32:05'
	result = timetools.Timestamp(string).to_datetime()
	assert result == expected


@pytest.mark.parametrize(
	"string, expected",
	[
		("20 Apr. 2022", datetime.datetime(year = 2022, month = 4, day = 20)),
		('13 Sep. 2005', datetime.datetime(year = 2005, month = 9, day = 13)),
		('1 Dec. 2021', datetime.datetime(year = 2021, month = 12, day = 1)),
		('22 Dec. 2019', datetime.datetime(year = 2019, month = 12, day = 22)),
		('Sun, 06 Apr 2025 16:00:00 +0000', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 0)),
		('Sun, 06 Apr 2025 16:00:33.5', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 33)),
		('06 Apr 2025 16:00:33.5', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 33))
	]
)
def test_from_regex(string, expected):
	result = timetools.Timestamp.from_regex(string)
	assert result == expected


@pytest.mark.parametrize(
	"string, expected",
	[
		("20250604", datetime.datetime(2025, 6, 4)),
		("2025.06.04", datetime.datetime(2025, 6, 4)),
		("2025.6.4", datetime.datetime(2025, 6, 4))
	]
)
def test_from_numeric_string(string, expected):
	assert timetools.Timestamp.from_numeric_string(string) == expected


@pytest.mark.parametrize(
	"value, expected",
	[
		("20250604", datetime.datetime(2025, 6, 4)),
		("2025.06.04", datetime.datetime(2025, 6, 4)),
		("2025.6.4", datetime.datetime(2025, 6, 4)),
		({'year': 2019, 'month': 5, 'day': 6, 'hour': 0, 'minute': 14, 'second': 26, 'microsecond': 246155}, datetime.datetime(2019, 5, 6, 0, 14, 26, 246155)),
		("20 Apr. 2022", datetime.datetime(year = 2022, month = 4, day = 20)),
		('13 Sep. 2005', datetime.datetime(year = 2005, month = 9, day = 13)),
		('Sun, 06 Apr 2025 16:00:00 +0000', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 0)),
		('Sun, 06 Apr 2025 16:00:33.5', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 33)),
		('06 Apr 2025 16:00:33.5', datetime.datetime(year = 2025, month = 4, day = 6, hour = 16, minute = 0, second = 33)),
		(datetime.datetime(2019, 5, 6, 0, 14, 26, 246155), datetime.datetime(2019, 5, 6, 0, 14, 26, 246155)),
		(pendulum.datetime(2019, 5, 6, 0, 14, 26, 246155), datetime.datetime(2019, 5, 6, 0, 14, 26, 246155))
	]
)
def test_timestamp(value, expected):
	assert timetools.Timestamp(value) == expected
