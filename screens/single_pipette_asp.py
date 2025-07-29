from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QSpacerItem, QSizePolicy,QGridLayout
from PyQt5.QtGui import QGuiApplication
from widgets.button import ThemedButton
from widgets.heading import HeadingWidget
from widgets.awesome_grid import ButtonGridWidget
from widgets.selector import ThemedSelector
from widgets.numericInput import ThemedInputField

class SinglePipetteAsp(QWidget):
    def __init__(self, parentObj):
        super().__init__()
#         self.setStyleSheet("""
#     QWidget {
#         background: qlineargradient(
#             spread:pad,
#             x1:0, y1:0,
#             x2:1, y2:1,
#             stop:0 #0f2a44,
#             stop:1 #1a4d7a
#         );
#     }
# """)
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 #3c7cb2,    /* Light blue that complements 'primary' */
            stop:1 #6baed6     /* Even lighter tone for smooth transition */
        );
    }
""")


        self.screen_width = QGuiApplication.primaryScreen().geometry().width()
        self.screen_height = QGuiApplication.primaryScreen().geometry().height()

        self.setWindowTitle("Single Pipette Aspiration")
        layout = QVBoxLayout()
        heading = HeadingWidget("Single Pipette Aspiration", alignment='center', stretchable=True)
        
        # Left Area
        playarea = QWidget()
        playarea.setStyleSheet("background: transparent;")
        playareaLayout = QHBoxLayout(playarea)
        playareaLayout.setContentsMargins(25, 0, 25, 0)

        
        SinglePipetteAspGrid = ButtonGridWidget(8,12)
        gridWrapper = QWidget()

        gridWrapper.setMaximumWidth(int(self.screen_width * 0.50))
        gridWrapper.setMaximumHeight(int(self.screen_height * 0.65))
        gridWrapper.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        gridWrapperLayout = QVBoxLayout(gridWrapper) 
        gridWrapperLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        gridWrapperLayout.addWidget(SinglePipetteAspGrid)
        gridWrapperLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Center Area
        aspirationOptionsWrapper = QWidget()
        aspirationOptionsWrapper.setStyleSheet("background: transparent;")
        aspirationOptionsWrapperLayout = QVBoxLayout(aspirationOptionsWrapper)
        input_field = ThemedInputField("Volume (µL)", "e.g. 10.5",size='small')
        input_field.line_edit.editingFinished.connect(lambda: print(f"lol: {input_field.text()} {type(input_field.text())}"))

        aspirationOptionsWrapperLayout.addWidget(input_field)


        # Reagent Selector
        reagentSelector = ThemedSelector(size="medium")
        reagentSelector.addItem("Reagent 1", userData=101)
        reagentSelector.addItem("Reagent 2", userData=202)
        reagentSelector.addItem("Reagent 3", userData=303)
        reagentSelector.currentIndexChanged.connect(lambda: print(reagentSelector.currentData()))

        

        ASpirationData = ThemedButton("Aspiration Data", size="large", primary_color="#1a4d7a", hover_color="#246ca3", pressed_color="#153b60")

        playareaLayout.addWidget(gridWrapper)
        playareaLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        playareaLayout.addWidget(aspirationOptionsWrapper)
        # playareaLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # playareaLayout.addWidget(ASpirationData)

        layout.addWidget(heading,1)
        playareaLayout.addSpacerItem(QSpacerItem(1, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(playarea, 8)


        self.setLayout(layout) 