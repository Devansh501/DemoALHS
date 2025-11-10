import sys
from enum import Enum
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QComboBox, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont



# ==================== CONFIGURATION ENUMS ====================


class ColorScheme(Enum):
    """Color scheme for the tabbed container"""
    # Tab header
    TAB_HEADER_BG = "#1a1f2e"
    TAB_HEADER_BORDER = "#2d3748"
    
    # Active tab button
    TAB_ACTIVE_BG = "#1a1f2e"
    TAB_ACTIVE_FG = "#ffffff"
    TAB_ACTIVE_BORDER = "#0ea5e9"
    TAB_ACTIVE_HOVER_BG = "#252d3d"
    
    # Inactive tab button
    TAB_INACTIVE_BG = "#1a1f2e"
    TAB_INACTIVE_FG = "#8b92aa"
    TAB_INACTIVE_BORDER = "#2d3748"
    TAB_INACTIVE_HOVER_BG = "#252d3d"
    TAB_INACTIVE_HOVER_FG = "#a0a8c0"
    
    # Content container
    CONTENT_BG = "#0f1419"
    
    # Container border
    CONTAINER_BORDER = "#ffffff"
    CONTAINER_BG = "#0f1419"
    
    # Widget backgrounds
    INPUT_TAB_BG = "#0f1419"
    TITLE_BG = "#ffffff"
    TITLE_FG = "#1a1f2e"
    TEXT_FG = "#ffffff"
    SECONDARY_TEXT_FG = "#a0a8c0"
    INPUT_BG = "#ffffff"
    INPUT_FG = "#1a1f2e"
    LABEL_FG = "#ffffff"


class SizeConfig(Enum):
    """Size configuration for the tabbed container"""
    TAB_BUTTON_HEIGHT = 50
    TAB_BUTTON_FONT_SIZE = 11
    TAB_BUTTON_PADDING = 20
    TAB_ACTIVE_BORDER_WIDTH = 3
    TAB_INACTIVE_BORDER_WIDTH = 2
    
    CONTAINER_BORDER_RADIUS = 8
    CONTAINER_BORDER_WIDTH = 2
    CONTAINER_PADDING = 2  # Padding to prevent corner cutting
    
    INPUT_HEIGHT = 35
    INPUT_BORDER_RADIUS = 8
    INPUT_PADDING = 8
    
    TITLE_FONT_SIZE = 12
    LABEL_FONT_SIZE = 11
    MAIN_HEADING_SIZE = 18
    
    CONTENT_MARGIN = 20
    CONTENT_SPACING = 20
    MAIN_MARGIN = 30
    MAIN_SPACING = 20


# ==================== TABBED CONTAINER ====================


class TabbedContainer(QFrame):
    """
    A reusable tabbed container widget that allows switching between custom widgets.
    Supports modern styling, dynamic tab switching, and data update notifications.
    
    Features:
    - Configurable colors and sizes via enums
    - Rounded corners with visible borders (no cutting)
    - Data change notifications for active widgets
    - Dynamic tab management
    """
    
    tab_changed = pyqtSignal(int)  # Signal emitted when tab is changed
    active_tab_update_requested = pyqtSignal(int)  # Signal to request update of active tab data
    
    def __init__(self, color_scheme=None, size_config=None, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(0)
        
        # Use provided configs or defaults
        self.color_scheme = color_scheme or ColorScheme
        self.size_config = size_config or SizeConfig
        
        self.tabs = []
        self.tab_buttons = []
        self.content_widgets = []
        self.current_tab_index = 0
        
        self.setup_ui()
        self._apply_border_styling()
        
    def setup_ui(self):
        """Initialize the UI structure with proper padding"""
        # OUTER LAYOUT - for the border and padding
        self.outer_layout = QVBoxLayout(self)
        padding = int(self.size_config.CONTAINER_PADDING.value)
        self.outer_layout.setContentsMargins(padding, padding, padding, padding)
        self.outer_layout.setSpacing(0)
        
        # INNER CONTAINER - holds the actual content
        self.inner_container = QFrame()
        self.inner_container.setFrameShape(QFrame.StyledPanel)
        self.inner_container.setFrameShadow(QFrame.Plain)
        self.inner_container.setLineWidth(0)
        self.inner_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color_scheme.CONTAINER_BG.value};
                border: none;
            }}
        """)
        
        # INNER LAYOUT - for the tab header and content
        self.main_layout = QVBoxLayout(self.inner_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Tab header container
        self.tab_header = QFrame()
        self.tab_header.setFrameShape(QFrame.StyledPanel)
        self.tab_header.setFrameShadow(QFrame.Plain)
        self.tab_header.setLineWidth(0)
        self.tab_header.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color_scheme.TAB_HEADER_BG.value};
                border: none;
            }}
        """)
        self.tab_header_layout = QHBoxLayout(self.tab_header)
        self.tab_header_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_header_layout.setSpacing(0)
        
        # Content container
        self.content_container = QFrame()
        self.content_container.setFrameShape(QFrame.StyledPanel)
        self.content_container.setFrameShadow(QFrame.Plain)
        self.content_container.setLineWidth(0)
        self.content_container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.color_scheme.CONTENT_BG.value};
                border: none;
            }}
        """)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Assemble the layout hierarchy
        self.main_layout.addWidget(self.tab_header)
        self.main_layout.addWidget(self.content_container, 1)
        self.outer_layout.addWidget(self.inner_container)
    
    def _apply_border_styling(self):
        """Apply border and corner radius to the main container only"""
        border_width = int(self.size_config.CONTAINER_BORDER_WIDTH.value)
        border_radius = int(self.size_config.CONTAINER_BORDER_RADIUS.value)
        border_color = self.color_scheme.CONTAINER_BORDER.value
        bg_color = self.color_scheme.CONTAINER_BG.value
        
        # Style the outer TabbedContainer (border and bg)
        self.setStyleSheet(f"""
            TabbedContainer {{
                border: {border_width}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: {bg_color};
            }}
        """)
    
    def add_tab(self, title, widget):
        """
        Add a new tab with the given title and widget.
        
        Args:
            title (str): The tab label
            widget (QWidget): The widget to display for this tab
        """
        # Store widget
        self.content_widgets.append(widget)
        
        # Create tab button
        tab_button = self._create_tab_button(title, len(self.tabs))
        self.tab_buttons.append(tab_button)
        self.tab_header_layout.addWidget(tab_button)
        
        # Store tab info
        self.tabs.append({
            'title': title,
            'widget': widget,
            'button': tab_button
        })
        
        # Add widget to content layout but hide if not first tab
        self.content_layout.addWidget(widget)
        if len(self.tabs) > 1:
            widget.hide()
    
    def _create_tab_button(self, title, index):
        """Create a styled tab button"""
        button = QPushButton(title)
        button.setFont(QFont("Segoe UI", int(self.size_config.TAB_BUTTON_FONT_SIZE.value), QFont.Normal))
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(int(self.size_config.TAB_BUTTON_HEIGHT.value))
        button.clicked.connect(lambda: self.select_tab(index))
        
        # Initial styling
        self._update_tab_style(button, is_active=(index == 0))
        
        return button
    
    def _update_tab_style(self, button, is_active):
        """Update tab button styling based on active state"""
        padding = int(self.size_config.TAB_BUTTON_PADDING.value)
        
        if is_active:
            active_border_width = int(self.size_config.TAB_ACTIVE_BORDER_WIDTH.value)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color_scheme.TAB_ACTIVE_BG.value};
                    color: {self.color_scheme.TAB_ACTIVE_FG.value};
                    border: none;
                    border-bottom: {active_border_width}px solid {self.color_scheme.TAB_ACTIVE_BORDER.value};
                    font-weight: bold;
                    padding: 0px {padding}px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_scheme.TAB_ACTIVE_HOVER_BG.value};
                }}
            """)
        else:
            inactive_border_width = int(self.size_config.TAB_INACTIVE_BORDER_WIDTH.value)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color_scheme.TAB_INACTIVE_BG.value};
                    color: {self.color_scheme.TAB_INACTIVE_FG.value};
                    border: none;
                    border-bottom: {inactive_border_width}px solid {self.color_scheme.TAB_INACTIVE_BORDER.value};
                    font-weight: normal;
                    padding: 0px {padding}px;
                }}
                QPushButton:hover {{
                    background-color: {self.color_scheme.TAB_INACTIVE_HOVER_BG.value};
                    color: {self.color_scheme.TAB_INACTIVE_HOVER_FG.value};
                }}
            """)
    
    def select_tab(self, index):
        """
        Switch to the specified tab.
        
        Args:
            index (int): The index of the tab to switch to
        """
        if index < 0 or index >= len(self.tabs):
            return
        
        # Hide current tab content
        self.content_widgets[self.current_tab_index].hide()
        self._update_tab_style(self.tab_buttons[self.current_tab_index], is_active=False)
        
        # Show new tab content
        self.current_tab_index = index
        self.content_widgets[index].show()
        self._update_tab_style(self.tab_buttons[index], is_active=True)
        
        # Emit signals
        self.tab_changed.emit(index)
        self.active_tab_update_requested.emit(index)
    
    def get_current_tab_index(self):
        """Get the index of the currently active tab"""
        return self.current_tab_index
    
    def get_current_widget(self):
        """Get the currently displayed widget"""
        return self.content_widgets[self.current_tab_index]
    
    def get_tab_widget(self, index):
        """Get a specific tab's widget by index"""
        if 0 <= index < len(self.content_widgets):
            return self.content_widgets[index]
        return None
    
    def remove_tab(self, index):
        """
        Remove a tab by index.
        
        Args:
            index (int): The index of the tab to remove
        """
        if index < 0 or index >= len(self.tabs):
            return
        
        # Remove button from layout
        button = self.tab_buttons.pop(index)
        self.tab_header_layout.removeWidget(button)
        button.deleteLater()
        
        # Remove widget from layout
        widget = self.content_widgets.pop(index)
        self.content_layout.removeWidget(widget)
        widget.deleteLater()
        
        # Remove tab info
        self.tabs.pop(index)
        
        # Update indices and select appropriate tab
        if self.current_tab_index >= len(self.tabs):
            self.current_tab_index = len(self.tabs) - 1
        
        if len(self.tabs) > 0:
            self.select_tab(self.current_tab_index)
    
    def set_tab_title(self, index, title):
        """Update the title of a tab"""
        if 0 <= index < len(self.tabs):
            self.tabs[index]['title'] = title
            self.tab_buttons[index].setText(title)
    
    def notify_active_tab_data_changed(self):
        """
        Notify the active tab that data has changed.
        Call this when external data changes and the active tab needs to update.
        The active tab widget should implement an on_data_changed() method or
        connect to active_tab_update_requested signal.
        """
        if self.current_tab_index >= 0 and self.current_tab_index < len(self.content_widgets):
            widget = self.content_widgets[self.current_tab_index]
            
            # Try to call on_data_changed method if it exists
            if hasattr(widget, 'on_data_changed') and callable(getattr(widget, 'on_data_changed')):
                widget.on_data_changed()



# ==================== EXAMPLE WIDGETS ====================


class InputTab(QWidget):
    """Example custom widget for the Input tab with data update capability"""
    
    def __init__(self, color_scheme=None, size_config=None):
        super().__init__()
        self.color_scheme = color_scheme or ColorScheme
        self.size_config = size_config or SizeConfig
        self.setStyleSheet(f"background-color: {self.color_scheme.INPUT_TAB_BG.value};")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(int(self.size_config.CONTENT_SPACING.value))
        layout.setContentsMargins(int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value))
        
        title = QLabel("Input: Protocol Configuration Pending")
        title.setFont(QFont("Segoe UI", int(self.size_config.TITLE_FONT_SIZE.value), QFont.Bold))
        title.setStyleSheet(f"""
            color: {self.color_scheme.TITLE_FG.value};
            background-color: {self.color_scheme.TITLE_BG.value};
            padding: 10px;
            border-radius: 8px;
        """)
        layout.addWidget(title)
        
        # Reagent Type
        reagent_label = QLabel("Reagent Type")
        reagent_label.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        reagent_label.setStyleSheet(f"color: {self.color_scheme.LABEL_FG.value};")
        layout.addWidget(reagent_label)
        
        self.reagent_combo = QComboBox()
        self.reagent_combo.addItems(["Reagent Type", "Type A", "Type B", "Type C"])
        self.reagent_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {self.color_scheme.INPUT_BG.value};
                color: {self.color_scheme.INPUT_FG.value};
                border: none;
                border-radius: {int(self.size_config.INPUT_BORDER_RADIUS.value)}px;
                padding: {int(self.size_config.INPUT_PADDING.value)}px 12px;
                min-height: {int(self.size_config.INPUT_HEIGHT.value)}px;
            }}
        """)
        layout.addWidget(self.reagent_combo)
        
        # Volume
        volume_label = QLabel("Volume (mL)")
        volume_label.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        volume_label.setStyleSheet(f"color: {self.color_scheme.LABEL_FG.value};")
        layout.addWidget(volume_label)
        
        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Volume (mL)")
        self.volume_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {self.color_scheme.INPUT_BG.value};
                color: {self.color_scheme.INPUT_FG.value};
                border: none;
                border-radius: {int(self.size_config.INPUT_BORDER_RADIUS.value)}px;
                padding: {int(self.size_config.INPUT_PADDING.value)}px 12px;
                min-height: {int(self.size_config.INPUT_HEIGHT.value)}px;
            }}
        """)
        layout.addWidget(self.volume_input)
        
        # Auto-Dispense toggle
        auto_label = QLabel("Auto-Dispense")
        auto_label.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        auto_label.setStyleSheet(f"color: {self.color_scheme.LABEL_FG.value};")
        layout.addWidget(auto_label)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        self.status_label.setStyleSheet(f"color: {self.color_scheme.SECONDARY_TEXT_FG.value};")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def on_data_changed(self):
        """Called when data changes in the parent application"""
        self.status_label.setText("Status: Data Updated")
        print("InputTab: Data has been updated!")
    
    def get_data(self):
        """Get current data from the widget"""
        return {
            'reagent_type': self.reagent_combo.currentText(),
            'volume': self.volume_input.text()
        }


class ProtocolTab(QWidget):
    """Example custom widget for the Protocol tab with data update capability"""
    
    def __init__(self, color_scheme=None, size_config=None):
        super().__init__()
        self.color_scheme = color_scheme or ColorScheme
        self.size_config = size_config or SizeConfig
        self.setStyleSheet(f"background-color: {self.color_scheme.INPUT_TAB_BG.value};")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(int(self.size_config.CONTENT_SPACING.value))
        layout.setContentsMargins(int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value),
                                  int(self.size_config.CONTENT_MARGIN.value))
        
        title = QLabel("Protocol: Configuration Settings")
        title.setFont(QFont("Segoe UI", int(self.size_config.TITLE_FONT_SIZE.value), QFont.Bold))
        title.setStyleSheet(f"color: {self.color_scheme.TEXT_FG.value};")
        layout.addWidget(title)
        
        description = QLabel("Protocol settings and configurations will appear here.")
        description.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        description.setStyleSheet(f"color: {self.color_scheme.SECONDARY_TEXT_FG.value};")
        layout.addWidget(description)
        
        self.update_count_label = QLabel("Updates: 0")
        self.update_count_label.setFont(QFont("Segoe UI", int(self.size_config.LABEL_FONT_SIZE.value)))
        self.update_count_label.setStyleSheet(f"color: {self.color_scheme.SECONDARY_TEXT_FG.value};")
        layout.addWidget(self.update_count_label)
        
        self.update_count = 0
        layout.addStretch()
    
    def on_data_changed(self):
        """Called when data changes in the parent application"""
        self.update_count += 1
        self.update_count_label.setText(f"Updates: {self.update_count}")
        print("ProtocolTab: Data has been updated!")


# ==================== MAIN WINDOW ====================


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Tabbed Container - Fixed Implementation")
        self.setGeometry(100, 100, 900, 600)
        
        # Set dark theme for main window
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {ColorScheme.CONTENT_BG.value};
            }}
        """)
        
        # Create central widget
        central_widget = QWidget()
        central_widget.setStyleSheet(f"background-color: {ColorScheme.CONTENT_BG.value};")
        self.setCentralWidget(central_widget)
        
        # Main layout with padding
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(int(SizeConfig.MAIN_MARGIN.value),
                                       int(SizeConfig.MAIN_MARGIN.value),
                                       int(SizeConfig.MAIN_MARGIN.value),
                                       int(SizeConfig.MAIN_MARGIN.value))
        main_layout.setSpacing(int(SizeConfig.MAIN_SPACING.value))
        
        # Heading
        heading = QLabel("Tabbed Container Widget")
        heading.setFont(QFont("Segoe UI", int(SizeConfig.MAIN_HEADING_SIZE.value), QFont.Bold))
        heading.setStyleSheet(f"color: {ColorScheme.TEXT_FG.value};")
        main_layout.addWidget(heading)
        
        # Subheading with description
        subheading = QLabel("Rounded corners with visible borders - no cutting on edges")
        subheading.setFont(QFont("Segoe UI", int(SizeConfig.LABEL_FONT_SIZE.value)))
        subheading.setStyleSheet(f"color: {ColorScheme.SECONDARY_TEXT_FG.value};")
        main_layout.addWidget(subheading)
        
        # Tabbed container (now using QFrame as base class for proper border rendering)
        self.tabbed = TabbedContainer()
        
        # Add tabs with custom widgets
        self.tabbed.add_tab("Input", InputTab())
        self.tabbed.add_tab("Protocol", ProtocolTab())
        
        # Connect signals
        self.tabbed.tab_changed.connect(self.on_tab_changed)
        self.tabbed.active_tab_update_requested.connect(self.on_active_tab_update_requested)
        
        main_layout.addWidget(self.tabbed, 1)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        update_btn = QPushButton("Update Active Tab Data")
        update_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #0ea5e9;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: #0284c7;
            }}
        """)
        update_btn.clicked.connect(self.on_update_clicked)
        button_layout.addWidget(update_btn)
        
        remove_tab_btn = QPushButton("Remove Tab")
        remove_tab_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: #dc2626;
            }}
        """)
        remove_tab_btn.clicked.connect(self.on_remove_tab)
        button_layout.addWidget(remove_tab_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
    
    def on_tab_changed(self, index):
        """Handle tab change event"""
        print(f"Switched to tab index: {index}")
    
    def on_active_tab_update_requested(self, index):
        """Handle active tab update request"""
        print(f"Active tab update requested for tab: {index}")
    
    def on_update_clicked(self):
        """Update the active tab data"""
        self.tabbed.notify_active_tab_data_changed()
    
    def on_remove_tab(self):
        """Remove the first tab as demonstration"""
        if len(self.tabbed.tabs) > 1:
            self.tabbed.remove_tab(0)
            print("Tab removed!")
        else:
            print("Cannot remove last tab!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())