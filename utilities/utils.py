from PyQt5.QtGui import QColor
from pathlib import Path
import sys
import json

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
    
    @staticmethod
    def load_stylesheet(filename):
        base_path = Path(sys.argv[0]).resolve().parent
        qss_path = base_path / "styles" / filename
        return qss_path.read_text()
    
    @staticmethod
    def load_json(filename):
        
        base_path = Path(sys.argv[0]).resolve().parent
        json_path = base_path / "resources/json" / filename

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[Error] JSON file not found: {json_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"[Error] Failed to decode JSON ({json_path}): {e}")
            return {}

