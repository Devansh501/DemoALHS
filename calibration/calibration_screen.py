from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QSlider, QLineEdit, QGraphicsDropShadowEffect,
    QSizePolicy, QSpacerItem, QSizePolicy,QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
class ClickableSlider(QSlider):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.type() == QMouseEvent.MouseButtonPress:
                if self.orientation() == Qt.Vertical:
                    pos = event.pos().y()
                    value = self.minimum() + (self.maximum() - self.minimum()) * (self.height() - pos) / self.height()
                else:
                    pos = event.pos().x()
                    value = self.minimum() + (self.maximum() - self.minimum()) * pos / self.width()
                self.setValue(round(value))
        super().mousePressEvent(event)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .styles import Styles
from .triggers import Triggers
from functools import partial
from widgets.button import ThemedButton
import json
import os

class CalibrationScreen(QWidget):
    def __init__(self,parentObj):
        super().__init__()
        self.setWindowTitle("CALIBRATION")
        # self.resize(1200, 600)  # default size
        # self.setMaximumSize(1800, 1000)
        self.setStyleSheet(Styles.BACKGROUND)
        file_path = "calibration/Machine_Code/start_up_values.json"
        if os.path.exists(file_path):

            with open(file_path, "r") as f:
                data = json.load(f)
        self.XCoOrdinate=float(data["OFFSETS_X"])
        self.YCoOrdinate=float(data["OFFSETS_Y"])
        self.ZCoOrdinate=float(data["OFFSETS_Z"])
        self.stepSize = float(.1)
        self.init_ui(parentObj)


    def init_ui(self,parentObj):
        # Title at top
        title = QLabel("Calibration")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(Styles.TITLE)

        # X Y Z row — bigger fields
        x_label = QLabel("X:")
        x_label.setStyleSheet(Styles.COORD)
        x_edit = QLineEdit("0")
        x_edit.setFixedWidth(80)
        x_edit.setStyleSheet(Styles.INPUT + "font-size: 18px; background: transparent;")

        y_label = QLabel("Y:")
        y_label.setStyleSheet(Styles.COORD)
        y_edit = QLineEdit("0")
        y_edit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)
        y_edit.setFixedWidth(80)
        y_edit.setStyleSheet(Styles.INPUT + "font-size: 18px; background: transparent;")

        z_label = QLabel("Z:")
        z_label.setStyleSheet(Styles.COORD)
        z_edit = QLineEdit("0")
        z_edit.setFixedWidth(80)
        z_edit.setStyleSheet(Styles.INPUT + "font-size: 18px; background: transparent;")
        x_edit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)
        y_edit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)
        z_edit.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred)

        x_pair = self.group_widgets(x_label,x_edit)
        y_pair = self.group_widgets(y_label,y_edit)
        z_pair = self.group_widgets(z_label,z_edit)


        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addStretch(1)
        top_row.addWidget(x_pair)
        top_row.addStretch(1)

        top_row.addWidget(y_pair)
        top_row.addStretch(1)
        top_row.addWidget(z_pair)
        top_row.addStretch(1)
        top_row.addStretch()
        
        # Left: Arrow controls
        arrows_layout = QGridLayout()
        btn_up = self.make_button("^", 80, 100)
        btn_down = self.make_button("v", 80, 100)
        btn_left = self.make_button("<", 100, 80)
        btn_right = self.make_button(">", 100, 80)

        # btn_up.clicked.connect(lambda: self.increaseVal("XCoOrdinate",x_edit))
        
        

        btn_up.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            outline:none;
            border-top-left-radius:12px;
            border-top-right-radius:12px;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
        
    """)
        
        btn_down.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            outline:none;
            border-bottom-left-radius:12px;
            border-bottom-right-radius:12px;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
        
    """)
        
        btn_left.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            outline:none;
            border-top-left-radius:12px;
            border-bottom-left-radius:12px;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
       
    """)
        
        btn_right.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            outline:none;
            border-top-right-radius:12px;
            border-bottom-right-radius:12px;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
       
    """)

        arrows_layout.addWidget(btn_up, 0, 1)
        arrows_layout.addWidget(btn_left, 1, 0)
        arrows_layout.addWidget(btn_right, 1, 2)
        arrows_layout.addWidget(btn_down, 2, 1)

        arrows_widget = QWidget()
        arrows_widget.setStyleSheet("background:transparent;")
        arrows_widget.setLayout(arrows_layout)

        # Center: 6 circular buttons
        center_grid = QGridLayout()
        buttons = ["HOME", "START", "OK", "DLD", "STRE", "STE","btn1","btn2"]
        for i, name in enumerate(buttons):
            btn = self.make_button(name, 60, 60, rounded=True)
            btn.clicked.connect(partial(Triggers.functionality_buttons, name,self))
            center_grid.addWidget(btn, i%2, i//2, alignment=Qt.AlignCenter)
        center_grid.setSpacing(15)
        center_widget = QWidget()
        center_widget.setStyleSheet("background:transparent;")
        center_widget.setLayout(center_grid)

        # Right: Slider & Z controls
        right_container = QHBoxLayout()

        # Slider
        slider_layout = QHBoxLayout()
        

        # Values to map to
        self.mapping = [0.1, 1, 10, 100]
        slider = ClickableSlider(Qt.Vertical)
        slider.setMinimum(0)
        slider.setMaximum(len(self.mapping) - 1)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setStyleSheet(Styles.SLIDER)
        slider.valueChanged.connect(self.update_label)
        slider.setFixedHeight(200)

        labels_layout = QVBoxLayout()
        labels_layout.setSpacing(0)
        for val in reversed(self.mapping):  # top to bottom
            lbl = QLabel(str(val))
            lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lbl.setFixedHeight(int(slider.height() / len(self.mapping)))
            labels_layout.addWidget(lbl)


        slider_layout.addSpacing(10)
        slider_layout.addLayout(labels_layout)
        slider_layout.addWidget(slider, alignment=Qt.AlignCenter)

        # Z controls
        z_buttons_layout = QVBoxLayout()
        z_up = self.make_button("^", 80, 100)
        z_down = self.make_button("v", 80, 100)

        z_up.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            outline:none;
            border-top-left-radius:12px;
            border-top-right-radius:12px;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
        
    """)
        
        z_down.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            font-size: 20px;
            font-weight:bold;
            border: none;
            padding: 2rem;
            border-bottom-left-radius:12px;
            border-bottom-right-radius:12px;
            outline:none;         
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
    """)
        
        # Button connectors
        btn_up.clicked.connect(lambda:Triggers.btn_y_up(self,y_edit))
        btn_down.clicked.connect(lambda:Triggers.btn_y_down(self,y_edit))
        btn_left.clicked.connect(lambda:Triggers.btn_x_left(self,x_edit))
        btn_right.clicked.connect(lambda: Triggers.btn_x_right(self,x_edit))
        z_down.clicked.connect(lambda:Triggers.btn_z_down(self,z_edit))
        z_up.clicked.connect(lambda:Triggers.btn_z_up(self,z_edit))
        
        # Edit Connectors
        x_edit.textEdited.connect(lambda text: Triggers.x_label_edit(self,text,x_edit))
        y_edit.textEdited.connect(lambda text: Triggers.y_label_edit(self,text,y_edit))
        z_edit.textEdited.connect(lambda text: Triggers.z_label_edit(self,text,z_edit))

        # z_buttons_layout.addStretch()
        z_buttons_layout.addWidget(z_up, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        z_buttons_layout.addItem(spacer)
        z_buttons_layout.addWidget(z_down, alignment=Qt.AlignCenter)
        # z_buttons_layout.addStretch()
        
        right_container.addLayout(slider_layout)
        right_container.addSpacing(20)
        right_container.addLayout(z_buttons_layout)

        right_widget = QWidget()
        right_widget.setStyleSheet("background:transparent;")
        right_widget.setLayout(right_container)

        # Body layout: Left | Center | Right
        body_layout = QHBoxLayout()
        body_layout.setSpacing(50)  # spacing between groups
        body_layout.setContentsMargins(40, 0, 40, 0)

        for widget in [arrows_widget, center_widget, right_widget]:
            widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        body_layout.addWidget(arrows_widget, alignment=Qt.AlignCenter)
        body_layout.addWidget(center_widget, alignment=Qt.AlignCenter)
        body_layout.addWidget(right_widget, alignment=Qt.AlignCenter)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)  # padding on all sides

        # Heading at top
        main_layout.addWidget(title, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # gap between heading and XYZ row
        main_layout.addSpacing(10)

        # XYZ row below heading
        top_row_widget = QWidget()
        top_row_widget.setStyleSheet("background:transparent;")
        top_row_widget.setLayout(top_row)
        main_layout.addWidget(top_row_widget, alignment=Qt.AlignTop)

        # stretch between XYZ and body → pushes body to bottom
        
        # body pinned at bottom
        main_layout.addLayout(body_layout)

        # extra padding below body
        main_layout.addSpacing(20)
        
        navLayout = QHBoxLayout()
        backButton = ThemedButton("Back")
        homeButton = ThemedButton("Home")
        
        navLayout.addWidget(backButton)
        navLayout.addStretch()
        navLayout.addWidget(homeButton)
        
        if hasattr(parentObj,"labware_screen"):
            backButton.clicked.connect(lambda: parentObj.router("reagent_config"))
        else:
            backButton.clicked.connect(lambda: parentObj.router("home"))
            
        homeButton.clicked.connect(lambda: parentObj.router("home"))
        
        main_layout.addLayout(navLayout)
        
        self.setLayout(main_layout)
    

    def update_label(self, index):
         self.stepSize = self.mapping[index]

    def make_button(self, text, w, h, rounded=False):
        btn = QPushButton(text)
        btn.setMinimumSize(w, h)
        btn.setMaximumSize(int(w*1.5), int(h*1.5))
        btn.setStyleSheet(
            Styles.BUTTON_ROUNDED if rounded else Styles.BUTTON
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 80))
        btn.setGraphicsEffect(shadow)

        return btn
    
    def group_widgets(self, label, edit):
        container = QWidget()
        layout = QHBoxLayout()
        
        layout.addWidget(label)
        layout.addWidget(edit)

        container.setLayout(layout)
        container.setStyleSheet("border: 1px solid #ccc;border-radius:8px;background: white;")
        return container



    
    def increaseVal(self,ordinate,edit):
        if (getattr(self, ordinate)+self.stepSize<=400):
            setattr(self,ordinate,round(getattr(self, ordinate) + self.stepSize,2))
            edit.setText(str(getattr(self,ordinate)))
    def decreaseVal(self,ordinate):
        if (getattr(self, ordinate)-self.stepSize>=0):
            setattr(self,ordinate,round(getattr(self, ordinate) - self.stepSize,2))
