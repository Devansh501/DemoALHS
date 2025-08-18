from PyQt5.QtWidgets import QVBoxLayout, QWidget,QHBoxLayout
from widgets.heading import Heading
from widgets.info_card import InfoCard
from widgets.button import ThemedButton
from widgets.numericInput import ThemedInputField

class LabwareScreen(QWidget):
    def __init__(self,parentObj):
        super().__init__()

        screenLayoutWrapper = QVBoxLayout(self)

        # Heading
        heading = Heading("Labware", level=1)

        # MainArea
        mainAreaWrapper = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainAreaWrapper)

        # left Area
        leftAreaWidget = QWidget()
        leftAreaWidgetLayout = QVBoxLayout(leftAreaWidget)

        upperOptionsWidget = QWidget()
        upperOptionsWidgetLayout = QHBoxLayout(upperOptionsWidget)
        btn = ThemedButton("Options Here!")
        upperOptionsWidgetLayout.addWidget(btn)

        leftAreaWidgetLayout.addWidget(upperOptionsWidget)
        
        labwareInfoCard = InfoCard(
            heading="Labware Info:",
            points=[
                "Maximum Labware Capacity: 200ul",
                "Minimum Pipette Capacity: 5ul",
                "Pipette company: brand name",
                "Pipette company: brand name"
            ],
            width=400,
            height=200
        )
        leftAreaWidgetLayout.addWidget(labwareInfoCard)

        addLabwareBtn = ThemedButton("Add Labware")
        leftAreaWidgetLayout.addWidget(addLabwareBtn)
        
                
        # right Area
        rightAreaWidget = QWidget()
        rightAreaWidgetLayout = QVBoxLayout(rightAreaWidget)

        card = InfoCard(
            heading="Pipette Info:",
            points=[
                "Maximum Pipette Capacity: 200ul",
                "Minimum Pipette Capacity: 5ul",
                "Pipette company: brand name",
                "Pipette company: brand name",
                "Pipette company: brand name",
                "Pipette company: brand name"
            ],
            width=400,
            height=350
        )
        inp = ThemedInputField("test", "0", "medium")
        rightAreaWidgetLayout.addWidget(inp)
        rightAreaWidgetLayout.addWidget(card)
        

        mainAreaWrapperLayout.addWidget(leftAreaWidget)
        mainAreaWrapperLayout.addWidget(rightAreaWidget)
        
        screenLayoutWrapper.addWidget(heading)
        screenLayoutWrapper.addWidget(mainAreaWrapper)