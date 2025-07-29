from PyQt5.QtWidgets import QMainWindow,QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.showFullScreen()
        self.current_screen = None
        
        # Default Screen
        self.router("home")

#         self.setStyleSheet("""
#     QWidget {
#         background: qlineargradient(
#             spread:pad,
#             x1:0, y1:0,
#             x2:1, y2:1,
#             stop:0 #0f2a44,
#             stop:1 #1a4d7a
#         );
#     }
# """)
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 #3c7cb2,    /* Light blue that complements 'primary' */
            stop:1 #6baed6     /* Even lighter tone for smooth transition */
        );
    }
""")



    
    def router(self, screen_name : str):
        if self.current_screen:
            self.current_screen.setParent(None)
            self.current_screen.deleteLater()
            self.current_screen = None
        
        if screen_name == "home":
            from screens.home import HomeScreen
            self.current_screen = HomeScreen(self)
        elif screen_name == "single_pipette_asp":
            from screens.single_pipette_asp import SinglePipetteAsp
            self.current_screen = SinglePipetteAsp(self)
        elif screen_name == "multi_pipette_asp":
            from screens.multi_pipette_asp import MultiPipetteAsp
            self.current_screen = MultiPipetteAsp(self)
        
        self.setCentralWidget(self.current_screen)