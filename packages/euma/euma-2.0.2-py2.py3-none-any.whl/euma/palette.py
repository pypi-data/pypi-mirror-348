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
				min(max(components[0], 0.0), 359.999_999_999_999),
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
				min(max(components[2], 0.0), 359.999_999_999_999),
			]
		elif color_space == ColorSpace.LCH:
			self.components = [
				min(max(components[0], 0.0), 100.0),
				min(max(components[1], 0.0), 230.0),
				min(max(components[2], 0.0), 359.999_999_999_999),
			]
		else:
			self.components = [0.0, 0.0, 0.0]

		self.alpha = alpha
		self.hex = hexadecimal


class Palette(Enum):
	"""Euma Color Palette"""

	RED_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.658_823_529_411_764_7, 0.239_215_686_274_509_81, 0.333_333_333_333_333_3],
		1.0,
		"#a83d55",
	)
	RED_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.807_843_137_254_902, 0.286_274_509_803_921_55, 0.403_921_568_627_451],
		1.0,
		"#ce4967",
	)
	RED_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.894_117_647_058_823_6, 0.419_607_843_137_254_9, 0.509_803_921_568_627_4],
		1.0,
		"#e46b82",
	)
	RED_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.945_098_039_215_686_2, 0.552_941_176_470_588_3, 0.615_686_274_509_804],
		1.0,
		"#f18d9d",
	)
	RED_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.976_470_588_235_294_1, 0.701_960_784_313_725_4, 0.737_254_901_960_784_4],
		1.0,
		"#f9b3bc",
	)
	GREEN_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.325_490_196_078_431_4, 0.549_019_607_843_137_3, 0.317_647_058_823_529_4],
		1.0,
		"#538c51",
	)
	GREEN_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.364_705_882_352_941_16, 0.705_882_352_941_176_5, 0.356_862_745_098_039_2],
		1.0,
		"#5db45b",
	)
	GREEN_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.470_588_235_294_117_64, 0.811_764_705_882_352_9, 0.458_823_529_411_764_7],
		1.0,
		"#78cf75",
	)
	GREEN_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.592_156_862_745_098, 0.878_431_372_549_019_6, 0.576_470_588_235_294_1],
		1.0,
		"#97e093",
	)
	GREEN_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.721_568_627_450_980_4, 0.929_411_764_705_882_4, 0.705_882_352_941_176_5],
		1.0,
		"#b8edb4",
	)
	BLUE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.254_901_960_784_313_7, 0.376_470_588_235_294_1, 0.435_294_117_647_058_83],
		1.0,
		"#41606f",
	)
	BLUE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.282_352_941_176_470_6, 0.501_960_784_313_725_5, 0.603_921_568_627_450_9],
		1.0,
		"#48809a",
	)
	BLUE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.313_725_490_196_078_4, 0.623_529_411_764_705_9, 0.764_705_882_352_941_1],
		1.0,
		"#509fc3",
	)
	BLUE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.419_607_843_137_254_9, 0.705_882_352_941_176_5, 0.839_215_686_274_509_8],
		1.0,
		"#6bb4d6",
	)
	BLUE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.564_705_882_352_941_2, 0.807_843_137_254_902, 0.925_490_196_078_431_4],
		1.0,
		"#90ceec",
	)
	CYAN_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.172_549_019_607_843_13, 0.584_313_725_490_196_1, 0.6],
		1.0,
		"#2c9599",
	)
	CYAN_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.168_627_450_980_392_17, 0.780_392_156_862_745_1, 0.803_921_568_627_451],
		1.0,
		"#2bc7cd",
	)
	CYAN_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.286_274_509_803_921_55, 0.870_588_235_294_117_7, 0.894_117_647_058_823_6],
		1.0,
		"#49dee4",
	)
	CYAN_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.419_607_843_137_254_9, 0.933_333_333_333_333_3, 0.952_941_176_470_588_2],
		1.0,
		"#6beef3",
	)
	CYAN_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.572_549_019_607_843_1, 0.968_627_450_980_392_2, 0.984_313_725_490_196],
		1.0,
		"#92f7fb",
	)
	MAGENTA_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.631_372_549_019_607_8, 0.349_019_607_843_137_24, 0.564_705_882_352_941_2],
		1.0,
		"#a15990",
	)
	MAGENTA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.749_019_607_843_137_3, 0.427_450_980_392_156_84, 0.674_509_803_921_568_7],
		1.0,
		"#bf6dac",
	)
	MAGENTA_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.847_058_823_529_411_8, 0.545_098_039_215_686_2, 0.772_549_019_607_843_2],
		1.0,
		"#d88bc5",
	)
	MAGENTA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.913_725_490_196_078_4, 0.662_745_098_039_215_7, 0.847_058_823_529_411_8],
		1.0,
		"#e9a9d8",
	)
	MAGENTA_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.964_705_882_352_941_2, 0.796_078_431_372_549, 0.917_647_058_823_529_4],
		1.0,
		"#f6cbea",
	)
	YELLOW_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.662_745_098_039_215_7, 0.619_607_843_137_254_9, 0.176_470_588_235_294_13],
		1.0,
		"#a99e2d",
	)
	YELLOW_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.847_058_823_529_411_8, 0.792_156_862_745_098, 0.192_156_862_745_098_05],
		1.0,
		"#d8ca31",
	)
	YELLOW_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.917_647_058_823_529_4, 0.866_666_666_666_666_7, 0.337_254_901_960_784_34],
		1.0,
		"#eadd56",
	)
	YELLOW_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.952_941_176_470_588_2, 0.913_725_490_196_078_4, 0.486_274_509_803_921_56],
		1.0,
		"#f3e97c",
	)
	YELLOW_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.976_470_588_235_294_1, 0.949_019_607_843_137_2, 0.639_215_686_274_509_8],
		1.0,
		"#f9f2a3",
	)
	PURPLE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.509_803_921_568_627_4, 0.309_803_921_568_627_46, 0.690_196_078_431_372_5],
		1.0,
		"#824fb0",
	)
	PURPLE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.611_764_705_882_353, 0.407_843_137_254_901_96, 0.8],
		1.0,
		"#9c68cc",
	)
	PURPLE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.717_647_058_823_529_4, 0.545_098_039_215_686_2, 0.890_196_078_431_372_5],
		1.0,
		"#b78be3",
	)
	PURPLE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.803_921_568_627_451, 0.678_431_372_549_019_6, 0.941_176_470_588_235_3],
		1.0,
		"#cdadf0",
	)
	PURPLE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.894_117_647_058_823_6, 0.827_450_980_392_156_8, 0.972_549_019_607_843_1],
		1.0,
		"#e4d3f8",
	)
	ORANGE_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.631_372_549_019_607_8, 0.466_666_666_666_666_7, 0.203_921_568_627_450_98],
		1.0,
		"#a17734",
	)
	ORANGE_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.803_921_568_627_451, 0.592_156_862_745_098, 0.231_372_549_019_607_85],
		1.0,
		"#cd973b",
	)
	ORANGE_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.894_117_647_058_823_6, 0.690_196_078_431_372_5, 0.368_627_450_980_392_2],
		1.0,
		"#e4b05e",
	)
	ORANGE_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.933_333_333_333_333_3, 0.764_705_882_352_941_1, 0.509_803_921_568_627_4],
		1.0,
		"#eec382",
	)
	ORANGE_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.956_862_745_098_039_3, 0.835_294_117_647_058_9, 0.654_901_960_784_313_7],
		1.0,
		"#f4d5a7",
	)
	AQUA_EXTRA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.196_078_431_372_549_02, 0.552_941_176_470_588_3, 0.490_196_078_431_372_53],
		1.0,
		"#328d7d",
	)
	AQUA_DARK: Color = Color(
		ColorSpace.SRGB,
		[0.196_078_431_372_549_02, 0.745_098_039_215_686_3, 0.658_823_529_411_764_7],
		1.0,
		"#32bea8",
	)
	AQUA_MEDIUM: Color = Color(
		ColorSpace.SRGB,
		[0.309_803_921_568_627_46, 0.862_745_098_039_215_7, 0.768_627_450_980_392_2],
		1.0,
		"#4fdcc4",
	)
	AQUA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.431_372_549_019_607_86, 0.917_647_058_823_529_4, 0.827_450_980_392_156_8],
		1.0,
		"#6eead3",
	)
	AQUA_EXTRA_LIGHT: Color = Color(
		ColorSpace.SRGB,
		[0.619_607_843_137_254_9, 1.0, 0.921_568_627_450_980_3],
		1.0,
		"#9effeb",
	)
	DARK_1: Color = Color(
		ColorSpace.SRGB,
		[0.047_058_823_529_411_764, 0.050_980_392_156_862_744, 0.062_745_098_039_215_69],
		1.0,
		"#0c0d10",
	)
	DARK_2: Color = Color(
		ColorSpace.SRGB,
		[0.094_117_647_058_823_53, 0.098_039_215_686_274_51, 0.105_882_352_941_176_47],
		1.0,
		"#18191b",
	)
	DARK_3: Color = Color(
		ColorSpace.SRGB,
		[0.137_254_901_960_784_33, 0.141_176_470_588_235_3, 0.149_019_607_843_137_25],
		1.0,
		"#232426",
	)
	DARK_4: Color = Color(
		ColorSpace.SRGB,
		[0.184_313_725_490_196_1, 0.188_235_294_117_647_06, 0.196_078_431_372_549_02],
		1.0,
		"#2f3032",
	)
	DARK_5: Color = Color(
		ColorSpace.SRGB,
		[0.227_450_980_392_156_86, 0.231_372_549_019_607_85, 0.239_215_686_274_509_81],
		1.0,
		"#3a3b3d",
	)
	DARK_6: Color = Color(
		ColorSpace.SRGB,
		[0.274_509_803_921_568_65, 0.278_431_372_549_019_6, 0.282_352_941_176_470_6],
		1.0,
		"#464748",
	)
	DARK_7: Color = Color(
		ColorSpace.SRGB,
		[0.321_568_627_450_980_4, 0.321_568_627_450_980_4, 0.325_490_196_078_431_4],
		1.0,
		"#525253",
	)
	DARK_8: Color = Color(
		ColorSpace.SRGB,
		[0.368_627_450_980_392_2, 0.368_627_450_980_392_2, 0.368_627_450_980_392_2],
		1.0,
		"#5e5e5e",
	)
	DARK_9: Color = Color(
		ColorSpace.SRGB,
		[0.411_764_705_882_352_9, 0.411_764_705_882_352_9, 0.415_686_274_509_803_94],
		1.0,
		"#69696a",
	)
	DARK_10: Color = Color(
		ColorSpace.SRGB,
		[0.458_823_529_411_764_7, 0.458_823_529_411_764_7, 0.458_823_529_411_764_7],
		1.0,
		"#757575",
	)
	GRAY_NEUTRAL: Color = Color(
		ColorSpace.SRGB,
		[0.501_960_784_313_725_5, 0.501_960_784_313_725_5, 0.505_882_352_941_176_4],
		1.0,
		"#808081",
	)
	LIGHT_10: Color = Color(
		ColorSpace.SRGB,
		[0.549_019_607_843_137_3, 0.549_019_607_843_137_3, 0.549_019_607_843_137_3],
		1.0,
		"#8c8c8c",
	)
	LIGHT_9: Color = Color(
		ColorSpace.SRGB,
		[0.596_078_431_372_549, 0.596_078_431_372_549, 0.592_156_862_745_098],
		1.0,
		"#989897",
	)
	LIGHT_8: Color = Color(
		ColorSpace.SRGB,
		[0.647_058_823_529_411_8, 0.643_137_254_901_960_8, 0.639_215_686_274_509_8],
		1.0,
		"#a5a4a3",
	)
	LIGHT_7: Color = Color(
		ColorSpace.SRGB,
		[0.694_117_647_058_823_5, 0.690_196_078_431_372_5, 0.682_352_941_176_470_6],
		1.0,
		"#b1b0ae",
	)
	LIGHT_6: Color = Color(
		ColorSpace.SRGB,
		[0.741_176_470_588_235_3, 0.737_254_901_960_784_4, 0.729_411_764_705_882_3],
		1.0,
		"#bdbcba",
	)
	LIGHT_5: Color = Color(
		ColorSpace.SRGB,
		[0.788_235_294_117_647, 0.784_313_725_490_196_1, 0.776_470_588_235_294_1],
		1.0,
		"#c9c8c6",
	)
	LIGHT_4: Color = Color(
		ColorSpace.SRGB,
		[0.835_294_117_647_058_9, 0.831_372_549_019_607_9, 0.819_607_843_137_254_9],
		1.0,
		"#d5d4d1",
	)
	LIGHT_3: Color = Color(
		ColorSpace.SRGB,
		[0.886_274_509_803_921_5, 0.878_431_372_549_019_6, 0.866_666_666_666_666_7],
		1.0,
		"#e2e0dd",
	)
	LIGHT_2: Color = Color(
		ColorSpace.SRGB,
		[0.933_333_333_333_333_3, 0.925_490_196_078_431_4, 0.909_803_921_568_627_4],
		1.0,
		"#eeece8",
	)
	LIGHT_1: Color = Color(
		ColorSpace.SRGB,
		[0.980_392_156_862_745_1, 0.972_549_019_607_843_1, 0.956_862_745_098_039_3],
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
