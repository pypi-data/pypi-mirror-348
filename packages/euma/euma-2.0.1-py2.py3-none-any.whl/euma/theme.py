from enum import Enum

import euma.tokens as tokens
from euma.palette import Color, ColorSpace, Palette


class Root(Enum):
	RED_EXTRA_DARK = Palette.RED_EXTRA_DARK.value
	RED_DARK = Palette.RED_DARK.value
	RED_MEDIUM = Palette.RED_MEDIUM.value
	RED_LIGHT = Palette.RED_LIGHT.value
	RED_EXTRA_LIGHT = Palette.RED_EXTRA_LIGHT.value
	GREEN_EXTRA_DARK = Palette.GREEN_EXTRA_DARK.value
	GREEN_DARK = Palette.GREEN_DARK.value
	GREEN_MEDIUM = Palette.GREEN_MEDIUM.value
	GREEN_LIGHT = Palette.GREEN_LIGHT.value
	GREEN_EXTRA_LIGHT = Palette.GREEN_EXTRA_LIGHT.value
	BLUE_EXTRA_DARK = Palette.BLUE_EXTRA_DARK.value
	BLUE_DARK = Palette.BLUE_DARK.value
	BLUE_MEDIUM = Palette.BLUE_MEDIUM.value
	BLUE_LIGHT = Palette.BLUE_LIGHT.value
	BLUE_EXTRA_LIGHT = Palette.BLUE_EXTRA_LIGHT.value
	CYAN_EXTRA_DARK = Palette.CYAN_EXTRA_DARK.value
	CYAN_DARK = Palette.CYAN_DARK.value
	CYAN_MEDIUM = Palette.CYAN_MEDIUM.value
	CYAN_LIGHT = Palette.CYAN_LIGHT.value
	CYAN_EXTRA_LIGHT = Palette.CYAN_EXTRA_LIGHT.value
	MAGENTA_EXTRA_DARK = Palette.MAGENTA_EXTRA_DARK.value
	MAGENTA_DARK = Palette.MAGENTA_DARK.value
	MAGENTA_MEDIUM = Palette.MAGENTA_MEDIUM.value
	MAGENTA_LIGHT = Palette.MAGENTA_LIGHT.value
	MAGENTA_EXTRA_LIGHT = Palette.MAGENTA_EXTRA_LIGHT.value
	YELLOW_EXTRA_DARK = Palette.YELLOW_EXTRA_DARK.value
	YELLOW_DARK = Palette.YELLOW_DARK.value
	YELLOW_MEDIUM = Palette.YELLOW_MEDIUM.value
	YELLOW_LIGHT = Palette.YELLOW_LIGHT.value
	YELLOW_EXTRA_LIGHT = Palette.YELLOW_EXTRA_LIGHT.value
	PURPLE_EXTRA_DARK = Palette.PURPLE_EXTRA_DARK.value
	PURPLE_DARK = Palette.PURPLE_DARK.value
	PURPLE_MEDIUM = Palette.PURPLE_MEDIUM.value
	PURPLE_LIGHT = Palette.PURPLE_LIGHT.value
	PURPLE_EXTRA_LIGHT = Palette.PURPLE_EXTRA_LIGHT.value
	ORANGE_EXTRA_DARK = Palette.ORANGE_EXTRA_DARK.value
	ORANGE_DARK = Palette.ORANGE_DARK.value
	ORANGE_MEDIUM = Palette.ORANGE_MEDIUM.value
	ORANGE_LIGHT = Palette.ORANGE_LIGHT.value
	ORANGE_EXTRA_LIGHT = Palette.ORANGE_EXTRA_LIGHT.value
	AQUA_EXTRA_DARK = Palette.AQUA_EXTRA_DARK.value
	AQUA_DARK = Palette.AQUA_DARK.value
	AQUA_MEDIUM = Palette.AQUA_MEDIUM.value
	AQUA_LIGHT = Palette.AQUA_LIGHT.value
	AQUA_EXTRA_LIGHT = Palette.AQUA_EXTRA_LIGHT.value
	DARK_1 = Palette.DARK_1.value
	DARK_2 = Palette.DARK_2.value
	DARK_3 = Palette.DARK_3.value
	DARK_4 = Palette.DARK_4.value
	DARK_5 = Palette.DARK_5.value
	DARK_6 = Palette.DARK_6.value
	DARK_7 = Palette.DARK_7.value
	DARK_8 = Palette.DARK_8.value
	DARK_9 = Palette.DARK_9.value
	DARK_10 = Palette.DARK_10.value
	GRAY_NEUTRAL = Palette.GRAY_NEUTRAL.value
	LIGHT_10 = Palette.LIGHT_10.value
	LIGHT_9 = Palette.LIGHT_9.value
	LIGHT_8 = Palette.LIGHT_8.value
	LIGHT_7 = Palette.LIGHT_7.value
	LIGHT_6 = Palette.LIGHT_6.value
	LIGHT_5 = Palette.LIGHT_5.value
	LIGHT_4 = Palette.LIGHT_4.value
	LIGHT_3 = Palette.LIGHT_3.value
	LIGHT_2 = Palette.LIGHT_2.value
	LIGHT_1 = Palette.LIGHT_1.value
	SHADOW_SMALL = tokens.Shadow(
		tokens.Dimension(0.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(2.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(10.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(-8.0, tokens.DimensionalUnit.PX),
		Color(ColorSpace.SRGB, [0.047058823529411764, 0.050980392156862744, 0.06274509803921569], 1.0, "#0c0d10"),
		None,
	)
	SHADOW_MEDIUM = tokens.Shadow(
		tokens.Dimension(0.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(4.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(10.0, tokens.DimensionalUnit.PX),
		tokens.Dimension(-6.0, tokens.DimensionalUnit.PX),
		Color(ColorSpace.SRGB, [0.047058823529411764, 0.050980392156862744, 0.06274509803921569], 1.0, "#0c0d10"),
		None,
	)
	FONT_FAMILY_DISPLAY = tokens.FontFamily(
		["Source Serif 4 Display", "Abril Fatface", "Playfair Display", "Times New Roman", "ui-serif", "serif"]
	)
	FONT_FAMILY_SERIF = tokens.FontFamily(
		[
			"Source Serif Variable",
			"Source Serif 4",
			"IBM Plex Serif",
			"Charis SIL",
			"Georgia",
			"Times New Roman",
			"ui-serif",
			"serif",
		]
	)
	FONT_FAMILY_SANS = tokens.FontFamily(
		[
			"Source Sans Variable",
			"Source Sans 3",
			"IBM Plex Sans",
			"Fira Sans",
			"Rambla",
			"PT Sans",
			"ui-sans-serif",
			"sans-serif",
		]
	)
	FONT_FAMILY_MONO = tokens.FontFamily(
		["Source Code VF", "Source Code Pro", "Fira Code", "Red Hat Mono", "ui-monospace", "monospace"]
	)
	FONT_FEATURE_SETTINGS_DISPLAY = tokens.FontFeatureSettings(
		font_features=None,
		stylistic_sets=[tokens.StylisticSet(identifier=tokens.StylisticSetId.SS02, value=True)],
		character_variants=None,
	)
	FONT_FEATURE_SETTINGS_SERIF = tokens.FontFeatureSettings(
		font_features=None,
		stylistic_sets=[tokens.StylisticSet(identifier=tokens.StylisticSetId.SS02, value=True)],
		character_variants=None,
	)
	FONT_FEATURE_SETTINGS_SANS = tokens.FontFeatureSettings(
		font_features=None,
		stylistic_sets=[tokens.StylisticSet(identifier=tokens.StylisticSetId.SS10, value=True)],
		character_variants=None,
	)
	FONT_FEATURE_SETTINGS_MONO = tokens.FontFeatureSettings(
		font_features=None,
		stylistic_sets=[tokens.StylisticSet(identifier=tokens.StylisticSetId.SS06, value=True)],
		character_variants=None,
	)
	FONT_WEIGHT_DISPLAY = tokens.FontWeight.W600
	FONT_WEIGHT_SERIF = tokens.FontWeight.W600
	FONT_WEIGHT_SANS = tokens.FontWeight.W400
	FONT_WEIGHT_MONO = tokens.FontWeight.W400
	FONT_VARIATION_SETTINGS_DISPLAY = tokens.FontVariationSettings(None, None, None, None, None)
	FONT_VARIATION_SETTINGS_SERIF = tokens.FontVariationSettings(None, None, None, None, 45.0)
	FONT_VARIATION_SETTINGS_SANS = tokens.FontVariationSettings(None, None, None, None, None)
	FONT_VARIATION_SETTINGS_MONO = tokens.FontVariationSettings(None, None, None, None, None)


THEME = tokens.Tokens()
THEME.color.background.header.highlight.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.background.paragraph.highlight.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.background.code.normal.default: tokens.Color = Root.DARK_3
THEME.color.background.side.normal.default: tokens.Color = Root.DARK_5
THEME.color.background.panel.normal.default: tokens.Color = Root.DARK_6
THEME.color.background.button.normal.default: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.background.button.normal.v1: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.background.button.normal.v2: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.background.button.hover.default: tokens.Color = Root.PURPLE_LIGHT
THEME.color.background.button.hover.v1: tokens.Color = Root.PURPLE_LIGHT
THEME.color.background.button.hover.v2: tokens.Color = Root.DARK_4
THEME.color.background.tab.active.default: tokens.Color = Root.DARK_2
THEME.color.background.tab.normal.default: tokens.Color = Root.DARK_4
THEME.color.background.tab.hover.default: tokens.Color = Root.DARK_5
THEME.color.background.link.highlight.default: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.background.window.normal.default: tokens.Color = Root.DARK_4
THEME.color.border.tab.active.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.border.tab.inactive.default: tokens.Color = Root.DARK_4
THEME.color.border.window.active.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.border.window.normal.default: tokens.Color = Root.DARK_4
THEME.color.border.button.normal.default: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.border.button.normal.v1: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.border.button.normal.v2: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.text.caption.normal.default: tokens.Color = Root.LIGHT_6
THEME.color.text.paragraph.normal.default: tokens.Color = Root.LIGHT_4
THEME.color.text.paragraph.highlight.default: tokens.Color = Root.LIGHT_1
THEME.color.text.link.normal.default: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.text.link.hover.default: tokens.Color = Root.PURPLE_LIGHT
THEME.color.text.link.active.default: tokens.Color = Root.PURPLE_EXTRA_LIGHT
THEME.color.text.link.visit.default: tokens.Color = Root.PURPLE_DARK
THEME.color.text.link.highlight.default: tokens.Color = Root.LIGHT_2
THEME.color.text.button.normal.default: tokens.Color = Root.LIGHT_1
THEME.color.text.button.normal.v1: tokens.Color = Root.LIGHT_1
THEME.color.text.button.normal.v2: tokens.Color = Root.PURPLE_MEDIUM
THEME.color.text.button.hover.default: tokens.Color = Root.LIGHT_1
THEME.color.text.button.hover.v1: tokens.Color = Root.LIGHT_1
THEME.color.text.button.hover.v2: tokens.Color = Root.PURPLE_LIGHT
THEME.color.text.tab.hover.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.text.tab.active.default: tokens.Color = Root.ORANGE_MEDIUM
THEME.color.text.tab.normal.default: tokens.Color = Root.LIGHT_4
THEME.color.text.header.normal.default: tokens.Color = Root.LIGHT_4
THEME.color.text.header.highlight.default: tokens.Color = Root.LIGHT_1
THEME.color.text.label.success.default: tokens.Color = Root.GREEN_MEDIUM
THEME.color.text.label.error.default: tokens.Color = Root.RED_MEDIUM
THEME.color.text_decoration_color.link.highlight.default: tokens.Color = Root.LIGHT_1
THEME.color.text_decoration_color.link.visit.default: tokens.Color = Root.PURPLE_EXTRA_DARK
THEME.space.border_width.button.normal.default: tokens.Dimension = tokens.Dimension(2.0, tokens.DimensionalUnit.PX)
THEME.space.max_width.paragraph.normal.default: tokens.Dimension = tokens.Dimension(760.0, tokens.DimensionalUnit.PX)
THEME.space.max_width.lists.normal.default: tokens.Dimension = tokens.Dimension(760.0, tokens.DimensionalUnit.PX)
THEME.space.border_radius.code.normal.default: tokens.Dimension = tokens.Dimension(4.0, tokens.DimensionalUnit.PX)
THEME.space.border_radius.panel.normal.default: tokens.Dimension = tokens.Dimension(1.0, tokens.DimensionalUnit.REM)
THEME.space.padding.code.normal.default: tokens.Dimension = tokens.Dimension(3.0, tokens.DimensionalUnit.PX)
THEME.space.padding.panel.normal.default: tokens.Dimension = tokens.Dimension(1.0, tokens.DimensionalUnit.REM)
THEME.space.padding.header.normal.default: tokens.Dimension = tokens.Dimension(0.0, tokens.DimensionalUnit.PX)
THEME.space.margin_left.entry.normal.default: tokens.Dimension = tokens.Dimension(0.5, tokens.DimensionalUnit.REM)
THEME.space.margin_block.paragraph.normal.default: tokens.Dimension = tokens.Dimension(0.6, tokens.DimensionalUnit.REM)
THEME.space.margin_block.entry.normal.default: tokens.Dimension = tokens.Dimension(0.6, tokens.DimensionalUnit.REM)
THEME.typo.font_family.paragraph.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.link.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.badge.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.button.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.caption.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.entry.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SANS
THEME.typo.font_family.header.normal.default: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.header.normal.v1: tokens.FontFamily = Root.FONT_FAMILY_DISPLAY
THEME.typo.font_family.header.normal.v2: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.header.normal.v3: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.header.normal.v4: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.header.normal.v5: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.header.normal.v6: tokens.FontFamily = Root.FONT_FAMILY_SERIF
THEME.typo.font_family.code.normal.default: tokens.FontFamily = Root.FONT_FAMILY_MONO
THEME.typo.font_weight.header.normal.default: tokens.FontWeight = Root.FONT_WEIGHT_DISPLAY
THEME.typo.font_weight.header.normal.v1: tokens.FontWeight = tokens.FontWeight.W700
THEME.typo.font_weight.header.normal.v2: tokens.FontWeight = 650
THEME.typo.font_weight.header.normal.v3: tokens.FontWeight = 640
THEME.typo.font_weight.header.normal.v4: tokens.FontWeight = 630
THEME.typo.font_weight.header.normal.v5: tokens.FontWeight = 620
THEME.typo.font_weight.header.normal.v6: tokens.FontWeight = 610
THEME.typo.font_weight.paragraph.normal.default: tokens.FontWeight = Root.FONT_WEIGHT_SANS
THEME.typo.font_weight.code.normal.default: tokens.FontWeight = Root.FONT_WEIGHT_SANS
THEME.typo.font_size.small.normal.default: tokens.Dimension = tokens.Dimension(15.11, tokens.DimensionalUnit.PX)
THEME.typo.font_size.small.normal.v1: tokens.Dimension = tokens.Dimension(15.79, tokens.DimensionalUnit.PX)
THEME.typo.font_size.paragraph.normal.default: tokens.Dimension = tokens.Dimension(17.0, tokens.DimensionalUnit.PX)
THEME.typo.font_size.paragraph.normal.v1: tokens.Dimension = tokens.Dimension(21.0, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.default: tokens.Dimension = tokens.Dimension(34.46, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v1: tokens.Dimension = tokens.Dimension(34.46, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v2: tokens.Dimension = tokens.Dimension(30.36, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v3: tokens.Dimension = tokens.Dimension(27.23, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v4: tokens.Dimension = tokens.Dimension(24.23, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v5: tokens.Dimension = tokens.Dimension(21.52, tokens.DimensionalUnit.PX)
THEME.typo.font_size.header.normal.v6: tokens.Dimension = tokens.Dimension(19.13, tokens.DimensionalUnit.PX)
THEME.typo.font_variation_settings.header.normal.default: tokens.FontVariationSettings = (
	Root.FONT_VARIATION_SETTINGS_SERIF
)
THEME.typo.font_variation_settings.header.normal.v2: tokens.FontVariationSettings = Root.FONT_VARIATION_SETTINGS_SERIF
THEME.typo.font_variation_settings.header.normal.v3: tokens.FontVariationSettings = Root.FONT_VARIATION_SETTINGS_SERIF
THEME.typo.font_variation_settings.header.normal.v4: tokens.FontVariationSettings = Root.FONT_VARIATION_SETTINGS_SERIF
THEME.typo.font_variation_settings.header.normal.v5: tokens.FontVariationSettings = Root.FONT_VARIATION_SETTINGS_SERIF
THEME.typo.font_variation_settings.header.normal.v6: tokens.FontVariationSettings = Root.FONT_VARIATION_SETTINGS_SERIF
THEME.typo.font_feature_settings.paragraph.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.link.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.badge.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.button.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.caption.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.entry.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_SANS
THEME.typo.font_feature_settings.header.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_DISPLAY
THEME.typo.font_feature_settings.code.normal.default: tokens.FontFeatureSettings = Root.FONT_FEATURE_SETTINGS_MONO
THEME.typo.word_spacing.paragraph.normal.default: tokens.Dimension = tokens.Dimension(0.08, tokens.DimensionalUnit.REM)
THEME.typo.letter_spacing.paragraph.normal.default: tokens.Dimension = tokens.Dimension(
	0.02, tokens.DimensionalUnit.REM
)
THEME.typo.font_variant_ligatures.paragraph.normal.default: tokens.FontVariantLigatures = (
	tokens.FontVariantLigatures.NO_COMMON_LIGATURES
)
THEME.typo.text_decoration_line.header.hover.default: tokens.TextDecorationLine = tokens.TextDecorationLine.NONE
THEME.typo.text_decoration_line.link.normal.default: tokens.TextDecorationLine = tokens.TextDecorationLine.NONE
THEME.typo.text_decoration_line.link.hover.default: tokens.TextDecorationLine = tokens.TextDecorationLine.UNDERLINE
THEME.typo.text_align.header.normal.default: tokens.TextAlign = tokens.TextAlign.CENTER
THEME.fx.animation_timing_function.icon.normal.default: tokens.CubicBezier = tokens.CubicBezier(
	0.252835273752, 0.89385320758, 0.252835273752, 0.89385320758
)
THEME.fx.box_shadow.panel.normal.default: tokens.Shadow = tokens.Shadow(
	tokens.Dimension(0.0, tokens.DimensionalUnit.PX),
	tokens.Dimension(2.0, tokens.DimensionalUnit.PX),
	tokens.Dimension(10.0, tokens.DimensionalUnit.PX),
	tokens.Dimension(-8.0, tokens.DimensionalUnit.PX),
	Root.DARK_1,
	None,
)
