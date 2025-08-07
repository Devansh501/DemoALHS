from PyQt5.QtWidgets import QMainWindow,QPushButton
from pathlib import Path
from resources import resources

def load_stylesheet(filename):
    base_path = Path(__file__).resolve().parent
    qss_path = base_path / "styles" / filename
    return qss_path.read_text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        # load qss stylesheets
        stylesheet = load_stylesheet("globals.qss")
        self.setStyleSheet(stylesheet)
        
        self.showFullScreen()
        self.current_screen = None
        
        # Default Screen
        self.router("home")




    
    def router(self, screen_name : str):
        if self.current_screen:
            self.current_screen.setParent(None)
            self.current_screen.deleteLater()
            self.current_screen = None
        
        if screen_name == "home":
            from screens.home import HomeScreen
            self.current_screen = HomeScreen(self)
        
        
        self.setCentralWidget(self.current_screen)