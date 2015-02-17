from PyQt5.QtWidgets import QWidget
from gui.ui_newcustomerform import Ui_NewCustomerForm


class NewCustomerForm(QWidget):
    
    def __init__(self,  parent=None):
        """"""
        super(NewCustomerForm, self).__init__(parent)
        
        self.ui = Ui_NewCustomerForm()
        
        self.ui.setupUi(self)
