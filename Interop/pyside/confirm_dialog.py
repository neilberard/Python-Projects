from Interop.pyside import window_example_setup
import os

ui_file_name = os.path.dirname(__file__) + r'\basic_window.ui'


class ConfirmDialog(window_example_setup.MainWindow_UI_LOADER):
    def __init__(self):
        super(ConfirmDialog, self).__init__(ui_file_name)
