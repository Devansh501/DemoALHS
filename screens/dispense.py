from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import  Qt
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.well_plate_selector import WellPlateSelectorWidget


class DispenseScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        
        screenLayoutWrapper = QVBoxLayout(self)
        
        # Heading
        heading = Heading("Dispense", level=1)
        
        # Main Area
        mainArea = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainArea)
        
        # Left Area - Well Plate Selector Widget
        leftAreaWrapper = QWidget()
        leftAreaLayout = QVBoxLayout(leftAreaWrapper)
        
        # Sample plate data
        sample_plates = [
            {
                "index": 1,
                "type": "Well Plate",
                "make": "PerkinElmer",
                "name": "OptiPlate-96",
                "details": [
                    {"label": "Wells", "value": "96"},
                    {"label": "Volume", "value": "350ul"},
                    {"label": "Rows", "value": "8"},
                    {"label": "Columns", "value": "12"}
                ]
            },
            {
                "index": 2,
                "type": "Well Plate",
                "make": "Corning",
                "name": "Costar 12-Well Plate",
                "details": [
                    {"label": "Wells", "value": "6"},
                    {"label": "Volume", "value": "80ul"},
                    {"label": "Rows", "value": "3"},
                    {"label": "Columns", "value": "2"}
                ]
            }
        ]
        
        # Create well plate selector
        self.wellPlateSelector = WellPlateSelectorWidget(sample_plates)
        self.wellPlateSelector.selectionChanged.connect(self.on_well_selection_changed)
        
        leftAreaLayout.addWidget(self.wellPlateSelector)
        leftAreaLayout.addStretch()
        
        mainAreaWrapperLayout.addWidget(leftAreaWrapper)
        mainAreaWrapperLayout.setAlignment(leftAreaWrapper,Qt.AlignLeft)        
        # Mid Area
        midAreaWrapper = QWidget()
        midAreaWrapperLayout = QVBoxLayout(midAreaWrapper)
        # Add your mid area widgets here
        
        mainAreaWrapperLayout.addWidget(midAreaWrapper)
        
        # Navigation Bottom Area
        bottomWidget = QWidget()
        bottomWidgetLayout = QHBoxLayout(bottomWidget)
        backButton = ThemedButton("Back")
        runButton = ThemedButton("Run")
        bottomWidgetLayout.addWidget(backButton)
        bottomWidgetLayout.addStretch()
        bottomWidgetLayout.addWidget(runButton)
        bottomWidgetLayout.setContentsMargins(20, 20, 20, 20)
        
        screenLayoutWrapper.addWidget(heading)
        screenLayoutWrapper.addWidget(mainArea)
        screenLayoutWrapper.addSpacing(1)
        screenLayoutWrapper.addWidget(bottomWidget)
    
    def on_well_selection_changed(self, selection_data):
        """Handle well selection changes"""
        print("Selection changed:", selection_data)
        # Process the selection data as needed
