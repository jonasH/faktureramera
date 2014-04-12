from PyQt5.QtWidgets  import  QWidget, QMainWindow
from gui.ui_jobform import Ui_jobForm

class JobForm(QWidget):
    
    def __init__(self,  parent=None):
        """"""
        super(JobForm, self).__init__(parent)
        
        self.ui = Ui_jobForm()
        
        self.ui.setupUi(self)
