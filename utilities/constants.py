from utilities.utils import Utils
from PyQt5.QtCore import QSize


# Btn/Selectors/TextBox----
CLICKABLE = {
    "primary":Utils.parse_rgba("rgba(30, 93, 145, 1)"),
    "hover" :Utils.parse_rgba("rgba(37, 123, 191, 1)"),
    "pressed": Utils.parse_rgba("rgba(22, 69, 105, 1)"),
    "disabledBg" : Utils.parse_rgba("rgba(38, 66, 93, 1)"),
    "disabledText" : Utils.parse_rgba("rgba(160, 170, 181, 1)"),
    "text" : Utils.parse_rgba("rgba(255, 255, 255, 1)"),
    "border": Utils.parse_rgba("rgba(44, 119, 184, 1)"),
    "placeholderText": Utils.parse_rgba("rgba(200, 213, 224, 1)"),
    "shadow": Utils.parse_rgba("rgba(0,0,0, 110)"),
    "fontSizeSmall": 12,
    "fontSizeMedium": 14,
    "fontSizeLarge": 16,
    "btnSizeLarge": QSize(160, 48),
    "btnSizeMedium": QSize(120, 36),
    "btnSizeSmall": QSize(90, 28)
}


HEADING = {
    "base":{
    1: {"size": 18, "spacing": 1.4},   # H1 (main heading)
    2: {"size": 16, "spacing": 1.2},   # H2
    3: {"size": 14, "spacing": 1.0},   # H3
    4: {"size": 13, "spacing": 0.9},   # H4
    5: {"size": 12, "spacing": 0.8},   # H5
    6: {"size": 11, "spacing": 0.7},   # H6 (smallest)
    },
    "font_name":"michroma",
    "font_color": "#ffffff"
}

MENU_BUTTON = {
    "length":225,
    "height": 198,
    "font_name": "lexendGiga",
    "bgColor": "#ffffff",
    "color":"#000000"
}