from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import QTimer
from widgets.button import ThemedButton
from widgets.newSelector import ThemedSelector
from widgets.heading import Heading
from widgets.info_card import InfoCard
from widgets.toast import ToastWidget
from widgets.status_popup import StatusPopup

class PipetteConfigScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        
        self.screen_data = {
            "pipette_type":"Single Channel",
            "pipette_capacity": "50ul"
        }

        screenLayoutWrapper = QVBoxLayout(self)
        
        # Heading
        heading = Heading("Pipette Configuration", level=1)

        # MainArea
        mainAreaWrapper = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainAreaWrapper)

        # left Area
        leftAreaWIdget = QWidget()
        leftAreaWidgetLayout = QVBoxLayout(leftAreaWIdget)
        pipTypeWidget = QWidget()
        pipTypeWidgetLayout = QHBoxLayout(pipTypeWidget)
        pipTypeWidgetLayout.addWidget(Heading("Pipette Type: ", level=5))
        pipTypeSelector = ThemedSelector(size="small")
        pipTypeSelector.addItems(["Single Channel", "Multi Channel"])
        pipTypeSelector.setCurrentIndex(0)
        pipTypeWidgetLayout.addWidget(pipTypeSelector)
        pipTypeSelector.currentTextChanged.connect(lambda text: self.screen_data.update({"pipette_type":text}))

        pipCapacityWidget = QWidget()
        pipCapacityWidgetLayout = QHBoxLayout(pipCapacityWidget)
        pipCapacityWidgetLayout.addWidget(Heading("Pipette Capacity: ", level=5))
        pipCapacitySelector = ThemedSelector(size="small")
        pipCapacitySelector.addItems(["50ul","100ul","200ul"])
        pipCapacityWidgetLayout.addWidget(pipCapacitySelector)
        pipCapacitySelector.currentTextChanged.connect(lambda text: self.screen_data.update({"pipette_capacity":text}))

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
                "Inaccuraccy %: 1.5%",
                "Imprecisions %: 1.0%",
                "Channels: 8"
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
        saveButton.clicked.connect(lambda: self.handleSave(parentObj))
        bottomWidgetLayout.addWidget(saveButton)
        bottomWidgetLayout.addStretch()
        bottomWidgetLayout.addWidget(homeButton)
        bottomWidgetLayout.setContentsMargins(20, 20, 20, 20)



        screenLayoutWrapper.addWidget(heading)
        screenLayoutWrapper.addWidget(mainAreaWrapper)
        screenLayoutWrapper.addWidget(bottomWidget)
    
    def handleSave(self,parentObj):
        # Logic to save pipette configuration
        parentObj.pipette_screen = self.screen_data
        StatusPopup("Saved Selection!", status="success", duration=1500)
        QTimer.singleShot(1800,lambda: parentObj.router("home"))