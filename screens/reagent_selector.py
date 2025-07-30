from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QGuiApplication
from widgets.heading import HeadingWidget
from widgets.numericInput import ThemedInputField
from widgets.button import ThemedButton

class ReagentSelector(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)  # Optional padding
        self.layout.setSpacing(16)

        self.screen_width = QGuiApplication.primaryScreen().geometry().width()
        self.screen_height = QGuiApplication.primaryScreen().geometry().height()

        # Heading
        heading = HeadingWidget("Reagent Selector", alignment='center', stretchable=True)
        self.layout.addWidget(heading)

        # Options section
        reagentSelector = QWidget()
        reagentSelector.setStyleSheet("background: transparent;")
        reagentSelectorLayout = QHBoxLayout(reagentSelector)
        reagentSelectorLayout.setContentsMargins(0, 0, 0, 0)
        reagentSelectorLayout.setSpacing(8)

        reagentSelectionHeading = HeadingWidget("Enter Reagent", alignment='left', stretchable=False, size='small')
        reagentSelectionHeading.setStyleSheet("color: black;")
        reagentSelectionHeading.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Input row
        reagentValueWrapper = QWidget()
        reagentValueWrapperLayout = QHBoxLayout(reagentValueWrapper)
        reagentValueWrapperLayout.setContentsMargins(0, 0, 0, 0)
        reagentValueWrapperLayout.setSpacing(10)

        reagentNameInput = ThemedInputField(None, "Reagent Name", size='medium', numeric_only=False)
        reagentNameInput.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        reagentNameEntry = ThemedButton("Done", size='medium')
        reagentNameEntry.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        reagentValueWrapperLayout.addWidget(reagentNameInput)
        reagentValueWrapperLayout.addWidget(reagentNameEntry)
        reagentValueWrapperLayout.addStretch(1)

        reagentSelectorLayout.addWidget(reagentSelectionHeading)
        reagentSelectorLayout.addStretch(1)
        reagentSelectorLayout.addWidget(reagentValueWrapper)

        reagentSelector.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        reagentSelector.setMaximumSize(int(self.screen_width * 0.33), int(self.screen_height * 0.45))

        self.layout.addWidget(reagentSelector)
        self.layout.addStretch(1)
