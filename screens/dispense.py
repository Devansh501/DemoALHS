from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,QPushButton
from PyQt5.QtCore import  Qt
from widgets.heading import Heading
from widgets.button import ThemedButton
from widgets.well_plate_selector import WellPlateSelectorWidget
from widgets.widget_tab_container import TabbedContainer
from widgets.newSelector import ThemedSelector
from widgets.numericInput import ThemedInputField
from widgets.menu_button import MenuButton
from widgets.scroll_area import ScrollableWidget



class StepAdder(QWidget):
    def __init__(self, dataObj,wrapper):
        super().__init__()
        self.reagentNames = [reagent['reagentName'] for reagent in dataObj.reagent_screen["reagentsConfigured"]]
        self.stepObj = {
            "reagentName":self.reagentNames[0],
            "reagentQuantity":"",
        }
        mainWrapper = QVBoxLayout(self)
        reagentSelectorLayout = QHBoxLayout()
        self.reagentSelector = ThemedSelector(placeholder="Add Reagent", size="small")

        self.reagentSelector.setItems(self.reagentNames)
        self.reagentSelector.currentTextChanged.connect(lambda x:self.reagentSelectionHandler(x,dataObj))
        self.colorBearer = QWidget()
        self.colorBearer.setFixedSize(50, 28)
        
        self.colorBearer.setStyleSheet(f"background-color: {dataObj.reagent_screen["reagentsConfigured"][0]["reagentColor"].name()}; border-radius:4px")
        reagentSelectorLayout.addStretch(1)
        reagentSelectorLayout.addWidget(Heading("Select Reagent",8))
        reagentSelectorLayout.addSpacing(2)
        reagentSelectorLayout.addWidget(self.reagentSelector)
        reagentSelectorLayout.addSpacing(1)
        reagentSelectorLayout.addWidget(self.colorBearer)
        reagentSelectorLayout.addStretch(1)
        mainWrapper.addLayout(reagentSelectorLayout)
        
        reagentQuantityLayout = QHBoxLayout()
        self.reagentQuantityInput = ThemedInputField(placeholder_text="0",size="small",numeric_only=True)
        self.reagentQuantityInput.line_edit.textChanged.connect(lambda x: self.reagentQuantityHandler(x))
        reagentQuantityLayout.addStretch(1)
        reagentQuantityLayout.addWidget(Heading("Set Quantity",8))
        reagentQuantityLayout.addSpacing(2)
        reagentQuantityLayout.addWidget(self.reagentQuantityInput)
        reagentQuantityLayout.addStretch(1)
        mainWrapper.addLayout(reagentQuantityLayout)
        
        buttonLayout = QHBoxLayout()
        addStepButton = MenuButton("Add Step",fontSize=12,btnHeight=110,btnWidth=150)
        addStepButton.clicked.connect(lambda : self.handleAddStep(wrapper))
        resetDefaults = MenuButton("Reset Defaults",fontSize=12,btnHeight=110,btnWidth=150)
        buttonLayout.addWidget(addStepButton)
        buttonLayout.addWidget(resetDefaults)
        mainWrapper.addLayout(buttonLayout)
    
    def handleAddStep(self,wrapper):
        wrapper.steps.append(self.stepObj)
        self.reagentQuantityInput.setValue("")
        wrapper.wellPlateSelector.clear_all_selections()
        
    
    def reagentSelectionHandler(self,text,dataObj):
        reagents_list = dataObj.reagent_screen["reagentsConfigured"]
        color = next((r["reagentColor"] for r in reagents_list if r["reagentName"] == text), None)
        self.colorBearer.setStyleSheet(f"background-color: {color.name()}; border-radius:4px")
        self.stepObj["reagentName"] = text
    
    def reagentQuantityHandler(self,text):
        self.stepObj["reagentQuantity"] = text
        
         
        

class ProtocolStepDump(QWidget):
    def __init__(self):
        super().__init__()
        mainWrapperA = QVBoxLayout(self)
        mainWrapperA.addWidget(Heading("Protocol",level=8))
        self.scrollStepArea = ScrollableWidget()
        


class DispenseScreen(QWidget):
    def __init__(self, parentObj):
        super().__init__()
        # print(f"lol phun!! {parentObj.labware_screen}")    
        screenLayoutWrapper = QVBoxLayout(self)
        
        # Heading
        heading = Heading("Dispense", level=1)
        
        # Main Area
        mainArea = QWidget()
        mainAreaWrapperLayout = QHBoxLayout(mainArea)
        
        # Left Area - Well Plate Selector Widget
        leftAreaWrapper = QWidget()
        leftAreaLayout = QVBoxLayout(leftAreaWrapper)
        
        self.availableWellPlates = [item for item in parentObj.labware_screen if item['type'] == 'Well Plate']
        

      
        
        # Create well plate selector
        self.wellPlateSelector = WellPlateSelectorWidget(self.availableWellPlates)
        self.wellPlateSelector.selectionChanged.connect(self.on_well_selection_changed)
        
        leftAreaLayout.addWidget(self.wellPlateSelector)
        leftAreaLayout.addStretch()
        
        mainAreaWrapperLayout.addWidget(leftAreaWrapper)
        mainAreaWrapperLayout.setAlignment(leftAreaWrapper,Qt.AlignLeft)        
        
        rightAreaWrapper = QWidget()
        rightAreaWrapperLayout = QVBoxLayout(rightAreaWrapper)
        
        self.tabber = TabbedContainer()
        self.steps = []
        
        self.tabber.add_tab("Options",StepAdder(parentObj,self))
        self.tabber.add_tab("Protocols",ProtocolStepDump())
        
        rightAreaWrapperLayout.addWidget(self.tabber)
        
        mainAreaWrapperLayout.addWidget(rightAreaWrapper)
        
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
