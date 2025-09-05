import array as arr
import os 
import json

class CoordinateConversion():

    def __init__(self):
        super().__init__()
        self.plasticus_Tip_Box_coordinate_list = []
        self.plasticus_Well_Plate_1_coordinate_list = []
        self.plasticus_Well_Plate_2_coordinate_list = []

        file_path = "calibration/Machine_Code/box_position.json"
        # Load existing data or create default structure
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = {
                        "Plasticus_Tip_Box":{
                        "plasticus_A1_X_val": 3.8,
                        "plasticus_A12_X_val": 102.7,
                        "plasticus_H1_X_val": 3.4,
                        "plasticus_H12_X_val": 103.1,

                        "plasticus_A1_Y_val": 14.5,
                        "plasticus_A12_Y_val": 14.5,
                        "plasticus_H1_Y_val": 77.7,
                        "plasticus_H12_Y_val": 78.2,

                        "plasticus_m_val":8,
                        "plasticus_n_val":12
                    },

                    
                    "Plasticus_well_Plate_one": {
                        "plasticus_well_A1_X_val": 149.2,
                        "plasticus_well_A12_X_val":  247.5,
                        "plasticus_well_H1_X_val": 148.5,
                        "plasticus_well_H12_X_val":  247.5,

                        "plasticus_well_A1_Y_val": 15.4,
                        "plasticus_well_A12_Y_val":  16.4,
                        "plasticus_well_H1_Y_val": 78.9,
                        "plasticus_well_H12_Y_val":  79.6,

                        "plasticus_well_m_val":8,
                        "plasticus_well_n_val":12
                    },

                    "Plasticus_well_Plate_two": {
                        "plasticus_well_A1_X_val": 145.0,
                        "plasticus_well_A12_X_val":  244.3,
                        "plasticus_well_H1_X_val": 145.3,
                        "plasticus_well_H12_X_val":  244.1,

                        "plasticus_well_A1_Y_val": 122.7,
                        "plasticus_well_A12_Y_val":  122.7,
                        "plasticus_well_H1_Y_val": 185.7,
                        "plasticus_well_H12_Y_val":  185.7,

                        "plasticus_well_m_val":8,
                        "plasticus_well_n_val":12
                    },

                    "Ejection_Box" : {
                        "x": 354.3,
                        "y": 97.7
                    },

                    "Reagent_Box":{
                        "First_Reagent_Box_X": 14.3,
                        "First_Reagent_Box_Y": 167.7,
                        
                        "Second_Reagent_Box_X": 44.3,
                        "Second_Reagent_Box_Y": 167.7,
                        
                        "Third_Reagent_Box_X": 74.3,
                        "Third_Reagent_Box_Y": 167.7,
                        
                        "Fourth_Reagent_Box_X": 104.3,
                        "Fourth_Reagent_Box_Y": 167.7
                    }


                }

        self.data = data

    def Co_ordinate_Horizontal_Calc(self, A1_X_Val, A1_Y_Val, A12_X_Val, A12_Y_Val, H1_X_Val, H1_Y_Val, m_val, n_val):
        x_offset = ((A12_X_Val - A1_X_Val) / (n_val -1))
        y_offset = ((H1_Y_Val - A1_Y_Val) / (m_val - 1))
        delta_x =  ((H1_X_Val - A1_X_Val) / (m_val -1))
        delta_y = ((A12_Y_Val - A1_Y_Val) / (n_val - 1))

        plasticus_box = [["" for _ in range(n_val)] for _ in range(m_val)]
        # print(f"delta_x  = {delta_x}, x_offset = {x_offset}, delta_y = {delta_y}, y_offset = {y_offset}")

        for m in range (m_val):
            for n in range (n_val):
                pos_x = abs(round((A1_X_Val + ((n) * x_offset) + ((m) * delta_x)), 2))
                pos_y = abs(round((A1_Y_Val + (m) * y_offset + (n) * delta_y), 2))
                plasticus_box[m][n] = f"G0X{pos_x}Y{pos_y};"
        return plasticus_box
    

    # ============================= Function For Tip Box ============================================

    def Tip_Single_Pos_Calculation(self, m, n):
        x_offset = (self.data["Plasticus_Tip_Box"]["plasticus_A12_X_val"] - self.data["Plasticus_Tip_Box"]["plasticus_A1_X_val"]) / (self.data["Plasticus_Tip_Box"]["plasticus_n_val"] - 1)
        y_offset = (self.data["Plasticus_Tip_Box"]["plasticus_H1_Y_val"] - self.data["Plasticus_Tip_Box"]["plasticus_A1_Y_val"]) / (self.data["Plasticus_Tip_Box"]["plasticus_m_val"] -1)
        delta_x = (self.data["Plasticus_Tip_Box"]["plasticus_H1_X_val"] - self.data["Plasticus_Tip_Box"]["plasticus_A1_X_val"]) / (self.data["Plasticus_Tip_Box"]["plasticus_m_val"] -1)
        delta_y = (self.data["Plasticus_Tip_Box"]["plasticus_A12_Y_val"] - self.data["Plasticus_Tip_Box"]["plasticus_A1_Y_val"]) / (self.data["Plasticus_Tip_Box"]["plasticus_n_val"] - 1)
       
        # print(f"delta_x  = {delta_x}, x_offset = {x_offset}, delta_y = {delta_y}, y_offset = {y_offset}")

        pos_x = abs(round((self.data["Plasticus_Tip_Box"]["plasticus_A1_X_val"] + ((n-1) * x_offset) + ((m-1) * delta_x)), 2))
        pos_y = abs(round((self.data["Plasticus_Tip_Box"]["plasticus_A1_Y_val"] + (m-1) * y_offset + (n-1) * delta_y), 2))
        return f"G0X{pos_x}Y{pos_y};"
 
    def show_values(self):
        # ================= For Tip Box ===================
        co_ordinates = self.Co_ordinate_Horizontal_Calc(self.data["Plasticus_Tip_Box"]["plasticus_A1_X_val"], self.data["Plasticus_Tip_Box"]["plasticus_A1_Y_val"], 
                                             self.data["Plasticus_Tip_Box"]["plasticus_A12_X_val"], self.data["Plasticus_Tip_Box"]["plasticus_A12_Y_val"], self.data["Plasticus_Tip_Box"]["plasticus_H1_X_val"], 
                                             self.data["Plasticus_Tip_Box"]["plasticus_H1_Y_val"], self.data["Plasticus_Tip_Box"]["plasticus_m_val"], self.data["Plasticus_Tip_Box"]["plasticus_n_val"])
        
        # ================= For Vertical Well Box ===================
        # co_ordinates = self.Co_ordinate_Vertical_Calc(self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"], 
        #                                      self.data["Plasticus_well_Plate"]["plasticus_well_J1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_J1_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A8_X_val"], 
        #                                      self.data["Plasticus_well_Plate"]["plasticus_well_A8_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_m_val"], self.data["Plasticus_well_Plate"]["plasticus_well_n_val"])
        
        for i, row in enumerate (co_ordinates):
            for j,val in enumerate (row):
                print(f"({i+1}, {j+1}) = {val}")

    def get_Plasticus_Tip_Box_List(self):
        co_ordinates = self.Co_ordinate_Horizontal_Calc(self.data["Plasticus_Tip_Box"]["plasticus_A1_X_val"], self.data["Plasticus_Tip_Box"]["plasticus_A1_Y_val"], 
                                             self.data["Plasticus_Tip_Box"]["plasticus_A12_X_val"], self.data["Plasticus_Tip_Box"]["plasticus_A12_Y_val"], self.data["Plasticus_Tip_Box"]["plasticus_H1_X_val"], 
                                             self.data["Plasticus_Tip_Box"]["plasticus_H1_Y_val"], self.data["Plasticus_Tip_Box"]["plasticus_m_val"], self.data["Plasticus_Tip_Box"]["plasticus_n_val"])
        for i, row in enumerate (co_ordinates):
            for j, val in enumerate (row):
                self.plasticus_Tip_Box_coordinate_list.append(val)
        return self.plasticus_Tip_Box_coordinate_list
    
    def get_Plasticus_One_Well_Plate_List(self):
        co_ordinates = self.Co_ordinate_Horizontal_Calc(self.data["Plasticus_well_Plate_one"]["plasticus_well_A1_X_val"], self.data["Plasticus_well_Plate_one"]["plasticus_well_A1_Y_val"], 
                                             self.data["Plasticus_well_Plate_one"]["plasticus_well_A12_X_val"], self.data["Plasticus_well_Plate_one"]["plasticus_well_A12_Y_val"], self.data["Plasticus_well_Plate_one"]["plasticus_well_H1_X_val"], 
                                             self.data["Plasticus_well_Plate_one"]["plasticus_well_H1_Y_val"], self.data["Plasticus_well_Plate_one"]["plasticus_well_m_val"], self.data["Plasticus_well_Plate_one"]["plasticus_well_n_val"])
        for i, row in enumerate (co_ordinates):
            for j, val in enumerate (row):
                self.plasticus_Well_Plate_1_coordinate_list.append(val)
        return self.plasticus_Well_Plate_1_coordinate_list
    
    def get_Plasticus_Two_Well_Plate_List(self):
        co_ordinates = self.Co_ordinate_Horizontal_Calc(self.data["Plasticus_well_Plate_two"]["plasticus_well_A1_X_val"], self.data["Plasticus_well_Plate_two"]["plasticus_well_A1_Y_val"], 
                                             self.data["Plasticus_well_Plate_two"]["plasticus_well_A12_X_val"], self.data["Plasticus_well_Plate_two"]["plasticus_well_A12_Y_val"], self.data["Plasticus_well_Plate_two"]["plasticus_well_H1_X_val"], 
                                             self.data["Plasticus_well_Plate_two"]["plasticus_well_H1_Y_val"], self.data["Plasticus_well_Plate_two"]["plasticus_well_m_val"], self.data["Plasticus_well_Plate_two"]["plasticus_well_n_val"])
        for i, row in enumerate (co_ordinates):
            for j, val in enumerate (row):
                self.plasticus_Well_Plate_2_coordinate_list.append(val)
        return self.plasticus_Well_Plate_2_coordinate_list
    
    def get_Ejection_Area(self):
        return (self.data["Ejection_Box"]["x"], self.data["Ejection_Box"]["y"])
    
    def get_First_Reagent_Box(self):
        return (self.data["Reagent_Box"]["First_Reagent_Box_X"], self.data["Reagent_Box"]["First_Reagent_Box_Y"])
    def get_Second_Reagent_Box(self):
        return (self.data["Reagent_Box"]["Second_Reagent_Box_X"], self.data["Reagent_Box"]["Second_Reagent_Box_Y"])
    def get_Third_Reagent_Box(self):
        return (self.data["Reagent_Box"]["Third_Reagent_Box_X"], self.data["Reagent_Box"]["Third_Reagent_Box_Y"])
    def get_Fourth_Reagent_Box(self):
        return (self.data["Reagent_Box"]["Fourth_Reagent_Box_X"], self.data["Reagent_Box"]["Fourth_Reagent_Box_Y"])

    def checkFor(self):
        for i in range(0, 10):
            if(i%2 == 0):
                print(i)










x = CoordinateConversion()
# print(x.get_Plasticus_One_Well_Plate_List())
x.checkFor()
# x.get_values()
# x.show_values()
# x.Co_ordinate_Calc()
# print(x.get_Plasticus_Tip_Box_List())
# print(x.get_Plasticus_Well_Plate_List())


# print("==================================================")
# print(x.Tip_Single_Pos_Calculation(1,1))
# print(x.Well_Single_Pos_Calculation(2,1))







# ========================== Extra Function For Vertical Box Orientation ================================
        


    # def get_Plasticus_Well_Plate_List(self):
    #     co_ordinates = self.Co_ordinate_Vertical_Calc(self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"], 
    #                                          self.data["Plasticus_well_Plate"]["plasticus_well_J1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_J1_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A8_X_val"], 
    #                                          self.data["Plasticus_well_Plate"]["plasticus_well_A8_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_m_val"], self.data["Plasticus_well_Plate"]["plasticus_well_n_val"])
    #     # for i, row in enumerate (co_ordinates):
    #     #     for j, val in enumerate (row):
    #     #         self.plasticus_coordinate_list.append(val)

    #     self.plasticus_coordinate_list = co_ordinates
    #     return self.plasticus_coordinate_list
    

    # def Co_ordinate_Vertical_Calc(self, A1_X_Val, A1_Y_Val, J1_X_Val, J1_Y_Val, A8_X_Val, A8_Y_Val, m_val, n_val):
    #     x_offset = round(((A8_X_Val - A1_X_Val) / (m_val -1)), 2)
    #     y_offset = round(((J1_Y_Val - A1_Y_Val) / (n_val - 1)), 2)
    #     delta_x =  round(((J1_X_Val - A1_X_Val) / (n_val -1)), 3)
    #     delta_y = round(((A8_Y_Val - A1_Y_Val) / (m_val - 1)), 3)

    #     plasticus_box = [["" for _ in range(m_val)] for _ in range(n_val)]
    #     # print(f"delta_x  = {delta_x}, x_offset = {x_offset}, delta_y = {delta_y}, y_offset = {y_offset}")

    #     for n in range (n_val):
    #         for m in range (m_val):
    #             pos_x = abs(round((A1_X_Val + ((m) * x_offset) + ((n) * delta_x)), 2))
    #             pos_y = abs(round((A1_Y_Val + (n) * y_offset + (m) * delta_y), 2))
    #             plasticus_box[n][m] = f"G0X{pos_x}Y{pos_y};"
    #     return plasticus_box

    # def get_values(self):
    #     co_ordinates = self.Co_ordinate_Vertical_Calc(self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"], 
    #                                          self.data["Plasticus_well_Plate"]["plasticus_well_J1_X_val"], self.data["Plasticus_well_Plate"]["plasticus_well_J1_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_A8_X_val"], 
    #                                          self.data["Plasticus_well_Plate"]["plasticus_well_A8_Y_val"], self.data["Plasticus_well_Plate"]["plasticus_well_m_val"], self.data["Plasticus_well_Plate"]["plasticus_well_n_val"])
    #     for i in range(0, 8):
    #         print(co_ordinates[i][i])




    # def Well_Single_Pos_Calculation(self, m, n):
    #     x_offset = (self.data["Plasticus_well_Plate"]["plasticus_well_A8_X_val"] - self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"]) / (self.data["Plasticus_well_Plate"]["plasticus_well_m_val"] - 1)
    #     y_offset = (self.data["Plasticus_well_Plate"]["plasticus_well_J1_Y_val"] - self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"]) / (self.data["Plasticus_well_Plate"]["plasticus_well_n_val"] -1)
    #     delta_x = (self.data["Plasticus_well_Plate"]["plasticus_well_J1_X_val"] - self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"]) / (self.data["Plasticus_well_Plate"]["plasticus_well_n_val"] -1)
    #     delta_y = (self.data["Plasticus_well_Plate"]["plasticus_well_A8_Y_val"] - self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"]) / (self.data["Plasticus_well_Plate"]["plasticus_well_m_val"] - 1)
    
    #     # print(f"delta_x  = {delta_x}, x_offset = {x_offset}, delta_y = {delta_y}, y_offset = {y_offset}")

    #     pos_x = abs(round((self.data["Plasticus_well_Plate"]["plasticus_well_A1_X_val"] + ((m-1) * x_offset) + ((n-1) * delta_x)), 2))
    #     pos_y = abs(round((self.data["Plasticus_well_Plate"]["plasticus_well_A1_Y_val"] + (n-1) * y_offset + (m-1) * delta_y), 2))
    #     return f"G0X{pos_x}Y{pos_y};"


   
    # def Co_ordinate_Vertical_Calc(self, A1_X_Val, A1_Y_Val, J1_X_Val, J1_Y_Val, A8_X_Val, A8_Y_Val, m_val, n_val):
    #     x_offset = round(((A8_X_Val - A1_X_Val) / (m_val -1)), 2)
    #     y_offset = round(((J1_Y_Val - A1_Y_Val) / (n_val - 1)), 2)
    #     delta_x =  round(((J1_X_Val - A1_X_Val) / (n_val -1)), 3)
    #     delta_y = round(((A8_Y_Val - A1_Y_Val) / (m_val - 1)), 3)

    #     plasticus_box = [["" for _ in range(m_val)] for _ in range(n_val)]
    #     # print(f"delta_x  = {delta_x}, x_offset = {x_offset}, delta_y = {delta_y}, y_offset = {y_offset}")

    #     for n in range (n_val):
    #         for m in range (m_val):
    #             pos_x = abs(round((A1_X_Val + ((m) * x_offset) + ((n) * delta_x)), 2))
    #             pos_y = abs(round((A1_Y_Val + (n) * y_offset + (m) * delta_y), 2))
    #             plasticus_box[n][m] = f"G0X{pos_x}Y{pos_y};"
    #     return plasticus_box
    
