import sys
from enum import Enum
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QPushButton, QMainWindow
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPen



# --------------------- ColorScheme ENUM ---------------------
class ColorScheme(Enum):
    """Predefined color schemes for the button grid"""
    BLUE = {
        "border": "#222",
        "fill": "#0078d7",
        "column_label_text": "#0078d7",
        "column_label_bg_start": "#f9f9f9",
        "column_label_bg_end": "#e3e3e3",
        "column_label_hover_start": "#ffffff",
        "column_label_hover_end": "#d6d6d6",
        "row_label_text": "#444",
        "container_bg": "#fff",
    }
    
    GREEN = {
        "border": "#1a472a",
        "fill": "#2d9b4d",
        "column_label_text": "#2d9b4d",
        "column_label_bg_start": "#f0f8f3",
        "column_label_bg_end": "#d4e6dd",
        "column_label_hover_start": "#ffffff",
        "column_label_hover_end": "#c0dcd0",
        "row_label_text": "#2d5a3d",
        "container_bg": "#fafbfa",
    }
    
    PURPLE = {
        "border": "#3d1a47",
        "fill": "#7c3aed",
        "column_label_text": "#7c3aed",
        "column_label_bg_start": "#f5f3ff",
        "column_label_bg_end": "#e9d5ff",
        "column_label_hover_start": "#ffffff",
        "column_label_hover_end": "#ddd6fe",
        "row_label_text": "#4c1d95",
        "container_bg": "#fafafa",
    }
    
    DARK = {
        "border": "#e5e7eb",
        "fill": "#ef4444",
        "column_label_text": "#ef4444",
        "column_label_bg_start": "#1f2937",
        "column_label_bg_end": "#111827",
        "column_label_hover_start": "#374151",
        "column_label_hover_end": "#1f2937",
        "row_label_text": "#d1d5db",
        "container_bg": "#0f172a",
    }



# --------------------- DynamicButton ---------------------
class DynamicButton(QWidget):
    def __init__(self, diameter=32, color_scheme=ColorScheme.BLUE, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # No clicks directly
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(diameter, diameter)

        self.checked = False
        self.color_scheme = color_scheme
        self.updateColors()

    def setColorScheme(self, color_scheme):
        self.color_scheme = color_scheme
        self.updateColors()

    def updateColors(self):
        colors = self.color_scheme.value
        self.border_color = QColor(colors["border"])
        self.fill_color = QColor(colors["fill"])

    def setChecked(self, state):
        self.checked = state
        self.update()

    def isChecked(self):
        return self.checked

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()
        radius = min(rect.width(), rect.height()) / 2 - 2

        # Border circle
        pen = QPen(self.border_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(center, radius, radius)

        # Inner filled circle if checked
        if self.checked:
            inner_radius = radius * 0.6
            painter.setBrush(self.fill_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, inner_radius, inner_radius)



# --------------------- ButtonGridWidget ---------------------
LABEL_SIZE = 32
BUTTON_SIZE = 32


class ButtonGridWidgetMulti(QWidget):
    def __init__(self, rows, cols, color_scheme=ColorScheme.BLUE):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.buttons = []
        self.color_scheme = color_scheme

        # Container with shadow for the grid
        container = QWidget()
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(4, 4)
        container.setGraphicsEffect(shadow)
        
        colors = self.color_scheme.value
        container.setStyleSheet(f"""
            QWidget {{
                background: {colors['container_bg']};
                border-radius: 16px;
            }}
        """)

        grid_layout = QGridLayout(container)
        grid_layout.setSpacing(3)
        grid_layout.setContentsMargins(25, 25, 25, 25)

        # Empty top-left cell
        empty_label = QLabel("")
        empty_label.setFixedSize(LABEL_SIZE, LABEL_SIZE)
        grid_layout.addWidget(empty_label, 0, 0)

        # Column labels (clickable)
        for c in range(cols):
            col_label = QLabel(f"{c + 1}")
            col_label.setFont(QFont("Arial", 12))
            col_label.setAlignment(Qt.AlignCenter)
            col_label.setFixedHeight(LABEL_SIZE)
            col_label.setCursor(Qt.PointingHandCursor)
            
            col_label.setStyleSheet(f"""
                QLabel {{
                    color: {colors['column_label_text']};
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 {colors['column_label_bg_start']}, stop:1 {colors['column_label_bg_end']});
                    border-radius: 16px;
                }}
                QLabel:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 {colors['column_label_hover_start']}, stop:1 {colors['column_label_hover_end']});
                }}
            """)
            col_label.mousePressEvent = lambda e, cc=c: self.toggleColumn(cc)
            grid_layout.addWidget(col_label, 0, c + 1)

        # Buttons with row labels
        for r in range(rows):
            row_label = QLabel(chr(65 + r))
            row_label.setFont(QFont("Arial", 12))
            row_label.setAlignment(Qt.AlignCenter)
            row_label.setFixedWidth(LABEL_SIZE)
            row_label.setStyleSheet(f"color: {colors['row_label_text']};")
            grid_layout.addWidget(row_label, r + 1, 0)

            row_buttons = []
            for c in range(cols):
                btn = DynamicButton(diameter=BUTTON_SIZE, color_scheme=self.color_scheme)
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                
                # Enable mouse events and connect to column toggle
                btn.setAttribute(Qt.WA_TransparentForMouseEvents, False)
                btn.setCursor(Qt.PointingHandCursor)
                btn.mousePressEvent = lambda e, col=c: self.toggleColumn(col)
                
                row_buttons.append(btn)
                grid_layout.addWidget(btn, r + 1, c + 1)
            self.buttons.append(row_buttons)

        # Layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(3)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

    def setColorScheme(self, color_scheme):
        """Change the color scheme for all elements"""
        self.color_scheme = color_scheme
        
        # Update button colors
        for row in self.buttons:
            for btn in row:
                btn.setColorScheme(color_scheme)
        
        # Refresh the widget
        self.update()

    def toggleColumn(self, col):
        """Toggle the entire column when any cell or column header is clicked"""
        all_checked = all(self.buttons[r][col].isChecked() for r in range(self.rows))
        for r in range(self.rows):
            self.buttons[r][col].setChecked(not all_checked)

    def getSelectedCells(self):
        """Return list of selected cells as strings (e.g., ['A1', 'B3'])"""
        selected = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.buttons[r][c].isChecked():
                    selected.append(f"{chr(65 + r)}{c + 1}")
        return selected



# --------------------- Demo Application ---------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    window.setWindowTitle("Button Grid with Color Schemes")
    window.setGeometry(100, 100, 600, 500)
    
    # Main widget with layout
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setSpacing(20)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # Create grid with BLUE scheme
    grid_blue = ButtonGridWidgetMulti(rows=5, cols=6, color_scheme=ColorScheme.BLUE)
    main_layout.addWidget(QLabel("Blue Scheme (Click cells or headers to toggle column):"))
    main_layout.addWidget(grid_blue)
    
    # Create grid with GREEN scheme
    grid_green = ButtonGridWidgetMulti(rows=5, cols=6, color_scheme=ColorScheme.GREEN)
    main_layout.addWidget(QLabel("Green Scheme:"))
    main_layout.addWidget(grid_green)
    
    # Create grid with PURPLE scheme
    grid_purple = ButtonGridWidgetMulti(rows=5, cols=6, color_scheme=ColorScheme.PURPLE)
    main_layout.addWidget(QLabel("Purple Scheme:"))
    main_layout.addWidget(grid_purple)
    
    main_widget.setStyleSheet("background: #f5f5f5;")
    window.setCentralWidget(main_widget)
    window.show()
    
    sys.exit(app.exec_())
