from enum import Enum

from euma.palette import Color


class CubicBezier:
	"""the timing function definition, of how to transition between two states"""

	def __init__(self, p1x: float, p1y: float, p2x: float, p2y: float) -> None:
		self.p1x = p1x
		self.p1y = p1y
		self.p2x = p2x
		self.p2y = p2y

	@property
	def p1x(self) -> float:
		return self._p1x

	@p1x.setter
	def p1x(self, value: float) -> None:
		self._p1x = min(max(value, 0.0), 1.0)

	@property
	def p2x(self) -> float:
		return self._p2x

	@p2x.setter
	def p2x(self, value: float) -> None:
		self._p2x = min(max(value, 0.0), 1.0)


class DimensionalUnit(Enum):
	PX = "px"
	REM = "rem"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member.value == value:
				return True
		return False


class Dimension:
	"""a measure of distance,length,..."""

	def __init__(self, value: int | float, unit: DimensionalUnit) -> None:
		self.value = value
		self.unit = unit


class TemporalUnit(Enum):
	SECONDS = "s"
	MILLI_SECONDS = "ms"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class Duration:
	"""a measure of time, duration,..."""

	def __init__(self, value: int | float, unit: TemporalUnit) -> None:
		self.value = value
		self.unit = unit


class FontFamily:
	"""the names of font families"""

	def __init__(self, families: list[str]) -> None:
		self.families = families


class FontWeight(Enum):
	"""the thickness of each letter, (100,slim) to (950,thick)"""

	W100 = 100
	THIN = 100
	HAIRLINE = 100
	W200 = 200
	EXTRA_LIGHT = 200
	ULTRA_LIGHT = 200
	W300 = 300
	LIGHT = 300
	W400 = 400
	NORMAL = 400
	REGULAR = 400
	BOOK = 400
	W500 = 500
	MEDIUM = 500
	W600 = 600
	SEMI_BOLD = 600
	DEMI_BOLD = 600
	W700 = 700
	BOLD = 700
	W800 = 800
	EXTRA_BOLD = 800
	ULTRA_BOLD = 800
	W900 = 900
	BLACK = 900
	HEAVY = 900
	W950 = 950
	EXTRA_BLACK = 950
	ULTRA_BLACK = 950

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class Typography:
	"""~description~"""

	def __init__(
		self,
		font_family: FontFamily,
		font_size: Dimension,
		font_weight: FontWeight,
		letter_spacing: Dimension,
		line_height: int | float,
	) -> None:
		self.font_family = font_family
		self.font_size = font_size
		self.font_weight = font_weight
		self.letter_spacing = letter_spacing
		self.line_height = line_height


class Transition:
	"""~description~"""

	def __init__(self, duration: Duration, delay: Duration, timing_function: CubicBezier) -> None:
		self.duration = duration
		self.delay = delay
		self.timing_function = timing_function


class LineCap(Enum):
	ROUND = "round"
	BUTT = "butt"
	SQUARE = "square"


class StrokeStyle:
	"""~description~"""

	SOLID = "solid"
	DASHED = "dashed"
	DOTTED = "dotted"
	DOUBLE = "double"
	GROOVE = "groove"
	RIDGE = "ridge"
	OUTSET = "outset"
	INSET = "inset"

	def __init__(self, dash_array: list[Dimension] = None, line_cap: LineCap = None) -> None:
		self.dash_array = dash_array
		self.line_cap = line_cap


class Shadow:
	"""~description~"""

	def __init__(
		self,
		offset_x: Dimension,
		offset_y: Dimension,
		blur: Dimension,
		spread: Dimension,
		color: Color,
		inset: bool = False,
	) -> None:
		self.offset_x = offset_x
		self.offset_y = offset_y
		self.blur = blur
		self.spread = spread
		self.color = color
		self.inset = inset


class GradientStop:
	def __init__(self, color: Color, position: float) -> None:
		self.color = color
		self.position = min(max(position, 0.0), 1.0)

	@property
	def position(self) -> float:
		return self._position

	@position.setter
	def position(self, value: float) -> None:
		self._position = min(max(value, 0.0), 1.0)


class Gradient:
	"""~description~"""

	_MIN_STOPS = 2

	def __init__(self, stops: list[GradientStop]) -> None:
		if len(stops) < self._MIN_STOPS:
			raise Exception("there need to be at least to 'GradientStop' to make a 'Gradient'; Count: " + len(stops))
		self.stops = stops


class Border:
	"""~description~"""

	def __init__(self, color: Color, width: Dimension, style: StrokeStyle) -> None:
		self.color = color
		self.width = width
		self.style = style


class StylisticSetId(Enum):
	SS01 = "ss01"
	SS02 = "ss02"
	SS03 = "ss03"
	SS04 = "ss04"
	SS05 = "ss05"
	SS06 = "ss06"
	SS07 = "ss07"
	SS08 = "ss08"
	SS09 = "ss09"
	SS10 = "ss10"
	SS11 = "ss11"
	SS12 = "ss12"
	SS13 = "ss13"
	SS14 = "ss14"
	SS15 = "ss15"
	SS16 = "ss16"
	SS17 = "ss17"
	SS18 = "ss18"
	SS19 = "ss19"
	SS20 = "ss20"


class StylisticSet:
	"""~description-stylisticSets~"""

	def __init__(self, identifier: StylisticSetId, value: bool) -> None:
		self.id = identifier
		self.value = value


class CharacterVariantId(Enum):
	CV01 = "cv01"
	CV02 = "cv02"
	CV03 = "cv03"
	CV04 = "cv04"
	CV05 = "cv05"
	CV06 = "cv06"
	CV07 = "cv07"
	CV08 = "cv08"
	CV09 = "cv09"
	CV10 = "cv10"
	CV11 = "cv11"
	CV12 = "cv12"
	CV13 = "cv13"
	CV14 = "cv14"
	CV15 = "cv15"
	CV16 = "cv16"
	CV17 = "cv17"
	CV18 = "cv18"
	CV19 = "cv19"
	CV20 = "cv20"
	CV21 = "cv21"
	CV22 = "cv22"
	CV23 = "cv23"
	CV24 = "cv24"
	CV25 = "cv25"
	CV26 = "cv26"
	CV27 = "cv27"
	CV28 = "cv28"
	CV29 = "cv29"
	CV30 = "cv30"
	CV31 = "cv31"
	CV32 = "cv32"
	CV33 = "cv33"
	CV34 = "cv34"
	CV35 = "cv35"
	CV36 = "cv36"
	CV37 = "cv37"
	CV38 = "cv38"
	CV39 = "cv39"
	CV40 = "cv40"
	CV41 = "cv41"
	CV42 = "cv42"
	CV43 = "cv43"
	CV44 = "cv44"
	CV45 = "cv45"
	CV46 = "cv46"
	CV47 = "cv47"
	CV48 = "cv48"
	CV49 = "cv49"
	CV50 = "cv50"
	CV51 = "cv51"
	CV52 = "cv52"
	CV53 = "cv53"
	CV54 = "cv54"
	CV55 = "cv55"
	CV56 = "cv56"
	CV57 = "cv57"
	CV58 = "cv58"
	CV59 = "cv59"
	CV60 = "cv60"
	CV61 = "cv61"
	CV62 = "cv62"
	CV63 = "cv63"
	CV64 = "cv64"
	CV65 = "cv65"
	CV66 = "cv66"
	CV67 = "cv67"
	CV68 = "cv68"
	CV69 = "cv69"
	CV70 = "cv70"
	CV71 = "cv71"
	CV72 = "cv72"
	CV73 = "cv73"
	CV74 = "cv74"
	CV75 = "cv75"
	CV76 = "cv76"
	CV77 = "cv77"
	CV78 = "cv78"
	CV79 = "cv79"
	CV80 = "cv80"
	CV81 = "cv81"
	CV82 = "cv82"
	CV83 = "cv83"
	CV84 = "cv84"
	CV85 = "cv85"
	CV86 = "cv86"
	CV87 = "cv87"
	CV88 = "cv88"
	CV89 = "cv89"
	CV90 = "cv90"
	CV91 = "cv91"
	CV92 = "cv92"
	CV93 = "cv93"
	CV94 = "cv94"
	CV95 = "cv95"
	CV96 = "cv96"
	CV97 = "cv97"
	CV98 = "cv98"
	CV99 = "cv99"


class CharacterVariant:
	"""~description-characterVariants~"""

	def __init__(self, identifier: CharacterVariantId, value: bool) -> None:
		self.id = identifier
		self.value = value


class FontFeatureId(Enum):
	AALT = "aalt"
	ABVF = "abvf"
	ABVM = "abvm"
	ABVS = "abvs"
	AFRC = "afrc"
	AKHN = "akhn"
	APKN = "apkn"
	BLWF = "blwf"
	BLWM = "blwm"
	BLWS = "blws"
	CALT = "calt"
	CASE = "case"
	CCMP = "ccmp"
	CFAR = "cfar"
	CHWS = "chws"
	CJCT = "cjct"
	CLIG = "clig"
	CPCT = "cpct"
	CPSP = "cpsp"
	CSWH = "cswh"
	CURS = "curs"
	C2PC = "c2pc"
	C2SC = "c2sc"
	DIST = "dist"
	DLIG = "dlig"
	DNOM = "dnom"
	DTLS = "dtls"
	EXPT = "expt"
	FALT = "falt"
	FIN2 = "fin2"
	FIN3 = "fin3"
	FINA = "fina"
	FLAC = "flac"
	FRAC = "frac"
	FWID = "fwid"
	HALF = "half"
	HALN = "haln"
	HALT = "halt"
	HIST = "hist"
	HKNA = "hkna"
	HLIG = "hlig"
	HNGL = "hngl"
	HOJO = "hojo"
	HWID = "hwid"
	INIT = "init"
	ISOL = "isol"
	ITAL = "ital"
	JALT = "jalt"
	JP78 = "jp78"
	JP83 = "jp83"
	JP90 = "jp90"
	JP04 = "jp04"
	KERN = "kern"
	LFBD = "lfbd"
	LIGA = "liga"
	LJMO = "ljmo"
	LNUM = "lnum"
	LOCL = "locl"
	LTRA = "ltra"
	LTRM = "ltrm"
	MARK = "mark"
	MED2 = "med2"
	MEDI = "medi"
	MGRK = "mgrk"
	MKMK = "mkmk"
	MSET = "mset"
	NALT = "nalt"
	NLCK = "nlck"
	NUKT = "nukt"
	NUMR = "numr"
	ONUM = "onum"
	OPBD = "opbd"
	ORDN = "ordn"
	ORNM = "ornm"
	PALT = "palt"
	PCAP = "pcap"
	PKNA = "pkna"
	PNUM = "pnum"
	PREF = "pref"
	PRES = "pres"
	PSTF = "pstf"
	PSTS = "psts"
	PWID = "pwid"
	QWID = "qwid"
	RAND = "rand"
	RCLT = "rclt"
	RKRF = "rkrf"
	RLIG = "rlig"
	RPHF = "rphf"
	RTBD = "rtbd"
	RTLA = "rtla"
	RTLM = "rtlm"
	RUBY = "ruby"
	RVRN = "rvrn"
	SALT = "salt"
	SINF = "sinf"
	SIZE = "size"
	SMCP = "smcp"
	SMPL = "smpl"
	SSTY = "ssty"
	STCH = "stch"
	SUBS = "subs"
	SUPS = "sups"
	SWSH = "swsh"
	TITL = "titl"
	TJMO = "tjmo"
	TNAM = "tnam"
	TNUM = "tnum"
	TRAD = "trad"
	TWID = "twid"
	UNIC = "unic"
	VALT = "valt"
	VAPK = "vapk"
	VATU = "vatu"
	VCHW = "vchw"
	VERT = "vert"
	VHAL = "vhal"
	VJMO = "vjmo"
	VKNA = "vkna"
	VKRN = "vkrn"
	VPAL = "vpal"
	VRT2 = "vrt2"
	VRTR = "vrtr"
	ZERO = "zero"


class FontFeature:
	"""~description-fontFeature~"""

	def __init__(self, identifier: FontFeatureId, value: int) -> None:
		self.identifier = identifier
		self.value = max(value, 0)


class FontFeatureSettings:
	"""~description~"""

	def __init__(
		self,
		font_features: list[FontFeature] = None,
		stylistic_sets: list[StylisticSet] = None,
		character_variants: list[CharacterVariant] = None,
	) -> None:
		self.font_features = font_features
		self.stylistic_sets = stylistic_sets
		self.character_variants = character_variants


class FontStyle(Enum):
	"""~description~"""

	NORMAL = "normal"
	ITALIC = "italic"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class FontVariantCaps(Enum):
	"""~description~"""

	NORMAL = "normal"
	SMALL_CAPS = "small-caps"
	ALL_SMALL_CAPS = "all-small-caps"
	PETITE_CAPS = "petite-caps"
	ALL_PETITE_CAPS = "all-petite-caps"
	UNICASE = "unicase"
	TITLING_CAPS = "titling-caps"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class FontVariantEastAsian(Enum):
	"""~description~"""

	NORMAL = "normal"
	JIS78 = "jis78"
	JIS83 = "jis83"
	JIS90 = "jis90"
	JIS04 = "jis04"
	SIMPLIFIED = "simplified"
	TRADITIONAL = "traditional"
	FULL_WIDTH = "full-width"
	PROPORTIONAL_WIDTH = "proportional-width"
	RUBY = "ruby"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class FontVariantLigatures(Enum):
	"""~description~"""

	NORMAL = "normal"
	NONE = "none"
	COMMON_LIGATURES = "common-ligatures"
	NO_COMMON_LIGATURES = "no-common-ligatures"
	DISCRETIONARY_LIGATURES = "discretionary-ligatures"
	NO_DISCRETIONARY_LIGATURES = "no-discretionary-ligatures"
	HISTORICAL_LIGATURES = "historical-ligatures"
	NO_HISTORICAL_LIGATURES = "no-historical-ligatures"
	CONTEXTUAL = "contextual"
	NO_CONTEXTUAL = "no-contextual"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class FontVariantNumeric(Enum):
	"""~description~"""

	NORMAL = "normal"
	ORDINAL = "ordinal"
	SLASHED_ZERO = "slashed-zero"
	LINING_NUMS = "lining-nums"
	OLDSTYLE_NUMS = "oldstyle-nums"
	PROPORTIONAL_NUMS = "proportional-nums"
	TABULAR_NUM = "tabular-num"
	DIAGONAL_FRACTIONS = "diagonal-fractions"
	STACKED_FRACTIONS = "stacked-fractions"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class FontVariationSettings:
	"""~description~"""

	def __init__(
		self,
		weight: int = None,
		width: float = None,
		slant: float = None,
		italic: bool = None,
		optical_sizing: float = None,
	) -> None:
		self.weight = weight
		self.width = width
		self.slant = slant
		self.italic = italic
		self.optical_sizing = optical_sizing


class TextAlign(Enum):
	"""~description~"""

	START = "start"
	END = "end"
	LEFT = "left"
	RIGHT = "right"
	CENTER = "center"
	JUSTIFY = "justify"
	MATCH_PARENT = "match-parent"
	JUSTIFY_ALL = "justify-all"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class TextDecorationLine(Enum):
	"""~description~"""

	NONE = "none"
	UNDERLINE = "underline"
	OVERLINE = "overline"
	LINE_THROUGH = "line-through"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class TextDecorationStyle(Enum):
	"""~description~"""

	SOLID = "solid"
	DOUBLE = "double"
	DOTTED = "dotted"
	DASHED = "dashed"
	WAVY = "wavy"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class TextUnderlinePosition(Enum):
	"""~description~"""

	AUTO = "auto"
	UNDER = "under"
	LEFT = "left"
	RIGHT = "right"

	@classmethod
	def includes(cls, value: str) -> bool:
		for member in cls:
			if member == value:
				return True

		return False


class VariantContainer:
	def __init__(
		self,
		default: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v1: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v2: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v3: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v4: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v5: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v6: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v7: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v8: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
		v9: Color
		| CubicBezier
		| Dimension
		| Duration
		| FontFamily
		| FontWeight
		| Typography
		| Transition
		| StrokeStyle
		| Shadow
		| Gradient
		| Border
		| FontFeatureSettings
		| FontStyle
		| FontVariantCaps
		| FontVariantEastAsian
		| FontVariantLigatures
		| FontVariantNumeric
		| FontVariationSettings
		| TextAlign
		| TextDecorationLine
		| TextDecorationStyle
		| TextUnderlinePosition = None,
	) -> None:
		self.default = default
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.v4 = v4
		self.v5 = v5
		self.v6 = v6
		self.v7 = v7
		self.v8 = v8
		self.v9 = v9


class StateContainer:
	#: the state when the cursor hovers over the element
	hover: VariantContainer = VariantContainer()
	#: the state when the element is in focus
	focus: VariantContainer = VariantContainer()
	#: the state when the element is active, regarding plain text: it means it's selected
	active: VariantContainer = VariantContainer()
	#: the state when the element is inactive, but more distinct than normal
	inactive: VariantContainer = VariantContainer()
	#: the normal state of the element
	normal: VariantContainer = VariantContainer()
	#: the state when the element is loading
	load: VariantContainer = VariantContainer()
	#: the state when the element is being blocked or can not proceed
	block: VariantContainer = VariantContainer()
	#: the state when the element was successful in doing something
	success: VariantContainer = VariantContainer()
	#: the state when something is wrong with the element
	error: VariantContainer = VariantContainer()
	#: the state when the element wants to warn about something
	warn: VariantContainer = VariantContainer()
	#: the state when the element holds additional information
	info: VariantContainer = VariantContainer()
	#: the state when the element is was newly added
	new: VariantContainer = VariantContainer()
	#: the state when the element has been visited, or was dealt with in the past
	visit: VariantContainer = VariantContainer()
	#: the state when the elements needs immediate attention and want to alert about something, more distinct than warn
	alert: VariantContainer = VariantContainer()
	#: the state when the element is being clicked
	click: VariantContainer = VariantContainer()
	#: the state when the element is being dragged
	drag: VariantContainer = VariantContainer()
	#: volatile, looses it's highlight after a short while, if unattended.
	highlight: VariantContainer = VariantContainer()


class LayoutElementContainer:
	#: a icon element
	icon: StateContainer = StateContainer()
	#: a box element, which is used the most. Think of the HTML `div` element
	box: StateContainer = StateContainer()
	#: a side element, think of a sidebar, HTML `aside`, Androids `Drawer`. A vertical element to the left or right of the main content
	side: StateContainer = StateContainer()
	#: an image element
	image: StateContainer = StateContainer()
	#: a popover/popup element
	popover: StateContainer = StateContainer()
	#: the list element, containing list items
	lists: StateContainer = StateContainer()
	#: a indicator element, can be something like a dot besides text, a colored border,...
	indicator: StateContainer = StateContainer()
	#: a panel element. more distinct than the box element
	panel: StateContainer = StateContainer()
	#: a row element
	row: StateContainer = StateContainer()
	#: the column element
	column: StateContainer = StateContainer()
	#: the cell in a table. less distinct than the box element
	cell: StateContainer = StateContainer()
	#: the window of an application
	window: StateContainer = StateContainer()


class TextElementContainer:
	#: a button element
	button: StateContainer = StateContainer()
	#: a badge element
	badge: StateContainer = StateContainer()
	#: a link element
	link: StateContainer = StateContainer()
	#: a label element
	label: StateContainer = StateContainer()
	#: a header text element
	header: StateContainer = StateContainer()
	#: a body text element, which is used the most. Think of HTML paragraph `p`
	paragraph: StateContainer = StateContainer()
	#: a small text element
	small: StateContainer = StateContainer()
	#: a code-text/preformatted-text element
	code: StateContainer = StateContainer()
	#: a 'select one from many' element. Different from 'tab', which when pressed changes the content of the much of screen space
	select: StateContainer = StateContainer()
	#: a text input element
	inputs: StateContainer = StateContainer()
	#: a legend element
	legend: StateContainer = StateContainer()
	#: a quoted text element
	quote: StateContainer = StateContainer()
	#: a notification element
	notification: StateContainer = StateContainer()
	#: element in a set of similar items, ordered horizontally; horizontal version of `entry`
	tab: StateContainer = StateContainer()
	#: element in a set of similar items,  ordered vertically; vertical version of `tab`
	entry: StateContainer = StateContainer()
	#: description for another element
	caption: StateContainer = StateContainer()


class ElementContainer(LayoutElementContainer, TextElementContainer):
	def __init__(self) -> None:
		return None


class TokenColor:
	"""TokenColor
	everything related to color
	…
	"""

	#: the background property for background-colors
	background: ElementContainer = ElementContainer()
	#: the border property
	border: ElementContainer = ElementContainer()
	#: the outline property
	outline: ElementContainer = ElementContainer()
	#: the text property contains the text colors, to be more precise, the coloring/fill of the glyphs
	text: TextElementContainer = TextElementContainer()
	#: the text property contains the text-decoration colors, behaves just like the CSS property
	text_decoration_color: TextElementContainer = TextElementContainer()


class TokenTypo:
	"""TokenTypo
	everything related to typography
	…
	"""

	#: the font family
	font_family: TextElementContainer = TextElementContainer()
	#: set flags to change the appearance of the font
	font_feature_settings: TextElementContainer = TextElementContainer()
	#: the font size
	font_size: TextElementContainer = TextElementContainer()
	#: the font weight
	font_weight: TextElementContainer = TextElementContainer()
	#: the ligature (joining of two characters into one shape) settings
	font_variant_ligatures: TextElementContainer = TextElementContainer()
	#: the caps (alternate glyphs used for small or petite capitals or for titling) settings
	font_variant_caps: TextElementContainer = TextElementContainer()
	#: the numeric (usage of alternate glyphs for numbers, fractions, and ordinal markers) settings
	font_variant_numeric: TextElementContainer = TextElementContainer()
	#: the asian (the use of alternate glyphs for East Asian scripts, like Japanese and Chinese) settings
	font_variant_east_asian: TextElementContainer = TextElementContainer()
	#: font settings for variable fonts
	font_variation_settings: TextElementContainer = TextElementContainer()
	#: whether a font should be styled with a `normal`, `italic`, or `oblique` face from its font-family
	font_style: TextElementContainer = TextElementContainer()
	#: the spacing between letters
	letter_spacing: TextElementContainer = TextElementContainer()
	#: sets the length of space between words and between tags.
	word_spacing: TextElementContainer = TextElementContainer()
	#: the text alignment
	text_align: TextElementContainer = TextElementContainer()
	#: the kind of line that is used on text in an element, such as an underline or overline
	text_decoration_line: TextElementContainer = TextElementContainer()
	#: the kind of style for the textDecorationLine that is used on text in an element
	text_decoration_style: TextElementContainer = TextElementContainer()
	#: sets the stroke thickness of the decoration line
	text_decoration_thickness: TextElementContainer = TextElementContainer()
	#: where the underline is positioned relative to the letters
	text_underline_position: TextElementContainer = TextElementContainer()


class TokenSpace:
	"""TokenSpace
	everything related to spacings, margins, and predefined shapes and dimensions
	…
	"""

	#: even margin all around
	margin: ElementContainer = ElementContainer()
	#: the top margin
	margin_top: ElementContainer = ElementContainer()
	#: the right margin
	margin_right: ElementContainer = ElementContainer()
	#: the bottom margin
	margin_bottom: ElementContainer = ElementContainer()
	#: the left margin
	margin_left: ElementContainer = ElementContainer()
	#: the top and bottom margin
	margin_block: ElementContainer = ElementContainer()
	#: even padding all around
	padding: ElementContainer = ElementContainer()
	#: the top padding
	padding_top: ElementContainer = ElementContainer()
	#: the right padding
	padding_right: ElementContainer = ElementContainer()
	#: the bottom padding
	padding_bottom: ElementContainer = ElementContainer()
	#: the left padding
	padding_left: ElementContainer = ElementContainer()
	#: the border/corner radius of all corners
	border_radius: ElementContainer = ElementContainer()
	#: the top left border/corner radius
	border_top_left_radius: ElementContainer = ElementContainer()
	#: the the top right border/corner radius
	border_top_right_radius: ElementContainer = ElementContainer()
	#: the the bottom right border/corner radius
	border_bottom_right_radius: ElementContainer = ElementContainer()
	#: the bottom left border/corner radius
	border_bottom_left_radius: ElementContainer = ElementContainer()
	#: predefined max widths
	max_width: ElementContainer = ElementContainer()
	#: predefined max heights
	max_height: ElementContainer = ElementContainer()
	#: the thickens of a border
	border_width: ElementContainer = ElementContainer()


class TokenFx:
	"""TokenFx
	everything related to animation/motion and effects, shadows, filters and sound
	…
	"""

	#: the duration a an animation
	animation_duration: ElementContainer = ElementContainer()
	#: the duration of a transition
	transition_duration: ElementContainer = ElementContainer()
	#: animation easing functions
	animation_timing_function: ElementContainer = ElementContainer()
	#: transition easing functions
	transition_timing_function: ElementContainer = ElementContainer()
	#: the delay before the start of an animation
	animation_delay: ElementContainer = ElementContainer()
	#: the delay before the start of a transition
	transition_delay: ElementContainer = ElementContainer()
	#: box shadows
	box_shadow: ElementContainer = ElementContainer()


class Tokens:
	"""Tokens
	Euma Design Tokens for UI elements
	…
	"""

	color: TokenColor = TokenColor()
	typo: TokenTypo = TokenTypo()
	space: TokenSpace = TokenSpace()
	fx: TokenFx = TokenFx()
