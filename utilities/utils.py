from PyQt5.QtGui import QColor

class Utils:

    @staticmethod
    def parse_rgba(rgba_str):
        nums = rgba_str[rgba_str.find("(")+1:rgba_str.find(")")].split(",")
        r, g, b = map(int, nums[:3])
        a = float(nums[3]) if len(nums) > 3 else 1.0
        return QColor(r, g, b, int(a * 255))

    @staticmethod
    def color_to_rgba_str(color: QColor) -> str:
        """Convert QColor to a 'rgba(r,g,b,a)' string for QSS."""
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alphaF():.2f})"
