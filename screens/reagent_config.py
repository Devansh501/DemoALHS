from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout, QPushButton,QColorDialog, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QColor, QStandardItemModel
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.numericInput import ThemedInputField
from widgets.beaker_widget import BeakerWidget
from widgets.tableqt import MaterialTableWidget

class ReagentConfiguration(QWidget):
    def __init__(self,parentObj):
        super().__init__()
        screenWrapperLayout = QVBoxLayout(self)
        
        screenWrapperLayout.addWidget(Heading("Reagent Configuration", level=1))
        
        # Reagent Addition
        reagentAddWrapper = QHBoxLayout()
        
        self.reagents = []
        self.choosenColor = QColor("ffffff")
         
        self.reagentName = ThemedInputField(placeholder_text="Name",size="small",numeric_only=False)
        self.reagentDescription = ThemedInputField(placeholder_text="Description",size="longsmall",numeric_only=False)
        self.addReagentBtn = ThemedButton("Add", size="small")
        self.colorBtn = QPushButton("  ")
        self.colorBtn.setFixedSize(50,28)
        self.colorBtn.setStyleSheet("background: #ffffff; border-radius:4px;")
        self.colorBtn.clicked.connect(self.chooseColor)
        self.addReagentBtn.clicked.connect(self.addReagent)
        
        
        # reagentAddWrapper.addStretch()
        reagentAddWrapper.addWidget(Heading("Add Reagent:", level=9))
        reagentAddWrapper.addWidget(self.reagentName)
        reagentAddWrapper.addWidget(self.reagentDescription)
        reagentAddWrapper.addWidget(self.colorBtn)
        reagentAddWrapper.addStretch()
        reagentAddWrapper.addWidget(self.addReagentBtn)
        reagentAddWrapper.addStretch()
                
        screenWrapperLayout.addLayout(reagentAddWrapper)
        screenWrapperLayout.addStretch()
        
        # Main Area
        mainArea=QWidget()
        mainAreaLayout = QHBoxLayout(mainArea)
        
        # Animated Beaker
        self.leftBeaker = BeakerWidget(
            fill_color=QColor("#FFAA5C"),
            background_color=QColor("#fff"),
            border_color=QColor("#ccc")
        )
        mainAreaLayout.addWidget(self.leftBeaker, alignment=Qt.AlignTop)
        
        # Center Controls
        centerWrap = QWidget()
        centerWrapLayout = QVBoxLayout(centerWrap)
        
        upCenterLayout = QGridLayout()
        
        
        
        # Right Table
        rightTable = MaterialTableWidget(theme="light",headers=["Reservoir","Well No.","Name","Quantity"])
        mainAreaLayout.addStretch()
        mainAreaLayout.addWidget(rightTable, alignment=Qt.AlignTop)
        
        screenWrapperLayout.addWidget(mainArea)
        
        # Navigation Layout
        navLayout = QHBoxLayout()
        backButton = ThemedButton("Back")
        nextButton = ThemedButton("Next")
        navLayout.addWidget(backButton)
        navLayout.addStretch(1)
        navLayout.addWidget(nextButton)
        
        backButton.clicked.connect(lambda: parentObj.router('pipette_selectn'))
        nextButton.clicked.connect(lambda: parentObj.router('calibration'))
    
        screenWrapperLayout.addLayout(navLayout)
        
    def addReagent(self):
        name = self.reagentName.text()
        color = self.choosenColor
        if self.reagentName.text():
            description = self.reagentDescription.text() if self.reagentDescription.text() else ""
            obj = {
                "reagentName":name,
                "reagentDescription":description,
                "reagentColor":color
            }
            self.reagents.append(obj)
            print(f"lol: {self.reagents}")
            self.reagentName.setValue("")
            self.reagentDescription.setValue("")
        # if color.isValid():
        #     
        #     self.leftBeaker.setFillColorAndAnimate(color)
        #     self.leftBeaker.setFillPercent(60)
    
    def chooseColor(self):
        self.choosenColor = QColorDialog.getColor()
        if self.choosenColor.isValid():
            self.colorBtn.setStyleSheet(f"background-color: {self.choosenColor.name()}; border-radius:4px;")
        else:
            self.choosenColor = QColor("ffffff")
        