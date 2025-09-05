class Styles:
    BACKGROUND = "background-color:qlineargradient(     x1:0, y1:0, x2:1, y2:1,     stop:0 #6BBCEB,     stop:1 #274472 ); "
    TITLE = "font-size: 38px; font-weight: bold; color: black; background: transparent;"
    COORD = "font-size: 26px; color: black; border: 0px solid red; background: transparent;"

    BUTTON = """
        QPushButton {
            background-color: white;
            color: black;
            font-size: 16px;
            border: none;
            padding: 2rem;
            border-top-left-radius:12px;
            border-top-right-radius:12px;            
        }
        QPushButton:hover {
            background-color: #5AAAD0;
        }
        QPushButton:pressed {
            background-color: #4A99BD;
        }
    """

    BUTTON_ROUNDED = """
        QPushButton {
            background-color: white;
            color: black;
            font-size: 16px;
            border: none;
            border-radius: 30px;
            padding: .4rem;
            outline:none;
        }
        QPushButton:pressed {
            background-color: #5AAAD0; 
        }
        
    """

    SLIDER = """
        QSlider::groove:vertical {
            background: #ddd;
            width: 12px;
            border-radius: 12px;
        }
        QSlider::handle:vertical {
            background: #6BBCEB;
            border: none;
            height: 20px;
            margin: 0 -2px;
            border-radius: 10px;
        }
    """


    INPUT = """
        QLineEdit {
            border: 0px solid #ccc;
            border-radius: 6px;
            font-size: 22px;
            color: black;
        }
    """
