from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout, QPushButton,QColorDialog, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QColor, QStandardItemModel
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.numericInput import ThemedInputField
from widgets.beaker_widget import BeakerWidget
from widgets.tableqt import MaterialTableWidget
from widgets.newSelector import ThemedSelector
from widgets.menu_button import MenuButton
from widgets.warning_dialog import WarningDialog

class ReagentConfiguration(QWidget):
    def __init__(self,parentObj):
        super().__init__()
        screenWrapperLayout = QVBoxLayout(self)
        
        self.reservoirCapacity = 1
        self.currentReagentSelected = {}
        
        self.reservoirDataAvailable = list(filter(lambda x: x["type"] == "Reservoir", parentObj.labware_screen))
        
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
        
        screenWrapperLayout.addStretch(1)        
        screenWrapperLayout.addLayout(reagentAddWrapper)
        screenWrapperLayout.addStretch(1)
        
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
        self.wellSelector = ThemedSelector()
        self.reservoirSelector = ThemedSelector()
        self.reagentSelector = ThemedSelector(placeholder="Add Reagent")
        self.reagentQuantity = ThemedInputField()
        reservoirOptions = list(map(lambda x: x["name"],self.reservoirDataAvailable))   
        self.reservoirSelector.currentTextChanged.connect(lambda text: self.handleReservoirChange(text))
        self.reservoirSelector.addItems(reservoirOptions)
        self.reagentSelector.setItems(list(map(lambda x: x["reagentName"],self.reagents)))
        self.reagentSelector.currentTextChanged.connect(lambda x: self.handleReagentChange(x))
        self.reagentQuantity.line_edit.textChanged.connect(lambda x: self.handleQuantityInput(x))
        
        addEntryButton = MenuButton("Add",fontSize=16,btnHeight=110,btnWidth=150)
        
        addEntryButton.clicked.connect(self.handleAddEntry)
        

        
        upCenterLayout.addWidget(self.reservoirSelector,1,1)
        upCenterLayout.addWidget(self.wellSelector,1,2)
        upCenterLayout.addWidget(self.reagentSelector,2,1)
        upCenterLayout.addWidget(self.reagentQuantity,2,2)
        centerWrapLayout.addLayout(upCenterLayout)
      
        centerWrapLayout.addWidget(addEntryButton,alignment=Qt.AlignCenter | Qt.AlignTop)
        centerWrapLayout.addStretch(1)
        
        
        mainAreaLayout.addWidget(centerWrap)
        
        # Right Table
        self.rightTable = MaterialTableWidget(theme="light",headers=["Reservoir","Well No.","Name","Quantity"])
        mainAreaLayout.addStretch()
        mainAreaLayout.addWidget(self.rightTable, alignment=Qt.AlignTop)
        
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
            self.reagentName.setValue("")
            self.reagentDescription.setValue("")
            self.reagentSelector.setItems(list(map(lambda x: x["reagentName"],self.reagents)))
    
    def chooseColor(self):
        self.choosenColor = QColorDialog.getColor()
        if self.choosenColor.isValid():
            self.colorBtn.setStyleSheet(f"background-color: {self.choosenColor.name()}; border-radius:4px;")
        else:
            self.choosenColor = QColor("ffffff")

    def get_channels(self,items, name,label):
        obj = next((item for item in items if item["name"] == name), None)
        if not obj:
            return None
        
        channel_detail = next(
            (d["value"] for d in obj["details"] if d["label"] == label),
            None
        )
        return channel_detail
    
    def handleReagentChange(self,text):
        reagentMatched = next ((item for item in self.reagents if text==item["reagentName"]),None)
        if not reagentMatched:
            return None
        self.currentReagentSelected = reagentMatched


    def handleReservoirChange(self,text):
        wells = int(self.get_channels(self.reservoirDataAvailable,text,"Channels"))
        wellsAvlbl = []
        for i in range(wells):
            wellsAvlbl.append(f"Well {i+1}")
        self.wellSelector.setItems(wellsAvlbl)
        self.reservoirCapacity = int(self.get_channels(self.reservoirDataAvailable,text,"Volume")[:-2])
        
    def handleQuantityInput(self,text):
        if (not self.currentReagentSelected 
             or "reagentName" not in self.currentReagentSelected 
             or len(self.currentReagentSelected["reagentName"]) <= 0
            ):
            dialog = WarningDialog("Select Reagent and Reservoir first!!")
            dialog.exec_()
            self.reagentQuantity.line_edit.blockSignals(True)
            self.reagentQuantity.line_edit.setText("0")
            self.reagentQuantity.line_edit.blockSignals(False)
        else:    
            if text=='':
                text='0'
            inpValue = int(float(text))
            allowedValue = int(self.reservoirCapacity)
            self.reagentQuantity.line_edit.blockSignals(True)
            if(allowedValue<inpValue):
                self.reagentQuantity.line_edit.setText(f"{allowedValue}")
            if(inpValue<0):
                self.reagentQuantity.line_edit.setText("0")
            self.reagentQuantity.line_edit.blockSignals(False)
            
            inpValue = int(float(self.reagentQuantity.text()) if len(self.reagentQuantity.text()) > 0 else "0")
            percent = int((inpValue/self.reservoirCapacity)*100)
            self.leftBeaker.setFillColorAndAnimate(self.currentReagentSelected["reagentColor"])
            self.leftBeaker.setFillPercent(percent)
            
        
    def handleAddEntry(self):
        if (not self.currentReagentSelected 
             or "reagentName" not in self.currentReagentSelected 
             or len(self.currentReagentSelected["reagentName"]) <= 0
             or len(self.reservoirSelector.currentText()) <= 0
             or len(self.wellSelector.currentText()) <=0
             or len(self.reagentQuantity.text()) <=0
             or self.reagentQuantity.text() == '0'
            ):
            dialog = WarningDialog("Values not entered!!")
            dialog.exec_()
        else:
            self.rightTable.add_row([self.reservoirSelector.currentText(),self.wellSelector.currentText(),self.currentReagentSelected["reagentName"],self.reagentQuantity.text()]) 
            self.reagentQuantity.line_edit.setText("0")