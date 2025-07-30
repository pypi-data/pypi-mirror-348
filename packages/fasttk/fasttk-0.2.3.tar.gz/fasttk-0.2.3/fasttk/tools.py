
from tkinter.font import Font
from typing import Any, Literal, TypeAlias

MODIFIERS: TypeAlias = Literal[
    "Control",
    "Mod1",
    "Alt",
    "Mod2",
    "Shift",
    "Mod3",
    "Lock",
    "Mod4",
    "Extended",
    "Mod5",
    "Button1",
    "Meta",
    "Button2",
    "Double",
    "Button3",
    "Triple",
    "Button4",
    "Quadruple",
    "Button5",
]

EVENT_TYPES: TypeAlias = Literal[
    "Activate",
    "Destroy",
    "Map",
    "ButtonPress",
    "Button",
    "Enter",
    "MapRequest",
    "ButtonRelease",
    "Expose",
    "Motion",
    "Circulate",
    "FocusIn",
    "MouseWheel",
    "CirculateRequest",
    "FocusOut",
    "Property",
    "Colormap",
    "Gravity",
    "Reparent",
    "Configure",
    "KeyPress",
    "Key",
    "ResizeRequest",
    "ConfigureRequest",
    "KeyRelease",
    "Unmap",
    "Create",
    "Leave",
    "Visibility",
    "Deactivate"
]

BUTTON: TypeAlias = Literal[0, 1, 2, 3, 4, 5]

# For full list of available key names,
# see: https://www.tcl-lang.org/man/tcl8.6/TkCmd/keysyms.htm
KEYS: TypeAlias = Literal[
    'space', 'exclam', 'quotedbl', 'numbersign', 'dollar', 'percent', 'ampersand', 
    'apostrophe', 'parenleft', 'parenright', 'asterisk', 'plus', 'comma', 'minus',
    'period', 'slash', '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9', 'colon', 'semicolon',
    'less', 'equal', 'greater', 'question', 'at', 'A', 'B',
    'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', 'bracketleft', 'backslash', 'bracketright', 'asciicircum',
    'underscore', 'grave', 'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's',
    't', 'u', 'v', 'w', 'x', 'y', 'z', 
    'braceleft', 'bar', 'braceright', 'asciitilde', 'nobreakspace', 'exclamdown', 'cent',
    'sterling', 'currency', 'yen', 'brokenbar', 'section', 'diaeresis', 'copyright',
    'ordfeminine', 'guillemetleft', 'notsign', 'hyphen', 'registered', 'macron', 'degree',
    'plusminus', 'twosuperior', 'threesuperior', 'acute', 'mu', 'paragraph', 'periodcentered',
    'cedilla', 'onesuperior', 'ordmasculine', 'guillemetright', 'onequarter', 'onehalf', 'threequarters',
    'questiondown', 'Agrave', 'Aacute', 'Acircumflex', 'Atilde', 'Adiaeresis', 'Aring',
    'AE', 'Ccedilla', 'Egrave', 'Eacute', 'Ecircumflex', 'Ediaeresis', 'Igrave',
    'Iacute', 'Icircumflex', 'Idiaeresis', 'ETH', 'Ntilde', 'Ograve', 'Oacute',
    'Ocircumflex', 'Otilde', 'Odiaeresis', 'multiply', 'Oslash', 'Ugrave', 'Uacute',
    'Ucircumflex', 'Udiaeresis', 'Yacute', 'THORN', 'ssharp', 'agrave', 'aacute',
    'acircumflex', 'atilde', 'adiaeresis', 'aring', 'ae', 'ccedilla', 'egrave',
    'eacute', 'ecircumflex', 'ediaeresis', 'igrave', 'iacute', 'icircumflex', 'idiaeresis',
    'eth', 'ntilde', 'ograve', 'oacute', 'ocircumflex', 'otilde', 'odiaeresis',
    'division', 'oslash', 'ugrave', 'uacute', 'ucircumflex', 'udiaeresis', 'yacute',
    'thorn', 'ydiaeresis'
]

class Props:

    _args: tuple[Any, ...]
    _kwargs: dict[str, Any]

    def __init__(self, *args: Any, **kwargs: Any):
        self._args = args
        self._kwargs = kwargs

class Selector:
    
    _select_map: dict[str, list[tuple[str]]]

    def __init__(self, selector: str):
        self._select_map = {}
        self._select_map["*"] = []
        or_select = selector.split()
        for select in or_select:
            if select.startswith("."):
                target = self._select_map.get("*")
                tags = select.removeprefix(".").split(".")
                target.append(tuple(tags))
            else:
                segments = select.split(".")
                target = self._select_map.get(segments[0], None)
                if target is None:
                    target = []
                    self._select_map[segments[0]] = target
                target.append(tuple(segments[1:]))
    
    def check(self, type: str, tags: set[str]) -> bool:
        typed = self._select_map.get(type, [])
        for require in typed:
            if not require: return True
            if all(tag in tags for tag in require):
                return True
        for require in self._select_map.get("*"):
            if all(tag in tags for tag in require):
                return True
        return False

class _EventSpec:
    def __call__(
        self,
        *,
        event: EVENT_TYPES | str,
        button: BUTTON | None = None,
        key: KEYS | str | None = None,
        modifier1: MODIFIERS | None = None,
        modifier2: MODIFIERS | None = None,
        virtual: bool = False
    ) -> str:
        builds = []
        if modifier2: builds.append(modifier2)
        if modifier1: builds.append(modifier1)
        builds.append(event)
        if button is not None: builds.append(str(button))
        if key: builds.append(key)
        inner = '-'.join(builds)
        return f"<<{inner}>>" if virtual else f"<{inner}>"

class _TclFont:
    
    def __call__(self, font: Font) -> str:
        f = font.actual()
        parts = [f['family'], str(f['size'])]

        if f.get('weight', 'normal') == 'bold':
            parts.append('bold')
        if f.get('slant', 'roman') == 'italic':
            parts.append('italic')
        if f.get('underline', 0):
            parts.append('underline')
        if f.get('overstrike', 0):
            parts.append('overstrike')

        return ' '.join(parts)

EventSpec = _EventSpec()
FontDescriptor = _TclFont()
