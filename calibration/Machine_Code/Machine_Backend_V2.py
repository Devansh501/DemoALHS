import sys
import serial
import time
import threading
import json
import os
import queue

#  Detection
from .box_detection_thread import BoxDetectionThread 

# Co-ordinate Function
from .Co_ordinate_Conversion_version2 import CoordinateConversion

# QT Threads, Timer, and Signal
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer


class CommandQueueWorker(QThread):
    log_signal = pyqtSignal(str)
    finished_batch_signal = pyqtSignal(object)

    def __init__(self, arduino, parent=None):
        super().__init__(parent)
        self.arduino = arduino
        self.command_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.running = True

    def enqueue(self, command_list, callback=None):
        self.command_queue.put((command_list, callback))
    
    def stop(self):
        self.stop_event.set()

    def run(self):
        while self.running:
            try:
                command_list, callback = self.command_queue.get(timeout=0.1)
                if not command_list:
                    continue

                for command in command_list:
                    if self.stop_event.is_set():
                        print("[QueueWorker] STOP signal received.")
                        break

                    self.arduino.write(command.strip().encode('Ascii'))
                    self.arduino.flush()
                    self.log_signal.emit(f"[QueueWorker] Sent: {command.strip()}")
                    
                    while not self.stop_event.is_set():
                        if self.stop_event.is_set():
                            break

                        line = self.arduino.read_until(';'.encode('Ascii'))
                        # print(line)
                        print(f"{line.decode('Ascii').strip()}")
                        # print()
                        if line.decode('Ascii').strip()=="OK;" or line.decode('Ascii')[:5] == "Error":
                            break
                        if line.decode('Ascii').strip()=="ER:1;" or line.decode('Ascii')[:5] == "Error":
                            break

                if callback:
                    QTimer.singleShot(0, lambda: callback())

            except queue.Empty:
                continue
            except Exception as e:
                print(f"[QueueWorker Error] {e}")
            
            print("[Worker] Finished Signal emitted")
            self.finished_batch_signal.emit(callback)



class LHSFunction():
    def __init__(self):
            super().__init__()
            self.home_done = False
            self.arduino = None
            self.IsStartupSend = False;
            self.stop_event = threading.Event()

            self.x1_val = 0.0
            self.y1_val = 0.0
            self.z1_val = 0.0
            self.x2_val = 0.0
            self.y2_val = 0.0
            self.z2_val = 0.0

            # --- Define the global variable in your class ---
            self.step_size = 0.1  # Default value
            self.is_First = True

            # Liquid Handling System variables 
            self.First_Tip = 0.0
            self.Insert_Tip = 0.0
            self.Clear = 0.0
            self.Reservoir = 0.0
            self.Dip = 0.0
            self.Aspiration = 0.0
            self.First_Block = 0.0
            self.Lower = 0.0
            self.Dispense = 0.0
            self.Ejection_Area = 0.0
            self.Ejected = 0.0
            self.isProcedureDone = False
            self.Dispense_val = 0
            
            
            self.init_serial()


    def init_serial(self):
            # while True:
        try:
            self.start_box_detection()
            self.arduino = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)
            # self.arduino = serial.Serial('/dev/Serial0', 115200, timeout=None)
            time.sleep(2)
            self.arduino.flush()
            self.arduino.reset_input_buffer()
            self.arduino.reset_output_buffer()
            

            print("[Arduino] Connected successfully.")
            self.worker = CommandQueueWorker(self.arduino)
            # self.worker.log_signal.connect(self.log)
            self.worker.finished_batch_signal.connect(self._handle_batch_done)
            self.worker.start()

            # Send startup values
            self.send_start_up_values()
            # if(self.arduino):break

        except Exception as e:
            print(f"[Arduino] Connection error: {e}")

# ======================================================= Object Detection Starts ==========================================================
    def start_box_detection(self):
        self.box_thread = BoxDetectionThread()
        self.box_thread.detection_result.connect(self.handle_box_detection_result)
        self.box_thread.start()

    def handle_box_detection_result(self, status, missing_boxes):
        if status == 5:
            print("✅ All boxes detected.")
            return True
        else:
            print(self.box_thread.detection_result)
            return False


# ======================================================= Object Detection Ends ==========================================================
        
    def enqueue_commands(self, command_list, on_done_callback=None):
        print("EnqueeCoomnads")
        if self.worker:
            print("Worker.enqueue")
            self.worker.enqueue(command_list, on_done_callback)

    def _handle_batch_done(self, callback):
        if(callback) :
            callback()

# =========================== Procedures =======================================

    def send_start_up_values(self):
        file_path = "calibration/Machine_Code/start_up_values.json"

        def isDone():
            print("StartUp Values Send")
            self.IsStartupSend = True
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            
        else:
            data = {
                    "SPMMS_X": 40.25,
                    "SPMMS_Y": 40.25,
                    "SPMMS_Z": 100,
                    "SPMMS_A": 117.2,
                    "Comments": "C1X{SPMMS_X}",
                    "MAX_FEED_X": 600,
                    "MAX_FEED_Y": 600,
                    "MAX_FEED_Z": 600,
                    "MAX_FEED_A": 500,
                    "Comments2": "C2X{MAX_FEED_X}",
                    "MAX_ACCELS_X": 300,
                    "MAX_ACCELS_Y": 300,
                    "MAX_ACCELS_Z": 200,
                    "MAX_ACCELS_A": 100,
                    "Comments3": "C3X{MAX_ACCELS_X}",
                    "MAX_TRAVELS_X": 401,
                    "MAX_TRAVELS_Y": 220,
                    "MAX_TRAVELS_Z": 190,
                    "MAX_TRAVELS_A": 200,
                    "Comments4": "C4X{MAX_TRAVELS_X}",
                    "OFFSETS_X": -3.1,
                    "OFFSETS_Y": -2.5,
                    "OFFSETS_Z": 0,
                    "OFFSETS_A": 0,
                    "Comments5": "C5X{OFFSETS_X}",
                    "HOMING_FEED_X": 30,
                    "HOMING_FEED_Y": 30,
                    "HOMING_FEED_Z": 30,
                    "HOMING_FEED_A": 100,
                    "Comments6": "C6X{HOMING_FEED_X}"
                }

        commands = [
           f'C1X{data["SPMMS_X"]};',
           f'C1Y{data["SPMMS_Y"]};',
           f'C1Z{data["SPMMS_Z"]};',
           f'C1A{data["SPMMS_A"]};',

           f'C2X{data["MAX_FEED_X"]};',
           f'C2Y{data["MAX_FEED_Y"]};',
           f'C2Z{data["MAX_FEED_Z"]};',
           f'C2A{data["MAX_FEED_A"]};',

           f'C3X{data["MAX_ACCELS_X"]};',
           f'C3Y{data["MAX_ACCELS_Y"]};',
           f'C3Z{data["MAX_ACCELS_Z"]};',
           f'C3A{data["MAX_ACCELS_A"]};',

           f'C4X{data["MAX_TRAVELS_X"]};',
           f'C4Y{data["MAX_TRAVELS_Y"]};',
           f'C4Z{data["MAX_TRAVELS_Z"]};',
           f'C4A{data["MAX_TRAVELS_A"]};',

           f'C5X{data["OFFSETS_X"]};',
           f'C5Y{data["OFFSETS_Y"]};',
           f'C5Z{data["OFFSETS_Z"]};',
           f'C5A{data["OFFSETS_A"]};',


           f'C6X{data["HOMING_FEED_X"]};',
           f'C6Y{data["HOMING_FEED_Y"]};',
           f'C6Z{data["HOMING_FEED_Z"]};',
           f'C6A{data["HOMING_FEED_A"]};'
        ]

        print("D5;")
        self.enqueue_commands(["D5;"]) # First Command for debugging
        print("Sending is Done Callback")
        self.enqueue_commands(commands, on_done_callback=isDone)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def start_action(self):
        print("Start button clicked")

    def Aspirate_Func(self):
        print("Aspirate button clicked")
        self.Dispense_val = 0;
        self.enqueue_commands(["G0A0;"])
    
    def dispense_Func(self):
        print("dispense button clicked")
        self.Dispense_val = self.Dispense_val+50
        self.enqueue_commands([f"G0A{self.Dispense_val};"])

    def eject_Func(self):
        self.enqueue_commands(["E0;"])

# =========================== Procedures =========================================
  
    # def Single_Tip_row_Ejection(self):
    #     self.plasticus_coordinates = CoordinateConversion()
    #     Tip_Box_List = self.plasticus_coordinates.get_Plasticus_Tip_Box_List()
    #     Well_PLate_List = self.plasticus_coordinates.get_Plasticus_Well_Plate_List()

    #     for i in range(0, 12):
    #         # print(f"Tip = {Tip_Box_List[i]}")
    #         self.enqueue_commands([Tip_Box_List[i]])
    #         self.enqueue_commands([
    #             "G0Z177;",   # Insert
    #             "G0Z100;", # Clear
    #             "G0X50Y202;", #Reservoir
    #             "G0Z162;", #Dip
    #             "G0Z170A0;", #Aspirate
    #             "G0Z100;" #Clear
    #         ])
    #         asp = 0;
    #         for z in Well_PLate_List[i]:
    #             # print(f"well = {z}")
    #             asp+=20
    #             self.enqueue_commands([z])
    #             self.enqueue_commands([
    #                 "G0Z179.5;", #Lower
    #                 f"G0Z178A{asp};", #dispense
    #                 "G0Z160;" # Clear
    #             ])
    #         self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])
    #     self.enqueue_commands([
    #             "G0Z10;",
    #             "G0X10Y10;" #Clear
    #             ])

    # def Single_Tip_Ejection(self):
    #     self.plasticus_coordinates = CoordinateConversion()
    #     Tip_Box_List = self.plasticus_coordinates.get_Plasticus_Tip_Box_List()
    #     Well_PLate_List = self.plasticus_coordinates.get_Plasticus_Well_Plate_List()

    #     well_Plates = []

    #     for i, row in enumerate (Well_PLate_List):
    #         for j, val in enumerate (row):
    #             well_Plates.append(val)

    #     for i, val1 in enumerate(Tip_Box_List):
    #         # self.enqueue_commands(["C5X-8.9;C5Y-9;"])
    #         self.enqueue_commands([Tip_Box_List[i]])
    #         self.enqueue_commands([
    #             "G0Z179;",   # Insert
    #             "G0Z100;", # Clear
    #             "G0X50Y202;", #Reservoir
    #             "G0Z162;", #Dip
    #             "G0Z170A0;", #Aspirate
    #             "G0Z100;" #Clear
    #         ])
    #         # self.enqueue_commands(["C5X-2;C5Y0;"])
    #         self.enqueue_commands([well_Plates[i]])
    #         self.enqueue_commands([
    #             "G0Z177;", #Lower
    #             "G0Z176A200;", #dispense
    #             "G0Z160;" # Clear

    #         ])
    #         self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A150;"     
    #         ])
    #     self.enqueue_commands([
    #         "G0Z10;",
    #         "G0X10Y10;" #Clear
    #         ])

    def check_Tip_Box(self):
        self.plasticus_coordinates = CoordinateConversion()
        commands = self.plasticus_coordinates.get_Plasticus_Tip_Box_List()
        ejection = self.plasticus_coordinates.get_Ejection_Area()

        for val in commands:
            self.enqueue_commands([val])
            self.enqueue_commands([
                "G0Z176.5;",   # Insert
                "G0Z80;",  # Lower
                f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                "E0;", #Eject
            ])

    def check_Well_Plate(self):
        self.plasticus_coordinates = CoordinateConversion()
        commands = self.plasticus_coordinates.get_Plasticus_One_Well_Plate_List()
        ejection = self.plasticus_coordinates.get_Ejection_Area()
        self.enqueue_commands([
            "G0X9.2Y44.8;"
            "G0Z176.5;",   # Insert
            "G0Z80;",  # Lower
        ])

        for val in commands:
            print(f"val = {val}")
            self.enqueue_commands([val])
            self.enqueue_commands([
                "G0Z176.5;",   # Insert
                "G0Z150;",  # UP
            ])
            
        self.enqueue_commands([
            "G0Z80;",  # Lower
            f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
            "E0;", #Eject
        ])
    
    # def Diagonal_Liquid_Drop(self):
    #     self.plasticus_coordinates = CoordinateConversion()
    #     Tip_Box_List = self.plasticus_coordinates.get_Plasticus_Tip_Box_List()
    #     Well_PLate_List = self.plasticus_coordinates.get_Plasticus_Well_Plate_List()

    #     for i in range(0, 8):
    #         self.enqueue_commands([Tip_Box_List[i]])
    #         self.enqueue_commands([
    #             "G0Z177;",   # Insert
    #             "G0Z100;", # Clear
    #             "G0X50Y202;", #Reservoir
    #             "G0Z162;", #Dip
    #             "G0Z170A0;", #Aspirate
    #             "G0Z100;" #Clear
    #         ])
    #         self.enqueue_commands([Well_PLate_List[i][i]])
    #         self.enqueue_commands([
    #             "G0Z179.5;", #Lower
    #             f"G0Z178A200;", #dispense
    #             "G0Z160;" # Clear
    #         ])
    #         self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])
    #     self.enqueue_commands([
    #             "G0Z10;",
    #             "G0X10Y10;" #Clear
    #             ])

    # def create_line(self):
    #     #  ==================================== First Line ========================================
    #     self.enqueue_commands([
    #         "G0X9.2Y44.8;",
    #         "G0Z177;",   # Insert
    #         "G0Z100;", # Clear
    #         "G0X50Y202;", #Reservoir
    #         "G0Z162;", #Dip
    #         "G0Z170A0;", #Aspirate
    #         "G0Z100;" #Clear
    #     ])
    #     self.enqueue_commands([
    #         "G0X150Y7;",
    #         "G0X150Y7Z184.5;",
    #         "G0X250Y7Z184.5A150F3;",
    #         "G0Z100;"
    #     ])
    #     self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])

    #     #  ==================================== Second Line ========================================
    #     self.enqueue_commands([
    #         "G0X18.23Y44.95;",
    #         "G0Z177;",   # Insert
    #         "G0Z100;", # Clear
    #         "G0X50Y202;", #Reservoir
    #         "G0Z162;", #Dip
    #         "G0Z170A0;", #Aspirate
    #         "G0Z100;" #Clear
    #     ])
    #     self.enqueue_commands([
    #         "G0X150Y12;",
    #         "G0X150Y12Z184.5;",
    #         "G0X250Y12Z184.5A150F3;",
    #         "G0Z100;"
    #     ])
    #     self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])

    #      #  ==================================== Third Line ========================================
    #     self.enqueue_commands([
    #         "G0X27.25Y45.11;",
    #         "G0Z177;",   # Insert
    #         "G0Z100;", # Clear
    #         "G0X50Y202;", #Reservoir
    #         "G0Z162;", #Dip
    #         "G0Z170A0;", #Aspirate
    #         "G0Z100;" #Clear
    #     ])
    #     self.enqueue_commands([
    #         "G0X150Y17;",
    #         "G0X150Y17Z184.5;",
    #         "G0X250Y17Z184.5A150F3;",
    #         "G0Z100;"
    #     ])
    #     self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])

    #      #  ==================================== Fourth Line ========================================
    #     self.enqueue_commands([
    #         "G0X36.28Y45.26;",
    #         "G0Z177;",   # Insert
    #         "G0Z100;", # Clear
    #         "G0X50Y202;", #Reservoir
    #         "G0Z162;", #Dip
    #         "G0Z170A0;", #Aspirate
    #         "G0Z100;" #Clear
    #     ])
    #     self.enqueue_commands([
    #         "G0X150Y22;",
    #         "G0X150Y22Z184.5;",
    #         "G0X250Y22Z184.5A150F3;",
    #         "G0Z100;"
    #     ])
    #     self.enqueue_commands([
    #             "G0Z80;",  # Lower
    #             "G0X300Y110;", #Ejection Area
    #             "E0;", #Eject
    #             "G0A160;"     
    #         ])

    # def runMethod(self, tip_box_list_dic: dict, aspiration_value: dict, well_plate_list_dic: dict):
    #     for key, value in tip_box_list_dic:
    #         x = value[0]
    #         y = value[1]
    #         self.plasticus_coordinates = CoordinateConversion()
    #         Tip_G_code = self.plasticus_coordinates.Tip_Single_Pos_Calculation(x, y)
    #         self.enqueue_commands([Tip_G_code])
            
    #         # Insert
    #         self.enqueue_commands([
    #             "G0Z177;",   # Insert
    #             "G0Z100;", # Clear
    #             "G0X50Y202;", #Reservoir
    #         ])

    #         asp = aspiration_value[key]
    #         self.enqueue_commands([
    #             "G0Z162;", #Dip
    #             f"G0A{asp}",
    #              "G0Z100;" #Clear
    #             ])
            
    #         for items in well_plate_list_dic[key]:
    #             well_x = items[0][0]
    #             well_y = items[0][1]
    #             disp = items[0][2]
    #             well_Gcode = self.plasticus_coordinates.Well_Single_Pos_Calculation(well_x, well_y)
    #             self.enqueue_commands([well_Gcode])
    #             self.enqueue_commands([
    #                 "G0Z177;", #Lower
    #                 f"G0Z176A{disp};", #dispense
    #                 "G0Z160;" # Clear

    #             ])
    #             self.enqueue_commands([
    #                 "G0Z80;",  # Lower
    #                 "G0X300Y110;", #Ejection Area
    #                 "E0;", #Eject
    #                 "G0A150;"     
    #             ])

    def serial_Dilution(self):
        self.plasticus_coordinates = CoordinateConversion()
        Tip_Box_List = self.plasticus_coordinates.get_Plasticus_Tip_Box_List()
        First_Well_PLate_List = self.plasticus_coordinates.get_Plasticus_One_Well_Plate_List()
        Second_Well_PLate_List = self.plasticus_coordinates.get_Plasticus_Two_Well_Plate_List()
        ejection = self.plasticus_coordinates.get_Ejection_Area()

        for i in range(0, 32):
            if(i<4):
                self.enqueue_commands([Tip_Box_List[i]])
                self.enqueue_commands([
                    "G0Z176.5;",   # Insert
                    "G0Z80;",  # clear
                ])
                if(i==0):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_First_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_First_Reagent_Box()[1]};"])
                
                elif(i==1):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Second_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Second_Reagent_Box()[1]};"])
                
                elif(i==2):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Third_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Third_Reagent_Box()[1]};"])
                
                elif(i==3):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Fourth_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Fourth_Reagent_Box()[1]};"])
                
                self.enqueue_commands([
                    "G0Z162;", #Dip
                    "G0Z170A0;", #Aspirate
                    "G0Z100;" #Clear
                ])
                x = i*12
                disp = 0
                for j in range(x, x+3):
                    self.enqueue_commands([First_Well_PLate_List[j]])
                    if j == x+2: 
                        disp = disp + 50
                    disp = disp + 50
                    self.enqueue_commands([
                    "G0Z177;", #Lower
                    f"G0Z176A{disp};", #dispense
                    "G0Z160;" # Clear
                    ])
                self.enqueue_commands([
                    "G0Z80;" #Clear
                ])

                if(i==0):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_First_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_First_Reagent_Box()[1]};"])
                
                elif(i==1):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Second_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Second_Reagent_Box()[1]};"])
                
                elif(i==2):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Third_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Third_Reagent_Box()[1]};"])
                
                elif(i==3):
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Fourth_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Fourth_Reagent_Box()[1]};"])
                
                self.enqueue_commands([
                    "G0Z162;", #Dip
                    "G0Z170A0;", #Aspirate
                    "G0Z100;" #Clear
                ])

                l = (i*12 )+3
                disp = 0
                for k in range (l, l+3):
                    self.enqueue_commands([First_Well_PLate_List[k]])
                    if k == l+2: 
                        disp = disp + 50
                    disp = disp + 50
                    self.enqueue_commands([
                    "G0Z177;", #Lower
                    f"G0Z176A{disp};", #dispense
                    "G0Z160;" # Clear
                    ])

                self.enqueue_commands([
                    "G0Z80;",  # Clear
                    f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                    "E0;", #Eject
                    "G0A150;"     
                ])
                # pass

            elif(i>=4 and i<8):
                # pass
                if(i==4):
                    #  ======================= Tip Selection =================================
                    self.enqueue_commands([Tip_Box_List[i]])


                    self.enqueue_commands([
                        "G0Z176.5;",   # Insert
                        "G0Z80;",  # clear
                    ])

                    # ===================== Selecting First Reagent Box ===================================

                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_First_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_First_Reagent_Box()[1]};"])
                    self.enqueue_commands([
                        "G0Z162;", #Dip
                        "G0Z170A0;", #Aspirate
                        "G0Z100;" #Clear
                    ])
                    x = i*12
                    disp = 0
                    for j in range(x, x+3):
                        self.enqueue_commands([First_Well_PLate_List[j]])
                        if j == x+2: 
                            disp = disp + 50
                        disp = disp + 50
                        self.enqueue_commands([
                        "G0Z177;", #Lower
                        f"G0Z176A{disp};", #dispense
                        "G0Z160;" # Clear
                        ])

                    self.enqueue_commands([
                        "G0Z80;",  # Clear
                        f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                        "E0;", #Eject
                        "G0A150;"     
                    ])
                elif(i==5):
                    #  ======================= Tip Selection =================================
                    self.enqueue_commands([Tip_Box_List[i]])


                    self.enqueue_commands([
                        "G0Z176.5;",   # Insert
                        "G0Z80;",  # clear
                    ])
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Second_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Second_Reagent_Box()[1]};"])
                    self.enqueue_commands([
                        "G0Z162;", #Dip
                        "G0Z170A0;", #Aspirate
                        "G0Z100;" #Clear
                    ])
                    disp = 0
                    x = (i-1)*12
                    for j in range(x, x+3):
                        self.enqueue_commands([First_Well_PLate_List[j]])
                        if j == x+2: 
                            disp = disp + 50
                        disp = disp + 50
                        self.enqueue_commands([
                        "G0Z177;", #Lower
                        f"G0Z176A{disp};", #dispense
                        "G0Z160;" # Clear
                        ])

                    self.enqueue_commands([
                        "G0Z80;",  # Clear
                        f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                        "E0;", #Eject
                        "G0A150;"     
                    ])
                elif i==6:
                    #  ======================= Tip Selection =================================
                    self.enqueue_commands([Tip_Box_List[i]])


                    self.enqueue_commands([
                        "G0Z176.5;",   # Insert
                        "G0Z80;",  # clear
                    ])
                        #  =========================== Third Reagent Box =======================

                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Third_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Third_Reagent_Box()[1]};"])
                    self.enqueue_commands([
                        "G0Z162;", #Dip
                        "G0Z170A0;", #Aspirate
                        "G0Z100;" #Clear
                    ])

                    l = ((i-2)*12)+3
                    disp = 0
                    for k in range (l, l+3):
                        self.enqueue_commands([First_Well_PLate_List[k]])
                        if k == l+2: 
                            disp = disp + 50
                        disp = disp + 50
                        self.enqueue_commands([
                        "G0Z177;", #Lower
                        f"G0Z176A{disp};", #dispense
                        "G0Z160;" # Clear
                        ])

                    self.enqueue_commands([
                        "G0Z80;",  # Clear
                        f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                        "E0;", #Eject
                        "G0A150;"     
                    ])
                elif(i==7):
                    #  ======================= Tip Selection =================================
                    self.enqueue_commands([Tip_Box_List[i]])


                    self.enqueue_commands([
                        "G0Z176.5;",   # Insert
                        "G0Z80;",  # clear
                    ])
                    self.enqueue_commands([f"G0X{self.plasticus_coordinates.get_Fourth_Reagent_Box()[0]}Y{self.plasticus_coordinates.get_Fourth_Reagent_Box()[1]};"])
                    self.enqueue_commands([
                        "G0Z162;", #Dip
                        "G0Z170A0;", #Aspirate
                        "G0Z100;" #Clear
                    ])
                    l = ((i-3)*12 )+3
                    disp = 0
                    for k in range (l, l+3):
                        self.enqueue_commands([First_Well_PLate_List[k]])
                        if k == l+2: 
                            disp = disp + 50
                        disp = disp + 50
                        self.enqueue_commands([
                        "G0Z177;", #Lower
                        f"G0Z176A{disp};", #dispense
                        "G0Z160;" # Clear
                        ])

                    self.enqueue_commands([
                        "G0Z80;",  # Clear
                        f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                        "E0;", #Eject
                        "G0A50;"     
                    ])
                
            elif(i==8):
                #  ======================= Tip Selection =================================
                self.enqueue_commands([Tip_Box_List[i]])
                self.enqueue_commands([
                    "G0Z178;",   # Insert
                    "G0Z80;",  # clear
                ])
                x = i*6
                for j in range(x, x+3):
                    #  Aspiration from Well
                    self.enqueue_commands([First_Well_PLate_List[j]])
                    self.enqueue_commands([
                    "G0Z178;", #Lower
                    f"G0Z176A0;", #dispense
                    "G0Z160;" # Clear
                    ])


                    self.enqueue_commands([First_Well_PLate_List[j+12]])
                    self.enqueue_commands([
                    "G0Z178;", #Lower
                    f"G0Z176A50;", #dispense
                    "G0Z160;" # Clear
                    ])

                self.enqueue_commands([
                    "G0Z80;",  # Clear
                    f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                    "E0;", #Eject
                    "G0A50;"
                         
                ])

            elif(i==9):
                #  ======================= Tip Selection =================================
                self.enqueue_commands([Tip_Box_List[i]])
                self.enqueue_commands([
                    "G0Z178;",   # Insert
                    "G0Z80;",  # clear
                ])
                l=((i-1)*6)+3
                for k in range(l, l+3):
                    #  Aspiration from Well
                    self.enqueue_commands([First_Well_PLate_List[k]])
                    self.enqueue_commands([
                    "G0Z177;", #Lower
                    "G0Z176A0;", #dispense
                    "G0Z160;" # Clear
                    ])


                    self.enqueue_commands([First_Well_PLate_List[k+12]])
                    self.enqueue_commands([
                    "G0Z177;", #Lower
                    "G0Z176A50;", #dispense
                    "G0Z160;" # Clear
                    ])
                self.enqueue_commands([
                    "G0Z80;",  # Clear
                    f"G0X{ejection[0]}Y{ejection[1]};", #Ejection Area
                    "E0;", #Eject
                    "G0A150;",
                    "G0X10Y10Z10A150;"     
                ])





                
               
                


# ============================ Screen Functionality ===================================
    def save_calibration(self,X_val,Y_val):
        file_path1 = "calibration/Machine_Code/start_up_values.json"
        file_path2 = "calibration/Machine_Code/box_position.json"
        if os.path.exists(file_path1):
            with open(file_path1, "r") as f:
                data1 = json.load(f)
        
        if os.path.exists(file_path2):
            with open(file_path2, "r") as f:
                data2 = json.load(f)
        
        data1["OFFSETS_X"] = round(data1["OFFSETS_X"] + (data2['Plasticus_Tip_Box']['plasticus_A1_X_val'] - round(X_val, 2)), 2)
        data1["OFFSETS_Y"] = round(data1["OFFSETS_Y"] + (data2['Plasticus_Tip_Box']['plasticus_A1_Y_val'] - round(Y_val, 2)), 2)
        with open(file_path1, "w") as f:
            json.dump(data1, f, indent=4)
        self.send_start_up_values()            
    
    def start_clicked(self):
        
        print("START clicked")

        # Running Procedure
        # self.check_Well_Plate()
        # self.Single_Tip_row_Ejection()
        # self.Single_Tip_Ejection()
        # self.check_Tip_Box()
        self.serial_Dilution()
        # self.create_line()
        # self.Diagonal_Liquid_Drop()

    def stop_clicked(self):
        print("STOP clicked - sending Dummy STOP to Arduino.")
        if(self.worker and self.worker.isRunning):
            print("Stopping worker thread...")
            self.worker.stop()
            print("Worker Stopped")
        else:
            print("No running worker to Stop!!!")

    def closeEvent(self, event):
        if hasattr(self, 'box_thread'):
            self.box_thread.stop()
            self.box_thread.quit()
            self.box_thread.wait()
        event.accept()

    def home_clicked(self):
        # self.stop_event.clear()
        print("HOME clicked")

        def on_home_done():
            print("Home completed.")
            self.home_done = True

        commands = ["H3;", "H2;", "H1;", "H0;", "G0A150;"]
        # commands = ["H2;", "H1;", "H0;"]
        self.enqueue_commands(commands, on_done_callback=on_home_done)


