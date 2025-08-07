from PyQt5.QtGui import QFontDatabase


class FontManager:
    _loaded_fonts = {}

    @staticmethod
    def load_fonts():
        fonts_to_load = {
            "michroma": ":/fonts/michroma.ttf",
            "lexendGiga": ":/fonts/lexendagiga.ttf"
        }

        for key, path in fonts_to_load.items():
            font_id = QFontDatabase.addApplicationFont(path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    FontManager._loaded_fonts[key] = families[0]
                else:
                    print(f"[FontManager] No families found in {path}")
            else:
                print(f"[FontManager] Failed to load font from {path}")

    @staticmethod
    def get_font(name: str) -> str:
        return FontManager._loaded_fonts.get(name, "")
