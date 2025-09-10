from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.mutli_grid import ButtonGridWidgetMulti
from widgets.awesome_grid import ButtonGridWidget
from widgets.info_card import InfoCard

class PipetteSelection(QWidget):
    def __init__(self,parentObj):
        super().__init__()
        wrapper = QVBoxLayout(self)
        wrapper.addWidget(Heading("Tip Selection",level=1))
        
        # main Area
        pipette_type = parentObj.pipette_screen["pipette_type"]
        
        if pipette_type == 'Single Channel':
            grid = ButtonGridWidget(8,12)
        elif pipette_type == 'Multi Channel':
            grid = ButtonGridWidgetMulti(8,12)
        
        mainArea = QWidget()
        mainAreaLayout = QHBoxLayout(mainArea)
        
        infoArea = InfoCard(
            heading="Tipbox Info.",
            points=[
                "Maximum Pipette Capacity: 200ul",
                "Minimum Pipette Capacity: 5ul",
                "Length: 100cm, Breadth: 125cm, Height:35cm",
                "Pipette Type: Single/Multi Channel"
            ]
        )
        
        mainAreaLayout.addStretch()
        mainAreaLayout.addWidget(grid)
        mainAreaLayout.addStretch()
        mainAreaLayout.addWidget(infoArea)
        mainAreaLayout.addStretch()
        
        wrapper.addWidget(mainArea)
        
        
        # bottom navigation Layout
        navLayout =  QHBoxLayout()
        backButton = ThemedButton("Back")
        nextButton = ThemedButton("Next")
        
        backButton.clicked.connect(lambda: parentObj.router('home'))
        nextButton.clicked.connect(lambda: parentObj.router('reagent_config'))
        
        navLayout.addWidget(backButton)
        navLayout.addStretch(1)
        navLayout.addWidget(nextButton)
        wrapper.addLayout(navLayout)