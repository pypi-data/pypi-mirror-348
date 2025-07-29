from enum import Enum


class ColorSpace(Enum):
	SRGB = "srgb"
	SRGB_LINEAR = "srgb-linear"
	HSL = "hsl"
	HWB = "hwb"
	LAB = "lab"
	LCH = "lch"
	OKLAB = "oklab"
	OKLCH = "oklch"
	DISPLAY_P3 = "display-p3"
	A98_RGB = "a98-rgb"
	PROPHOTO_RGB = "prophoto-rgb"
	REC2020 = "rec2020"
	XYZ_D65 = "xyz-d65"
	XYZ_D50 = "xyz-d50"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member.value == value:
				return True
		return False


class Color:
	"""a color"""

	def __init__(
		self, color_space: ColorSpace, components: list[float], alpha: float = None, hexadecimal: str = None
	) -> None:
		self.color_space = color_space
		channel_spaces = {
			ColorSpace.SRGB,
			ColorSpace.SRGB_LINEAR,
			ColorSpace.DISPLAY_P3,
			ColorSpace.A98_RGB,
			ColorSpace.PROPHOTO_RGB,
			ColorSpace.REC2020,
			ColorSpace.XYZ_D50,
			ColorSpace.XYZ_D65,
		}
		hue_spaces = {ColorSpace.HSL, ColorSpace.HWB}
		space = {color_space}
		if space.issubset(channel_spaces):
			self.components = [
				min(max(components[0], 0.0), 1.0),
				min(max(components[1], 0.0), 1.0),
				min(max(components[2], 0.0), 1.0),
			]
		elif space.issubset(hue_spaces):
			self.components = [
				min(max(components[0], 0.0), 359.99999999999),
				min(max(components[1], 0.0), 100.0),
				min(max(components[2], 0.0), 100.0),
			]
		elif color_space == ColorSpace.OKLAB:
			self.components = [
				min(max(components[0], 0.0), 1.0),
				min(max(components[1], -0.5), 0.5),
				min(max(components[2], -0.5), 0.5),
			]
		elif color_space == ColorSpace.LAB:
			self.components = [
				min(max(components[0], 0.0), 100.0),
				min(max(components[1], -160.0), 160.0),
				min(max(components[2], -160.0), 160.0),
			]
		elif color_space == ColorSpace.OKLCH:
			self.components = [
				min(max(components[0], 0.0), 1.0),
				min(max(components[1], 0.0), 0.5),
				min(max(components[2], 0.0), 359.99999999999),
			]
		elif color_space == ColorSpace.LCH:
			self.components = [
				min(max(components[0], 0.0), 100.0),
				min(max(components[1], 0.0), 230.0),
				min(max(components[2], 0.0), 359.99999999999),
			]
		else:
			self.components = [0.0, 0.0, 0.0]

		self.alpha = alpha
		self.hex = hexadecimal


class Palette(Enum):
	"""Euma Color Palette"""

	RED_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.6588235294117647, 0.23921568627450981, 0.3333333333333333],
		1.0,
		"#a83d55",
	)
	RED_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.807843137254902, 0.28627450980392155, 0.403921568627451],
		1.0,
		"#ce4967",
	)
	RED_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.8941176470588236, 0.4196078431372549, 0.5098039215686274],
		1.0,
		"#e46b82",
	)
	RED_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9450980392156862, 0.5529411764705883, 0.615686274509804],
		1.0,
		"#f18d9d",
	)
	RED_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9764705882352941, 0.7019607843137254, 0.7372549019607844],
		1.0,
		"#f9b3bc",
	)
	GREEN_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.3254901960784314, 0.5490196078431373, 0.3176470588235294],
		1.0,
		"#538c51",
	)
	GREEN_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.36470588235294116, 0.7058823529411765, 0.3568627450980392],
		1.0,
		"#5db45b",
	)
	GREEN_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.47058823529411764, 0.8117647058823529, 0.4588235294117647],
		1.0,
		"#78cf75",
	)
	GREEN_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.592156862745098, 0.8784313725490196, 0.5764705882352941],
		1.0,
		"#97e093",
	)
	GREEN_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.7215686274509804, 0.9294117647058824, 0.7058823529411765],
		1.0,
		"#b8edb4",
	)
	BLUE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.2549019607843137, 0.3764705882352941, 0.43529411764705883],
		1.0,
		"#41606f",
	)
	BLUE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.2823529411764706, 0.5019607843137255, 0.6039215686274509],
		1.0,
		"#48809a",
	)
	BLUE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.3137254901960784, 0.6235294117647059, 0.7647058823529411],
		1.0,
		"#509fc3",
	)
	BLUE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.4196078431372549, 0.7058823529411765, 0.8392156862745098],
		1.0,
		"#6bb4d6",
	)
	BLUE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.5647058823529412, 0.807843137254902, 0.9254901960784314],
		1.0,
		"#90ceec",
	)
	CYAN_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.17254901960784313, 0.5843137254901961, 0.6],
		1.0,
		"#2c9599",
	)
	CYAN_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.16862745098039217, 0.7803921568627451, 0.803921568627451],
		1.0,
		"#2bc7cd",
	)
	CYAN_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.28627450980392155, 0.8705882352941177, 0.8941176470588236],
		1.0,
		"#49dee4",
	)
	CYAN_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.4196078431372549, 0.9333333333333333, 0.9529411764705882],
		1.0,
		"#6beef3",
	)
	CYAN_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.5725490196078431, 0.9686274509803922, 0.984313725490196],
		1.0,
		"#92f7fb",
	)
	MAGENTA_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.6313725490196078, 0.34901960784313724, 0.5647058823529412],
		1.0,
		"#a15990",
	)
	MAGENTA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.7490196078431373, 0.42745098039215684, 0.6745098039215687],
		1.0,
		"#bf6dac",
	)
	MAGENTA_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.8470588235294118, 0.5450980392156862, 0.7725490196078432],
		1.0,
		"#d88bc5",
	)
	MAGENTA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9137254901960784, 0.6627450980392157, 0.8470588235294118],
		1.0,
		"#e9a9d8",
	)
	MAGENTA_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9647058823529412, 0.796078431372549, 0.9176470588235294],
		1.0,
		"#f6cbea",
	)
	YELLOW_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.6627450980392157, 0.6196078431372549, 0.17647058823529413],
		1.0,
		"#a99e2d",
	)
	YELLOW_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.8470588235294118, 0.792156862745098, 0.19215686274509805],
		1.0,
		"#d8ca31",
	)
	YELLOW_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.9176470588235294, 0.8666666666666667, 0.33725490196078434],
		1.0,
		"#eadd56",
	)
	YELLOW_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9529411764705882, 0.9137254901960784, 0.48627450980392156],
		1.0,
		"#f3e97c",
	)
	YELLOW_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9764705882352941, 0.9490196078431372, 0.6392156862745098],
		1.0,
		"#f9f2a3",
	)
	PURPLE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.5098039215686274, 0.30980392156862746, 0.6901960784313725],
		1.0,
		"#824fb0",
	)
	PURPLE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.611764705882353, 0.40784313725490196, 0.8],
		1.0,
		"#9c68cc",
	)
	PURPLE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.7176470588235294, 0.5450980392156862, 0.8901960784313725],
		1.0,
		"#b78be3",
	)
	PURPLE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.803921568627451, 0.6784313725490196, 0.9411764705882353],
		1.0,
		"#cdadf0",
	)
	PURPLE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.8941176470588236, 0.8274509803921568, 0.9725490196078431],
		1.0,
		"#e4d3f8",
	)
	ORANGE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.6313725490196078, 0.4666666666666667, 0.20392156862745098],
		1.0,
		"#a17734",
	)
	ORANGE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.803921568627451, 0.592156862745098, 0.23137254901960785],
		1.0,
		"#cd973b",
	)
	ORANGE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.8941176470588236, 0.6901960784313725, 0.3686274509803922],
		1.0,
		"#e4b05e",
	)
	ORANGE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9333333333333333, 0.7647058823529411, 0.5098039215686274],
		1.0,
		"#eec382",
	)
	ORANGE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.9568627450980393, 0.8352941176470589, 0.6549019607843137],
		1.0,
		"#f4d5a7",
	)
	AQUA_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.19607843137254902, 0.5529411764705883, 0.49019607843137253],
		1.0,
		"#328d7d",
	)
	AQUA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.19607843137254902, 0.7450980392156863, 0.6588235294117647],
		1.0,
		"#32bea8",
	)
	AQUA_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.30980392156862746, 0.8627450980392157, 0.7686274509803922],
		1.0,
		"#4fdcc4",
	)
	AQUA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.43137254901960786, 0.9176470588235294, 0.8274509803921568],
		1.0,
		"#6eead3",
	)
	AQUA_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.6196078431372549, 1.0, 0.9215686274509803],
		1.0,
		"#9effeb",
	)
	DARK_1: Color = Color(
		ColorSpace.SRGB,
		[0.047058823529411764, 0.050980392156862744, 0.06274509803921569],
		1.0,
		"#0c0d10",
	)
	DARK_2: Color = Color(
		ColorSpace.SRGB,
		[0.09411764705882353, 0.09803921568627451, 0.10588235294117647],
		1.0,
		"#18191b",
	)
	DARK_3: Color = Color(
		ColorSpace.SRGB,
		[0.13725490196078433, 0.1411764705882353, 0.14901960784313725],
		1.0,
		"#232426",
	)
	DARK_4: Color = Color(
		ColorSpace.SRGB,
		[0.1843137254901961, 0.18823529411764706, 0.19607843137254902],
		1.0,
		"#2f3032",
	)
	DARK_5: Color = Color(
		ColorSpace.SRGB,
		[0.22745098039215686, 0.23137254901960785, 0.23921568627450981],
		1.0,
		"#3a3b3d",
	)
	DARK_6: Color = Color(
		ColorSpace.SRGB,
		[0.27450980392156865, 0.2784313725490196, 0.2823529411764706],
		1.0,
		"#464748",
	)
	DARK_7: Color = Color(
		ColorSpace.SRGB,
		[0.3215686274509804, 0.3215686274509804, 0.3254901960784314],
		1.0,
		"#525253",
	)
	DARK_8: Color = Color(
		ColorSpace.SRGB,
		[0.3686274509803922, 0.3686274509803922, 0.3686274509803922],
		1.0,
		"#5e5e5e",
	)
	DARK_9: Color = Color(
		ColorSpace.SRGB,
		[0.4117647058823529, 0.4117647058823529, 0.41568627450980394],
		1.0,
		"#69696a",
	)
	DARK_10: Color = Color(
		ColorSpace.SRGB,
		[0.4588235294117647, 0.4588235294117647, 0.4588235294117647],
		1.0,
		"#757575",
	)
	GRAY_NEUTRAL: Color = Color(
		ColorSpace.SRGB,
		[0.5019607843137255, 0.5019607843137255, 0.5058823529411764],
		1.0,
		"#808081",
	)
	LIGHT_10: Color = Color(
		ColorSpace.SRGB,
		[0.5490196078431373, 0.5490196078431373, 0.5490196078431373],
		1.0,
		"#8c8c8c",
	)
	LIGHT_9: Color = Color(
		ColorSpace.SRGB,
		[0.596078431372549, 0.596078431372549, 0.592156862745098],
		1.0,
		"#989897",
	)
	LIGHT_8: Color = Color(
		ColorSpace.SRGB,
		[0.6470588235294118, 0.6431372549019608, 0.6392156862745098],
		1.0,
		"#a5a4a3",
	)
	LIGHT_7: Color = Color(
		ColorSpace.SRGB,
		[0.6941176470588235, 0.6901960784313725, 0.6823529411764706],
		1.0,
		"#b1b0ae",
	)
	LIGHT_6: Color = Color(
		ColorSpace.SRGB,
		[0.7411764705882353, 0.7372549019607844, 0.7294117647058823],
		1.0,
		"#bdbcba",
	)
	LIGHT_5: Color = Color(
		ColorSpace.SRGB,
		[0.788235294117647, 0.7843137254901961, 0.7764705882352941],
		1.0,
		"#c9c8c6",
	)
	LIGHT_4: Color = Color(
		ColorSpace.SRGB,
		[0.8352941176470589, 0.8313725490196079, 0.8196078431372549],
		1.0,
		"#d5d4d1",
	)
	LIGHT_3: Color = Color(
		ColorSpace.SRGB,
		[0.8862745098039215, 0.8784313725490196, 0.8666666666666667],
		1.0,
		"#e2e0dd",
	)
	LIGHT_2: Color = Color(
		ColorSpace.SRGB,
		[0.9333333333333333, 0.9254901960784314, 0.9098039215686274],
		1.0,
		"#eeece8",
	)
	LIGHT_1: Color = Color(
		ColorSpace.SRGB,
		[0.9803921568627451, 0.9725490196078431, 0.9568627450980393],
		1.0,
		"#faf8f4",
	)


RED_EXTRA_DARK: Color = Palette.RED_EXTRA_DARK
RED_DARK: Color = Palette.RED_DARK
RED_MEDIUM: Color = Palette.RED_MEDIUM
RED_LIGHT: Color = Palette.RED_LIGHT
RED_EXTRA_LIGHT: Color = Palette.RED_EXTRA_LIGHT
GREEN_EXTRA_DARK: Color = Palette.GREEN_EXTRA_DARK
GREEN_DARK: Color = Palette.GREEN_DARK
GREEN_MEDIUM: Color = Palette.GREEN_MEDIUM
GREEN_LIGHT: Color = Palette.GREEN_LIGHT
GREEN_EXTRA_LIGHT: Color = Palette.GREEN_EXTRA_LIGHT
BLUE_EXTRA_DARK: Color = Palette.BLUE_EXTRA_DARK
BLUE_DARK: Color = Palette.BLUE_DARK
BLUE_MEDIUM: Color = Palette.BLUE_MEDIUM
BLUE_LIGHT: Color = Palette.BLUE_LIGHT
BLUE_EXTRA_LIGHT: Color = Palette.BLUE_EXTRA_LIGHT
CYAN_EXTRA_DARK: Color = Palette.CYAN_EXTRA_DARK
CYAN_DARK: Color = Palette.CYAN_DARK
CYAN_MEDIUM: Color = Palette.CYAN_MEDIUM
CYAN_LIGHT: Color = Palette.CYAN_LIGHT
CYAN_EXTRA_LIGHT: Color = Palette.CYAN_EXTRA_LIGHT
MAGENTA_EXTRA_DARK: Color = Palette.MAGENTA_EXTRA_DARK
MAGENTA_DARK: Color = Palette.MAGENTA_DARK
MAGENTA_MEDIUM: Color = Palette.MAGENTA_MEDIUM
MAGENTA_LIGHT: Color = Palette.MAGENTA_LIGHT
MAGENTA_EXTRA_LIGHT: Color = Palette.MAGENTA_EXTRA_LIGHT
YELLOW_EXTRA_DARK: Color = Palette.YELLOW_EXTRA_DARK
YELLOW_DARK: Color = Palette.YELLOW_DARK
YELLOW_MEDIUM: Color = Palette.YELLOW_MEDIUM
YELLOW_LIGHT: Color = Palette.YELLOW_LIGHT
YELLOW_EXTRA_LIGHT: Color = Palette.YELLOW_EXTRA_LIGHT
PURPLE_EXTRA_DARK: Color = Palette.PURPLE_EXTRA_DARK
PURPLE_DARK: Color = Palette.PURPLE_DARK
PURPLE_MEDIUM: Color = Palette.PURPLE_MEDIUM
PURPLE_LIGHT: Color = Palette.PURPLE_LIGHT
PURPLE_EXTRA_LIGHT: Color = Palette.PURPLE_EXTRA_LIGHT
ORANGE_EXTRA_DARK: Color = Palette.ORANGE_EXTRA_DARK
ORANGE_DARK: Color = Palette.ORANGE_DARK
ORANGE_MEDIUM: Color = Palette.ORANGE_MEDIUM
ORANGE_LIGHT: Color = Palette.ORANGE_LIGHT
ORANGE_EXTRA_LIGHT: Color = Palette.ORANGE_EXTRA_LIGHT
AQUA_EXTRA_DARK: Color = Palette.AQUA_EXTRA_DARK
AQUA_DARK: Color = Palette.AQUA_DARK
AQUA_MEDIUM: Color = Palette.AQUA_MEDIUM
AQUA_LIGHT: Color = Palette.AQUA_LIGHT
AQUA_EXTRA_LIGHT: Color = Palette.AQUA_EXTRA_LIGHT
DARK_1: Color = Palette.DARK_1
DARK_2: Color = Palette.DARK_2
DARK_3: Color = Palette.DARK_3
DARK_4: Color = Palette.DARK_4
DARK_5: Color = Palette.DARK_5
DARK_6: Color = Palette.DARK_6
DARK_7: Color = Palette.DARK_7
DARK_8: Color = Palette.DARK_8
DARK_9: Color = Palette.DARK_9
DARK_10: Color = Palette.DARK_10
GRAY_NEUTRAL: Color = Palette.GRAY_NEUTRAL
LIGHT_10: Color = Palette.LIGHT_10
LIGHT_9: Color = Palette.LIGHT_9
LIGHT_8: Color = Palette.LIGHT_8
LIGHT_7: Color = Palette.LIGHT_7
LIGHT_6: Color = Palette.LIGHT_6
LIGHT_5: Color = Palette.LIGHT_5
LIGHT_4: Color = Palette.LIGHT_4
LIGHT_3: Color = Palette.LIGHT_3
LIGHT_2: Color = Palette.LIGHT_2
LIGHT_1: Color = Palette.LIGHT_1
