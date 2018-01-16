from Interop.pyside import basic_window
import os

ui_file_name = os.path.dirname(__file__) + r'\basic_window.ui'


class ConfirmDialog(basic_window.BaseWindow):
    def __init__(self):
        super(ConfirmDialog, self).__init__(ui_file_name)
