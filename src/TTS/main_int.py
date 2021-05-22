import sys
from PyQt5.QtWidgets import QApplication
from ui.app import *


app = QApplication(sys.argv)
window = App()
window.show()
app.exec()
