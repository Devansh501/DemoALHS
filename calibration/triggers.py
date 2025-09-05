import json
import os
from .utils import Utils
from PyQt5.QtWidgets import QMessageBox,QApplication
from PyQt5.QtWidgets import QLabel
from .Machine_Code.Machine_Backend_V2 import LHSFunction
Liquid_handling = LHSFunction()
utils = Utils()

class Triggers:
    def btn_y_up(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.YCoOrdinate = max((round((obj.YCoOrdinate - obj.stepSize) , 2)), data["OFFSETS_Y"])
            edit.setText(str(obj.YCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0Y{obj.YCoOrdinate};'])
    
    def btn_y_down(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.YCoOrdinate = min((round((obj.YCoOrdinate + obj.stepSize) , 2)), data["MAX_TRAVELS_Y"])
            edit.setText(str(obj.YCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0Y{obj.YCoOrdinate};'])

    def btn_x_left(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.XCoOrdinate = max((round((obj.XCoOrdinate - obj.stepSize) , 2)), data["OFFSETS_X"])
            edit.setText(str(obj.XCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0X{obj.XCoOrdinate};'])

    def btn_x_right(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.XCoOrdinate = min((round((obj.XCoOrdinate + obj.stepSize) , 2)), data["MAX_TRAVELS_X"])
            edit.setText(str(obj.XCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0X{obj.XCoOrdinate};'])

    def btn_z_up(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.ZCoOrdinate = max((round((obj.ZCoOrdinate - obj.stepSize) , 2)), data["OFFSETS_Z"])
            edit.setText(str(obj.ZCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0Z{obj.ZCoOrdinate};'])

    def btn_z_down(obj,edit):
        if not Liquid_handling.home_done:
                utils.warning(obj,"Press Home First...")
        else:
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            obj.ZCoOrdinate = min((round((obj.ZCoOrdinate + obj.stepSize) , 2)), data["MAX_TRAVELS_Z"])
            edit.setText(str(obj.ZCoOrdinate))
            Liquid_handling.enqueue_commands([f'G0Z{obj.ZCoOrdinate};'])

    def x_label_edit(obj,text,edit):
        try:
            num = int(text)
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            maxV = data["MAX_TRAVELS_X"]
            minV = 0
            if num >=minV and num<=maxV:
                obj.XCoOrdinate = num
                edit.setText(str(num))
            else:
                edit.setText(str(obj.XCoOrdinate))
                # An Value Exceeded Alert here TODO
        except:
            print("Wrong Input Detected") 
            # ALSO HERE
            edit.setText(str(obj.XCoOrdinate))
    
    def y_label_edit(obj,text,edit):
        try:
            num = int(text)
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            maxV = data["MAX_TRAVELS_Y"]
            minV = 0
            if num >=minV and num<=maxV:
                obj.YCoOrdinate = num
                edit.setText(str(num))
            else:
                edit.setText(str(obj.YCoOrdinate))
                # An Value Exceeded Alert here TODO
        except:
            print("Wrong Input Detected")
            obj.setText(str(obj.YCoOrdinate))

    def z_label_edit(obj,text,edit):
        try:
            num = int(text)
            file_path = "calibration/Machine_Code/start_up_values.json"
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
            maxV = data["MAX_TRAVELS_Z"]
            minV = 0
            if num >=minV and num<=maxV:
                obj.ZCoOrdinate = num
                edit.setText(str(num))
            else:
                edit.setText(str(obj.ZCoOrdinate))
                # An Value Exceeded Alert here TODO
        except:
            print("Wrong Input Detected")
            obj.setText(str(obj.ZCoOrdinate))
    
    def functionality_buttons(name,self):
        if name=='DLD':
            if not Liquid_handling.home_done:
                utils.warning(self,"Press Home First...")
            else:
                Liquid_handling.Diagonal_Liquid_Drop()
        elif name=='STRE':
            if not Liquid_handling.home_done:
                utils.warning(self,"Press Home First...")
            else:
                Liquid_handling.Single_Tip_row_Ejection()
        elif name=='STE':
            if not Liquid_handling.home_done:
                utils.warning(self,"Press Home First...")
            else:
                Liquid_handling.Single_Tip_Ejection()
        elif name=='START':
            if not Liquid_handling.home_done:
                utils.warning(self,"Press Home First...")
            else:    
                Liquid_handling.start_clicked()
        elif name=='OK':
            if not Liquid_handling.home_done:
                utils.warning(self,"Press Home First...")
            else:
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setWindowTitle("Confirm Save")
                msg_box.setText("Are you sure you want to save these values?")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: #23272e;
                        color: white;
                        border-radius: 10px;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 16px;
                    }
                    QLabel, QMessageBox QLabel {
                        background-color: #23272e;
                        color: white;
                        font-size: 18px;
                        font-weight: bold;
                        border-radius: 0px;
                        padding: 8px 0 8px 0;
                    }
                    QPushButton {
                        background-color: #3b4252;
                        color: white;
                        border: 1px solid #81a1c1;
                        padding: 8px 24px;
                        border-radius: 6px;
                        font-size: 15px;
                        margin: 8px 4px;
                    }
                    QPushButton:hover {
                        background-color: #5e81ac;
                        color: #fff;
                    }
                """)
                # Set label text color to white
                from PyQt5.QtWidgets import QLabel as _QLabel
                label = msg_box.findChild(_QLabel)
                if label:
                    label.setStyleSheet("background-color: #23272e; color: white; font-size: 18px; font-weight: bold; border-radius: 0px; padding: 8px 0 8px 0;")

                # Use QTimer to style buttons after dialog is shown
                from PyQt5.QtCore import QTimer
                def style_buttons():
                    yes_btn = msg_box.button(QMessageBox.Yes)
                    no_btn = msg_box.button(QMessageBox.No)
                    if yes_btn:
                        yes_btn.setStyleSheet("background-color: #5e81ac; color: white; border: 1px solid #81a1c1; border-radius: 6px; font-size: 15px; padding: 8px 24px; margin: 8px 4px;")
                    if no_btn:
                        no_btn.setStyleSheet("background-color: #3b4252; color: white; border: 1px solid #81a1c1; border-radius: 6px; font-size: 15px; padding: 8px 24px; margin: 8px 4px;")
                QTimer.singleShot(0, style_buttons)

                reply = msg_box.exec_()

                if reply == QMessageBox.Yes:
                    print("User chose Yes")
                    Liquid_handling.save_calibration(self.XCoOrdinate,self.YCoOrdinate)
                else:
                    print("User chose No")
            
        elif name=='HOME':
            if not Liquid_handling.IsStartupSend:
               utils.warning(self,"Wait For Startup...")
            else:
                Liquid_handling.home_clicked()
        
        elif name=='btn1':
            if not Liquid_handling.IsStartupSend:
               utils.warning(self,"Wait For Startup...")
            else:
                print("btn1 clicked")
        elif name=='btn2':
            if not Liquid_handling.IsStartupSend:
               utils.warning(self,"Wait For Startup...")
            else:
                print("btn2 clicked")
        