from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from widgets.button import ThemedButton
from widgets.newSelector import ThemedSelector
from widgets.heading import Heading
from widgets.info_card import InfoCard

class PipetteConfigScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()

        screenLayoutWrapper = QVBoxLayout(self)
        
        # Heading
        heading = Heading("Pipette Configuration", font_size=28)

        # MainArea
        mainAreaWrapper = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainAreaWrapper)

        # left Area
        leftAreaWIdget = QWidget()
        leftAreaWidgetLayout = QVBoxLayout(leftAreaWIdget)
        pipTypeWidget = QWidget()
        pipTypeWidgetLayout = QHBoxLayout(pipTypeWidget)
        pipTypeWidgetLayout.addWidget(Heading("Pipette Type: ", font_size=20))
        pipTypeSelector = ThemedSelector()
        pipTypeSelector.addItems(["Single Pipette", "Multi Pipette"])
        pipTypeWidgetLayout.addWidget(pipTypeSelector)

        pipCapacityWidget = QWidget()
        pipCapacityWidgetLayout = QHBoxLayout(pipCapacityWidget)
        pipCapacityWidgetLayout.addWidget(Heading("Pipette Capacity: ", font_size=20))
        pipCapacitySelector = ThemedSelector()
        pipCapacitySelector.addItems(["50ul","100ul","200ul"])
        pipCapacityWidgetLayout.addWidget(pipCapacitySelector)

        leftAreaWidgetLayout.addStretch(3)
        leftAreaWidgetLayout.addWidget(pipTypeWidget)
        leftAreaWidgetLayout.addStretch(1)
        leftAreaWidgetLayout.addWidget(pipCapacityWidget)
        leftAreaWidgetLayout.addStretch(3)


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
        rightAreaWidgetLayout.addWidget(card)
        mainAreaWrapperLayout.addWidget(leftAreaWIdget)
        mainAreaWrapperLayout.addStretch()
        mainAreaWrapperLayout.addWidget(rightAreaWidget)

        bottomWidget = QWidget()
        bottomWidgetLayout = QHBoxLayout(bottomWidget)
        homeButton = ThemedButton("Home")
        saveButton = ThemedButton("Save")

        homeButton.clicked.connect(lambda: parentObj.router("home"))
        saveButton.clicked.connect(lambda: print("Pipette configuration saved!"))
        bottomWidgetLayout.addWidget(saveButton)
        bottomWidgetLayout.addStretch()
        bottomWidgetLayout.addWidget(homeButton)
        bottomWidgetLayout.setContentsMargins(20, 20, 20, 20)



        screenLayoutWrapper.addWidget(heading)
        screenLayoutWrapper.addWidget(mainAreaWrapper)
        screenLayoutWrapper.addWidget(bottomWidget)