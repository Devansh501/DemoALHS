from enum import Enum
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QRectF, QEvent, QSize, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QLinearGradient, QPainterPath

class GridDimensions(Enum):
    """Grid dimensions - reference size for scaling"""
    REFERENCE_ROWS = 8
    REFERENCE_COLS = 12
    REFERENCE_WELL_SIZE = 32
    WELL_SPACING = 4  # Gap between wells (pixels)

class WellPlateColors(Enum):
    GRID_BACKGROUND = "#FFFFFF"
    GRID_BORDER = "#D0D0D0"
    WELL_UNSELECTED_FILL = "#FFFFFF"
    WELL_UNSELECTED_BORDER = "#333333"
    WELL_SELECTED_FILL = "#4A90E2"
    WELL_SELECTED_BORDER = "#2E5C8A"
    LABEL_TEXT = "#0066CC"

class NavigationColors(Enum):
    BUTTON_BACKGROUND = "transparent"
    BUTTON_TEXT = "#444444"
    BUTTON_BORDER = "#CCCCCC"
    BUTTON_HOVER_BG = "rgba(200, 200, 200, 0.3)"
    BUTTON_PRESSED_BG = "rgba(150, 150, 150, 0.4)"
    BUTTON_DISABLED_TEXT = "#BBBBBB"
    BUTTON_DISABLED_BORDER = "#DDDDDD"
    INDICATOR_TEXT = "#222222"

class ContainerColors(Enum):
    MAIN_BACKGROUND = "transparent"

def extract_rows_cols(details):
    rows, cols = None, None
    for d in details:
        if d['label'].lower() == 'rows':
            rows = int(d['value'])
        elif d['label'].lower() == 'columns':
            cols = int(d['value'])
    return rows, cols

def extract_wells(details):
    for d in details:
        if d['label'].lower() == 'wells':
            return int(d['value'])
    return 96

class WellButton(QWidget):
    clicked = pyqtSignal(int, int)
    
    def __init__(self, row, col, color_scheme=None, size=32):
        super().__init__()
        self.row = row
        self.col = col
        self.selected = False
        self.colors = color_scheme or WellPlateColors
        self.well_size = size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        self.setCursor(Qt.PointingHandCursor)
    
    def toggle(self):
        self.selected = not self.selected
        self.update()
        self.clicked.emit(self.row, self.col)
    
    def set_selected(self, selected):
        self.selected = selected
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        padding = 2
        circle_size = self.well_size - 2 * padding
        if self.selected:
            painter.setBrush(QColor(self.colors.WELL_SELECTED_FILL.value))
            painter.setPen(QPen(QColor(self.colors.WELL_SELECTED_BORDER.value), 2))
        else:
            painter.setBrush(QColor(self.colors.WELL_UNSELECTED_FILL.value))
            painter.setPen(QPen(QColor(self.colors.WELL_UNSELECTED_BORDER.value), 1.5))
        painter.drawEllipse(padding, padding, circle_size, circle_size)
    
    def mousePressEvent(self, event):
        self.toggle()

class WellPlateGridWidget(QWidget):
    selectionChanged = pyqtSignal(list)
    LABEL_SIZE = 32
    GRID_MARGINS = 15

    def __init__(self, rows=8, cols=12, wells=96, color_scheme=None, parent=None,
                 ref_rows=None, ref_cols=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.wells = wells
        self.colors = color_scheme or WellPlateColors
        self.selected_wells = set()
        
        # Store reference dimensions (from the largest grid across all plates)
        self.reference_rows = ref_rows if ref_rows is not None else GridDimensions.REFERENCE_ROWS.value
        self.reference_cols = ref_cols if ref_cols is not None else GridDimensions.REFERENCE_COLS.value
        self.reference_well_size = GridDimensions.REFERENCE_WELL_SIZE.value
        self.reference_spacing = GridDimensions.WELL_SPACING.value
        
        # Calculate well size and spacing based on current grid dimensions
        self.well_size = self._calculate_well_size(rows, cols)
        self.spacing = self._calculate_spacing(rows, cols)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(self.GRID_MARGINS, self.GRID_MARGINS,
                                           self.GRID_MARGINS, self.GRID_MARGINS)
        self.main_layout.setSpacing(0)
        
        self._build_grid()
        self.setLayout(self.main_layout)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.dragging = False
        self.toggled_buttons = set()
        self.touch_start_pos = None
        self.tap_threshold = 10
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(4, 4)
        self.setGraphicsEffect(shadow)
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAttribute(Qt.WA_AcceptTouchEvents, True)
        self.setStyleSheet("background: transparent;")
        
        self._calculate_size_hint()
    
    def _calculate_well_size(self, rows, cols):
        """
        Calculate well size by scaling UP from the reference well size.
        Fewer rows/columns = larger wells.
        More rows/columns = smaller wells.
        
        Uses the reference dimensions to maintain consistent well sizing.
        """
        # Calculate scaling factor based on the density of the current grid
        # compared to the reference grid
        
        # Scaling factor for rows: ref_rows / current_rows
        # Scaling factor for cols: ref_cols / current_cols
        row_scale = self.reference_rows / rows if rows > 0 else 1
        col_scale = self.reference_cols / cols if cols > 0 else 1
        
        # Use the average scaling to get well size
        scale_factor = (row_scale + col_scale) / 2
        
        # Apply scaling to reference well size
        well_size = int(self.reference_well_size * scale_factor)
        
        # Cap maximum to 80 pixels for very small grids
        return min(well_size, 80)
    
    def _calculate_spacing(self, rows, cols):
        """
        Calculate spacing based on grid density.
        Smaller grids get consistent spacing; maintain proportionality.
        """
        base_spacing = self.reference_spacing
        
        # For very small grids (3x4), maintain or slightly increase spacing
        max_dim = max(rows, cols)
        if max_dim <= 4:
            return int(base_spacing * 1.2)
        elif max_dim <= 8:
            return base_spacing
        else:
            return max(int(base_spacing * 0.9), 2)
    
    def _calculate_size_hint(self):
        """Calculate size hint based on current well size and spacing"""
        wells_width = (self.cols * self.well_size + 
                      (self.cols - 1) * self.spacing)
        wells_height = (self.rows * self.well_size + 
                       (self.rows - 1) * self.spacing)
        
        total_width = wells_width + self.LABEL_SIZE + 2 * self.GRID_MARGINS
        total_height = wells_height + self.LABEL_SIZE + 2 * self.GRID_MARGINS
        
        self.fixed_width = total_width + 20
        self.fixed_height = total_height + 20
    
    def sizeHint(self):
        return QSize(self.fixed_width, self.fixed_height)
    
    def minimumSizeHint(self):
        return QSize(self.fixed_width, self.fixed_height)
    
    def _build_grid(self):
        """Build the grid using nested layouts with proper spacing"""
        self.well_buttons = []
        
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Header row with column labels
        header_layout = QHBoxLayout()
        header_layout.setSpacing(self.spacing)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        header_layout.addSpacing(self.LABEL_SIZE)
        
        for col in range(self.cols):
            label = QLabel(str(col + 1))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    font-size: 13px;
                    color: {self.colors.LABEL_TEXT.value};
                    background: transparent;
                }}
            """)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setFixedWidth(self.well_size)
            label.setFixedHeight(self.LABEL_SIZE)
            header_layout.addWidget(label)
        
        header_layout.addStretch()
        
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        self.main_layout.addWidget(header_widget)
        
        # Data rows
        for row in range(self.rows):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(self.spacing)
            row_layout.setContentsMargins(0, 0, 0, 0)
            
            # Row label
            label = QLabel(chr(65 + row))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(f"""
                QLabel {{
                    font-weight: bold;
                    font-size: 13px;
                    color: {self.colors.LABEL_TEXT.value};
                    background: transparent;
                }}
            """)
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setFixedWidth(self.LABEL_SIZE)
            label.setFixedHeight(self.well_size)
            row_layout.addWidget(label)
            
            # Wells
            row_buttons = []
            for col in range(self.cols):
                well_idx = row * self.cols + col
                if well_idx < self.wells:
                    btn = WellButton(row, col, self.colors, self.well_size)
                    btn.clicked.connect(self.on_well_clicked)
                    row_layout.addWidget(btn)
                    row_buttons.append(btn)
            
            row_layout.addStretch()
            self.well_buttons.append(row_buttons)
            
            row_widget = QWidget()
            row_widget.setLayout(row_layout)
            self.main_layout.addWidget(row_widget)
        
        self.main_layout.addStretch()
    
    def paintEvent(self, event):
        """Draw the container background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect().adjusted(5, 5, -5, -5)
        radius = 20
        
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0, QColor("#ffffff"))
        gradient.setColorAt(1, QColor("#ffffff"))
        
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        
        painter.fillPath(path, gradient)
        
        pen = QPen(QColor("#888"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPath(path)
    
    def on_well_clicked(self, row, col):
        """Handle well button click"""
        well_idx = (row, col)
        
        if well_idx in self.selected_wells:
            self.selected_wells.remove(well_idx)
        else:
            self.selected_wells.add(well_idx)
        
        self.selectionChanged.emit(self.get_selected_wells())
    
    def mousePressEvent(self, event):
        self.dragging = True
        self.toggled_buttons.clear()
        self.toggle_well_at(event.pos())
    
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.toggle_well_at(event.pos())
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.toggled_buttons.clear()
    
    def event(self, e):
        if e.type() == QEvent.TouchBegin:
            e.accept()
            self.dragging = False
            self.toggled_buttons.clear()
            self.touch_start_pos = e.touchPoints()[0].pos().toPoint()
            return True
        elif e.type() == QEvent.TouchUpdate:
            e.accept()
            point = e.touchPoints()[0].pos().toPoint()
            dx = abs(point.x() - self.touch_start_pos.x())
            dy = abs(point.y() - self.touch_start_pos.y())
            if max(dx, dy) > self.tap_threshold:
                self.dragging = True
                self.toggle_well_at(point)
            return True
        elif e.type() == QEvent.TouchEnd:
            e.accept()
            end_pos = e.touchPoints()[0].pos().toPoint()
            if not self.dragging:
                self.toggle_well_at(end_pos)
            self.dragging = False
            self.toggled_buttons.clear()
            self.touch_start_pos = None
            return True
        return super().event(e)
    
    def toggle_well_at(self, pos):
        well = self.childAt(pos)
        if isinstance(well, WellButton) and well not in self.toggled_buttons:
            well.toggle()
            self.toggled_buttons.add(well)
    
    def get_selected_wells(self):
        wells = []
        for row, col in sorted(self.selected_wells):
            well_name = f"{chr(65 + row)}{col + 1}"
            wells.append(well_name)
        return wells
    
    def set_selected_wells(self, well_names):
        self.selected_wells.clear()
        for well_name in well_names:
            if len(well_name) >= 2:
                row = ord(well_name[0].upper()) - ord('A')
                try:
                    col = int(well_name[1:]) - 1
                    if 0 <= row < self.rows and 0 <= col < self.cols:
                        self.selected_wells.add((row, col))
                        if row < len(self.well_buttons) and col < len(self.well_buttons[row]):
                            self.well_buttons[row][col].set_selected(True)
                except ValueError:
                    pass
    
    def clear_selection(self):
        for row, col in self.selected_wells:
            if row < len(self.well_buttons) and col < len(self.well_buttons[row]):
                self.well_buttons[row][col].set_selected(False)
        self.selected_wells.clear()
        self.selectionChanged.emit([])
    
    def set_grid(self, rows, cols, wells):
        """Update grid dimensions and recalculate sizing"""
        self.rows = rows
        self.cols = cols
        self.wells = wells
        self.selected_wells.clear()
        
        # Recalculate well size and spacing for new dimensions
        self.well_size = self._calculate_well_size(rows, cols)
        self.spacing = self._calculate_spacing(rows, cols)
        
        # Update size hints
        self._calculate_size_hint()
        
        self._build_grid()

class WellPlateSelectorWidget(QWidget):
    selectionChanged = pyqtSignal(dict)
    
    def __init__(self, plate_objects=None, well_plate_color_scheme=None,
                 nav_color_scheme=None, parent=None):
        super().__init__(parent)
        self.plates_data = plate_objects or []
        self.current_plate_index = 0
        self.selections = {po['name']: [] for po in self.plates_data}
        self.is_switching_plates = False
        
        self.well_plate_colors = well_plate_color_scheme or WellPlateColors
        self.nav_colors = nav_color_scheme or NavigationColors
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(f"background: {ContainerColors.MAIN_BACKGROUND.value};")
        
        # Find maximum rows/columns for all plates
        self.max_rows = GridDimensions.REFERENCE_ROWS.value
        self.max_cols = GridDimensions.REFERENCE_COLS.value
        if self.plates_data:
            for po in self.plates_data:
                rows, cols = extract_rows_cols(po['details'])
                if rows is not None and rows > self.max_rows:
                    self.max_rows = rows
                if cols is not None and cols > self.max_cols:
                    self.max_cols = cols
        
        self.setup_ui()
        if self.plates_data:
            self.show_plate(0)
    
    def set_well_plate_colors(self, color_scheme):
        self.well_plate_colors = color_scheme
        self.plate_widget.colors = color_scheme
        self.plate_widget.update()
    
    def set_navigation_colors(self, color_scheme):
        self.nav_colors = color_scheme
        self._update_navigation_styles()
    
    def _update_navigation_styles(self):
        button_style = f"""
            QPushButton {{
                background: {self.nav_colors.BUTTON_BACKGROUND.value};
                color: {self.nav_colors.BUTTON_TEXT.value};
                border: 2px solid {self.nav_colors.BUTTON_BORDER.value};
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background: {self.nav_colors.BUTTON_HOVER_BG.value};
            }}
            QPushButton:pressed {{
                background: {self.nav_colors.BUTTON_PRESSED_BG.value};
            }}
            QPushButton:disabled {{
                color: {self.nav_colors.BUTTON_DISABLED_TEXT.value};
                border: 2px solid {self.nav_colors.BUTTON_DISABLED_BORDER.value};
            }}
        """
        self.prev_btn.setStyleSheet(button_style)
        self.next_btn.setStyleSheet(button_style)
        
        self.plate_indicator.setStyleSheet(f"""
            QLabel {{
                color: {self.nav_colors.INDICATOR_TEXT.value};
                font-weight: bold;
                font-size: 15px;
                padding: 6px;
            }}
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        nav_container = QWidget()
        nav_container.setStyleSheet("background: transparent;")
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(10)
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(40, 40)
        self.prev_btn.clicked.connect(self.previous_plate)
        
        self.plate_indicator = QLabel()
        self.plate_indicator.setAlignment(Qt.AlignCenter)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(40, 40)
        self.next_btn.clicked.connect(self.next_plate)
        
        self._update_navigation_styles()
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.plate_indicator, 1)
        nav_layout.addWidget(self.next_btn)
        layout.addWidget(nav_container, alignment=Qt.AlignCenter)
        
        if self.plates_data:
            po = self.plates_data[0]
            rows, cols = extract_rows_cols(po['details'])
            wells = extract_wells(po['details'])
            self.plate_widget = WellPlateGridWidget(
                rows, cols, wells,
                color_scheme=self.well_plate_colors,
                ref_rows=self.max_rows,
                ref_cols=self.max_cols
            )
        else:
            self.plate_widget = WellPlateGridWidget(
                8, 12, 96,
                color_scheme=self.well_plate_colors,
                ref_rows=self.max_rows,
                ref_cols=self.max_cols
            )
        
        self.plate_widget.selectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.plate_widget, alignment=Qt.AlignCenter)
        self.setLayout(layout)
    
    def show_plate(self, index):
        if 0 <= index < len(self.plates_data):
            self.is_switching_plates = True
            current_name = self.plates_data[self.current_plate_index]['name']
            self.selections[current_name] = self.plate_widget.get_selected_wells()
            
            self.current_plate_index = index
            po = self.plates_data[index]
            rows, cols = extract_rows_cols(po['details'])
            wells = extract_wells(po['details'])
            self.plate_widget.set_grid(rows, cols, wells)
            self.plate_widget.set_selected_wells(self.selections.get(po['name'], []))
            
            self.plate_indicator.setText(po['name'])
            self.prev_btn.setEnabled(self.current_plate_index > 0)
            self.next_btn.setEnabled(self.current_plate_index < len(self.plates_data) - 1)
            self.is_switching_plates = False
            self.emit_selection_data()
    
    def next_plate(self):
        if self.current_plate_index < len(self.plates_data) - 1:
            self.show_plate(self.current_plate_index + 1)
    
    def previous_plate(self):
        if self.current_plate_index > 0:
            self.show_plate(self.current_plate_index - 1)
    
    def on_selection_changed(self, selected_wells):
        if self.is_switching_plates:
            return
        current_name = self.plates_data[self.current_plate_index]['name']
        self.selections[current_name] = selected_wells
        self.emit_selection_data()
    
    def emit_selection_data(self):
        selection_data = {
            "current_plate": self.plates_data[self.current_plate_index]['name'],
            "selections": []
        }
        for po in self.plates_data:
            wells = self.selections.get(po['name'], [])
            if wells:
                selection_data["selections"].append({
                    "plate_name": po['name'],
                    "plate_index": po['index'],
                    "selected_wells": wells,
                    "count": len(wells)
                })
        self.selectionChanged.emit(selection_data)
    
    def clear_selection(self):
        self.plate_widget.clear_selection()
    
    def clear_all_selections(self):
        for po in self.plates_data:
            self.selections[po['name']] = []
        self.plate_widget.clear_selection()
        self.emit_selection_data()
    
    def get_selection_data(self):
        selection_data = {
            "current_plate": self.plates_data[self.current_plate_index]['name'],
            "selections": []
        }
        for po in self.plates_data:
            wells = self.selections.get(po['name'], [])
            if wells:
                selection_data["selections"].append({
                    "plate_name": po['name'],
                    "plate_index": po['index'],
                    "selected_wells": wells,
                    "count": len(wells)
                })
        return selection_data
    
    def get_selected_wells(self):
        return self.plate_widget.get_selected_wells()
    
    def get_well_count(self):
        return self.plate_widget.wells
