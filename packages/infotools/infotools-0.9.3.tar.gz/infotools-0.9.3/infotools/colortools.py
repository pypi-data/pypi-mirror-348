from typing import *
import matplotlib.colors as mcolors
import numpy
import re
import random
import ctypes
RGBType = Tuple[int, int, int]
HexType = NewType("HexType", str)

matplotlib_colors = {**mcolors.BASE_COLORS, **mcolors.TABLEAU_COLORS, **mcolors.CSS4_COLORS, **mcolors.XKCD_COLORS}

marker_colormaps = {
	'PD-1':  "Blues_r",
	'SOX10': 'Oranges_r',
	'CD68':  'Reds_r',
	'CD3':   'Greens_r',
	'CD8':   'YlOrBr_r',
	'PD-L1': "Purples_r",
	'DAPI':  None
}

REGEX_COLOR = re.compile("^(?:#[0-9A-Fa-f]{6})|(?:tab:[a-z]+)")

palette_distinct = [
	'#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231',
	'#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
	'#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
	'#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080'
]


def is_number(value: Any) -> bool:
	try:
		float(value)
		result = True
	except ValueError:
		result = False
	return result


def is_hex_color(value: Any) -> bool:
	if isinstance(value, str):
		pattern = "[#][0-9ABCDEF]{6}"
		result = bool(re.search(pattern, value))
	else:
		result = False
	return result


def is_rgb_color(value: Any) -> bool:
	if isinstance(value, (tuple, list, numpy.ndarray)) and len(value) == 3:
		is_numbertype = all([is_number(i) for i in value])

		if is_numbertype:
			result = all([i < 256 for i in value])
		else:
			result = False

	elif isinstance(value, str):
		try:
			value = string_to_rgb(value)
			result = is_rgb_color(value)
		except ValueError:
			result = False
	else:
		result = False
	return result


def hex_to_rgb(string, as_sRGB: bool = False) -> Tuple[int, int, int]:
	red = string[1:3]
	green = string[3:5]
	blue = string[5:7]

	red = int(red, 16)
	green = int(green, 16)
	blue = int(blue, 16)

	if as_sRGB:
		red = red / 55
		green = green / 255
		blue = blue / 255

	return red, green, blue


def string_to_rgb(value: str) -> List[int]:
	""" Converts a string into a list of integers """
	return [int(i.strip()) for i in value.split(',')]


def rgb_to_hex(value: Union[str, Tuple[int, int, int]]) -> str:
	""" Converts the color specified in the tiff file to hex format. The color is usually given as either as a string ('255,0,255') or tuple ((255, 0, 255))"""
	if isinstance(value, str):
		value = string_to_rgb(value)

	if all(i < 1 for i in value):  # Float RGB format
		color = mcolors.rgb2hex(value).upper()
	else:
		value = [int(i) for i in value]
		value_red, value_green, value_blue, *extra = value
		color = f"#{value_red:>02X}{value_green:>02X}{value_blue:>02X}"
	return color


def convert_to_hex(value: Union[RGBType, HexType, str]) -> HexType:
	"""
		Converts the input color into a hex color code.

	Parameters
	----------
	value: Union[RGBType, HexType, str]
		- `RGBType`: Tuple of ints
		- `HexType`: A hex color code
		- `str`: The name of a CSS color

	Returns
	-------
		HexType
	"""

	if is_hex_color(value):
		result = value
	elif is_rgb_color(value):
		result = rgb_to_hex(value)
	elif isinstance(value, str) and value.lower() in matplotlib_colors:
		value = matplotlib_colors[value.lower()]
		result = convert_to_hex(value)
	else:
		message = f"Cannot convert '{value}' int a hex color code!"
		raise ValueError(message)
	return result


def convert_to_luminance_factor(value: float) -> float:
	""" Converts an sRGB value to whatever unit luminance uses. """
	if value < 0.03928:
		value = value / 12.92
	else:
		value = ((value + 0.055) / 1.055) ** 2.4
	return value


def calculate_luminance(rgb: Tuple[int, int, int]) -> float:
	red, green, blue = rgb
	red = convert_to_luminance_factor(red)
	green = convert_to_luminance_factor(green)
	blue = convert_to_luminance_factor(blue)

	luminance = (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)
	if luminance == 0:
		luminance = 1
	return luminance


def calculate_contrast(color_1: str, color_2: str) -> float:
	rgb_1 = hex_to_rgb(color_1, as_sRGB = True)
	rgb_2 = hex_to_rgb(color_2, as_sRGB = True)
	# the relative luminance of the lighter colour (L1) is divided through the relative luminance of the darker colour (L2):
	l_1 = calculate_luminance(rgb_1)
	l_2 = calculate_luminance(rgb_2)
	# Check if the darker/lighter color was reversed
	if l_2 > l_1:
		l_1, l_2 = l_2, l_1

	ratio = (l_1 + 0.05) / (l_2 / 0.05)

	return ratio


def convert_color_to_integer(color: str):
	"""
		inverse of `convert_integer_to_color()`

	Parameters
	----------
	color:str
		The hex-formatted color value. Only the RGB component is returned (no alpha).

	Returns
	-------
	int:int
		The integer representation of a signed 32-bit integer in which the hex color code is encoded in the hex representation of the integer.
	"""

	value = "0x" + color[1:] + 'FF'
	# value = "ctypes.c_int32({value})"
	# command = f"struct.unpack('>i', {value})"
	command = f"ctypes.c_int32({value})"
	number = eval(command)

	# color = bytes_to_hex(packed_value)[:-2].upper() # Upper so it's consistent with other representations of the color.
	return number.value


def convert_integer_to_color(integer: int) -> str:
	"""
		Colors in OME formatted descriptions are encoded as signed 32-bit integers,
		so the byte representation represents the hex code of the color.
		The default value "-1" is #FFFFFFFF so solid white (it is a signed 32 bit value)
	Parameters
	----------
	integer:int
		The integer representation of a signed 32-bit integer in which the hex color code is encoded in the hex representation of the integer.

	Returns
	-------
	str
		The hex-formatted color value. Only the RGB component is returned (no alpha).
	"""
	binary_string = integer.to_bytes(4, 'big', signed = True)
	hex_string = binary_string.hex()
	return '#' + hex_string[:-2].upper()

def get_random_color(lower: int = 50, upper: int = 250) -> str:
	""" Generates a random hex color code. """
	red = random.randint(lower, upper)
	green = random.randint(lower, upper)
	blue = random.randint(lower, upper)
	return f"#{red:>02X}{green:>02X}{blue:>02X}"