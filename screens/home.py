from PyQt5.QtWidgets import QWidget,QHBoxLayout,QLabel
from PyQt5.QtGui import QFontDatabase,QFont
from PyQt5.QtCore import QFile
from widgets.button import ThemedButton
from resources import resources


# class HomeScreen(QWidget):
#     def __init__(self, parentObj):
#         super().__init__()
#         font_id = QFontDatabase.addApplicationFont(":/fonts/michroma.ttf") # Use the path within the QRC file

#         if font_id == -1:
#             print("Font failed to load")
#         else:
#             families = QFontDatabase.applicationFontFamilies(font_id)
#             print("Loaded font families:", families)
        
#         f = QFile(":/fonts/michroma.ttf")
#         if f.exists():
#             print("Font file exists in resource system ✅")
#         else:
#             print("Font file does NOT exist in resource system ❌")
        
#         font_id = QFontDatabase.addApplicationFont("../resources/fonts/Michroma-Regular.ttf")
#         print("Font ID (file load):", font_id)


#         self.setWindowTitle("Home")
#         layout = QHBoxLayout()
#         single_pipette_button = ThemedButton("Single Pipette",size="large")
#         multi_pipette_button = ThemedButton("Multi Pipette",size="large")
#         reagent_selector_button = ThemedButton("Reagent Selector",size="large")

#         single_pipette_button.clicked.connect(lambda: parentObj.router("single_pipette_asp"))
#         multi_pipette_button.clicked.connect(lambda: parentObj.router("multi_pipette_asp"))
#         reagent_selector_button.clicked.connect(lambda: parentObj.router("reagent_selector"))
        
        
#         layout.addWidget(single_pipette_button)
#         layout.addWidget(multi_pipette_button)
#         layout.addWidget(reagent_selector_button)
#         self.setLayout(layout)

class HomeScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()

        from PyQt5.QtGui import QFont, QFontDatabase

        font_id = QFontDatabase.addApplicationFont(":/fonts/michroma.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        label = QLabel("Hello with Custom Font!")
        label.setFont(QFont(families[0], 20)) # Apply the font


        self.setWindowTitle("Home")
        layout = QHBoxLayout()

        single_pipette_button = ThemedButton("Single Pipette", size="large")
        multi_pipette_button = ThemedButton("Multi Pipette", size="large")
        reagent_selector_button = ThemedButton("0123456789", size="large")


        single_pipette_button.clicked.connect(lambda: parentObj.router("single_pipette_asp"))
        multi_pipette_button.clicked.connect(lambda: parentObj.router("multi_pipette_asp"))
        reagent_selector_button.clicked.connect(lambda: parentObj.router("reagent_selector"))

        layout.addWidget(single_pipette_button)
        layout.addWidget(multi_pipette_button)
        layout.addWidget(reagent_selector_button)
        layout.addWidget(label)
        self.setLayout(layout)
