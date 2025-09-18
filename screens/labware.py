from PyQt5.QtWidgets import QVBoxLayout, QWidget,QHBoxLayout, QGraphicsDropShadowEffect,QLabel,QApplication, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import QTimer
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.newSelector import ThemedSelector
from widgets.toast import ToastWidget
from widgets.scroll_area import ScrollableWidget
from utilities.utils import Utils
from utilities.constants import LABWARE_CARD
from widgets.labware_card import LabwareCard
from widgets.labware_stack_card import LabwareStackCard
from widgets.status_popup import StatusPopup
from widgets.warning_dialog import WarningDialog
        

class LabwareScreen(QWidget):
    def __init__(self,parentObj):
        super().__init__()
        self.rightStackWidget = ScrollableWidget()
        self.leftInfoWidget = ScrollableWidget()
        self.activeLabwares = []
        self.selectedItem = 0
        self.addedLabwares = []
        self.filters = {
            "type": 'All',
            "make": 'All'
        }
        self.infoSectionId = 0
  
        self.middleScrollArea = ScrollableWidget()
        self.labwareData = Utils.load_json("labwares.json")
        self.filteredLabwares = self.labwareData
        
        
        self.typeOptions = set(map(lambda x: x["type"], self.labwareData))
        
        screenDimensions = QApplication.primaryScreen().size()
        screenLayoutWrapper = QVBoxLayout(self)

        # Heading
        mainHeading = Heading("Labware",level=1)
        screenLayoutWrapper.addWidget(mainHeading)
        
        # upperOptionsLayout
        upperOptionsWidget = QWidget()
        upperOptionsLayout = QHBoxLayout(upperOptionsWidget)
        
        optionAWrap = QWidget()
        optionALayout = QHBoxLayout(optionAWrap)
        
        optionALayout.addWidget(Heading("Type: ", level=5))
        optionAInput = ThemedSelector(size="medium")
        optionAInput.addItems(["All"])
        optionAInput.addItems(list(self.typeOptions))
        indexA = optionAInput.findText("All")
        if indexA >= 0:
            optionAInput.setCurrentIndex(indexA)
        optionALayout.addWidget(optionAInput)
       
        
        optionBWrap = QWidget()
        optionBLayout = QHBoxLayout(optionBWrap)
        
        optionBLayout.addWidget(Heading("Make: ", level=5))
        optionBInput = ThemedSelector(size="medium")
        optionBInput.addItems(["All"])
        indexB = optionBInput.findText("All")
        if indexB >= 0:
            optionBInput.setCurrentIndex(indexB)
        self.handleTypeChange("All", optionBInput)
        optionBLayout.addWidget(optionBInput)
        
        
        upperOptionsLayout.addWidget(optionAWrap)
        upperOptionsLayout.addWidget(optionBWrap)
        upperOptionsLayout.addStretch(1)
        
        screenLayoutWrapper.addWidget(upperOptionsWidget)
        
        
        # mainArea
        mainAreaWrapper = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainAreaWrapper)
        
        # main Area --> left Area
        leftAreaWidget = QWidget()
        leftAreaWidget.setMaximumSize(int(screenDimensions.width() * 0.18), int(screenDimensions.height() * 0.7))
        leftAreaWidget.setProperty("class", "dropper")
        leftAreaWidgetLayout = QVBoxLayout(leftAreaWidget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(6)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 60))  # RGBA shadow
        leftAreaWidget.setGraphicsEffect(shadow)
        leftAreaWidgetLayout.addWidget(Heading("Info. ", level=6))
        self.setInfo(0)
        leftAreaWidgetLayout.addWidget(self.leftInfoWidget)
        leftAreaWidgetLayout.addStretch(1)
        
        # main Area --> middle Area
        middleAreaWidget = QWidget()
        middleAreaWidget.setMaximumSize(int(screenDimensions.width() * 0.5), int(screenDimensions.height() * 0.7))
        middleAreaWidget.setProperty("class", "dropper")
        middleAreaWidgetLayout = QVBoxLayout(middleAreaWidget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(6)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 60))  # RGBA shadow
        middleAreaWidget.setGraphicsEffect(shadow)
        middleAreaWidgetLayout.setContentsMargins(0,0,0,0)
        middleAreaWidgetLayout.addWidget(self.middleScrollArea)
        

        
        # right Area --> right Area   
        rightAreaWidget = QWidget()   
        rightAreaWidget.setMaximumSize(int(screenDimensions.width() * 0.25), int(screenDimensions.height() * 0.7))
        rightAreaWidget.setProperty("class", "dropper")
        rightAreaWidgetLayout = QVBoxLayout(rightAreaWidget)
        rightAreaWidgetLayout.addSpacing(1)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(6)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 60))  # RGBA shadow
        rightAreaWidget.setGraphicsEffect(shadow)
        rightAreaWidgetLayout.addWidget(Heading("Labware Added",7))
        self.loadSelectedCards()
        rightAreaWidgetLayout.addWidget(self.rightStackWidget)
            
        
        mainAreaWrapperLayout.addSpacing(4)
        mainAreaWrapperLayout.addWidget(leftAreaWidget)
        mainAreaWrapperLayout.addWidget(middleAreaWidget)
        mainAreaWrapperLayout.addWidget(rightAreaWidget)

        
               
        screenLayoutWrapper.addWidget(mainAreaWrapper)
        
        # navigation Buttons
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
        screenLayoutWrapper.addWidget(bottomWidget)
        
        # events
        optionAInput.currentTextChanged.connect(lambda text: self.handleTypeChange(text,optionBInput))
        optionBInput.currentTextChanged.connect(lambda text: self.handleMakeChange(text))

    def handleSave(self,parentObj):
        # Logic to save labware configuration
        resevoirCount =  sum(1 for obj in self.addedLabwares if obj["type"] == "Reservoir")
        
        if len(self.addedLabwares)==0:
            dialog = WarningDialog("No Added Labwares",parent=self)
            dialog.exec_()
            return
        elif resevoirCount == 0:
            dialog = WarningDialog("No Reservoir Added",parent=self)
            dialog.exec_()
            return
        parentObj.labware_screen = self.addedLabwares
        StatusPopup("Saved Selection!", status="success", duration=1500)
        QTimer.singleShot(1800, lambda: parentObj.router("home"))
    
    def handleTypeChange(self,text,optionBInput):
        optionBInput.clear()
        optionBInput.addItems(["All"])
        indexB = optionBInput.findText("All")
        if indexB >= 0:
            optionBInput.setCurrentIndex(indexB)
        if text == "All":
            availableMakes = set(map(lambda x: x["make"], self.labwareData))
        else:
            availableMakes = set(
                map(lambda x: x["make"],
                    filter(lambda x: x["type"] == text and x.get("make"), self.labwareData))
            )
        optionBInput.addItems(list(availableMakes))
        self.filters["type"] = text
        self.filters["make"] = "All"
        self.filterLabwares()
    
    def handleMakeChange(self,text):
        self.filters["make"] = text
        self.filterLabwares()
    
    def loadCards(self):
        self.clearLayout(self.middleScrollArea.contentLayout())
        filteredCards = map(lambda x: LabwareCard(self,x), self.filteredLabwares)
        rows = len(self.filteredLabwares)
        grid = QGridLayout()
        grid.setSpacing(22)
        self.middleScrollArea.setContentLayout(grid)
        c=0
        r=0
        for x in filteredCards:
            if c==0:
                self.middleScrollArea.contentLayout().addWidget(x,r,c)
                c=1
            else:
                self.middleScrollArea.contentLayout().addWidget(x,r,c)
                c=0
                r = r + 1
        
        infoParameter = self.filteredLabwares[0]["index"] if len(self.filteredLabwares)>0 else -1
        self.setInfo(infoParameter)
    
    def filterLabwares(self):
        if self.filters["type"] == "All" and self.filters["make"] == "All":
            self.filteredLabwares = self.labwareData
        else:
            self.filteredLabwares = list(
                filter(
                    lambda x: (self.filters["type"] == "All" or x["type"] == self.filters["type"]) and
                               (self.filters["make"] == "All" or x["make"] == self.filters["make"]),
                    self.labwareData
                )
            )
        self.loadCards()
        
    def addLabwares(self,index):
        tempFilltr = list(filter(lambda x: x["index"]==index, self.filteredLabwares))
        self.addedLabwares.append(tempFilltr[0])
        self.loadSelectedCards()
    
    def removeAddedLabwares(self, index):
        i = next((i for i, item in enumerate(self.addedLabwares) if item["index"] == index), None)
        if i is not None:
            self.addedLabwares.pop(i)
        self.loadSelectedCards()

    
    def clearLayout(self,layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
    
    def setInfo(self,ind):
        if len(self.filteredLabwares)<=0 or ind == -1:
            self.clearLayout(self.leftInfoWidget.contentLayout())
            tempLayout = QVBoxLayout()
            self.leftInfoWidget.setContentLayout(tempLayout)
            templabel = QLabel("No data found!!")
            self.leftInfoWidget.contentLayout().addWidget(templabel)
        else:
            self.selectedItem = ind
            detailsData = self.labwareData[ind]["details"]
            self.clearLayout(self.leftInfoWidget.contentLayout())
            tempLayout = QVBoxLayout()
            self.leftInfoWidget.setContentLayout(tempLayout)
            for x in detailsData:
                dataWidget = QWidget()
                dataWidgetLayout = QVBoxLayout(dataWidget)
                label = QLabel(f'{x["label"]}  ')
                font = QFont("Arial", 12)
                font.setBold(True)
                label.setFont(font)
                value = QLabel(x["value"])
                value.setFont(QFont("Arial", 10))
                value.setStyleSheet("color: #BDD5F9;")
                dataWidgetLayout.addWidget(label)
                dataWidgetLayout.addWidget(value)
                self.leftInfoWidget.contentLayout().addWidget(dataWidget)
                
    def loadSelectedCards(self):
        if len(self.addedLabwares) == 0:
            self.clearLayout(self.rightStackWidget.contentLayout())
            tempLayout = QVBoxLayout()
            self.rightStackWidget.setContentLayout(tempLayout)
            templabel = QLabel("No Labwares Added!!")
            templabel.setStyleSheet("color: #BDD5F9;")
            self.rightStackWidget.contentLayout().addWidget(templabel)
            self.rightStackWidget.contentLayout().addStretch(1)
        else:
            self.clearLayout(self.rightStackWidget.contentLayout())
            tempLayout = QVBoxLayout()
            self.rightStackWidget.setContentLayout(tempLayout)
            
            for x in self.addedLabwares:
                card = LabwareStackCard(self,x)
                self.rightStackWidget.contentLayout().addWidget(card)
            
            self.rightStackWidget.contentLayout().addStretch(1)
                
        
        
