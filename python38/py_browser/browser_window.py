from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Signal
import abc
import os
import sys
import json
import logging
logging.basicConfig()
log = logging.getLogger(__name__)



SETTINGS_PATH = os.path.join(os.environ['APPDATA'], "File")
TEST_PATH = 'C:/Users/Neil/Desktop'
MAIN_WINDOW = None


DOCK_WIDGET_VIEW_MODE = "Dock Widgets"
TAB_VIEW_MODE = "Tabs"


ACTIVE_STYLE = "QWidget { background-color: rgba(255, 255, 255, 128);}"
INACTIVE_STYLE = "QWidget { background-color: rgba(128, 128, 128, 50);}"


class AbstractDockWindow:
    @abc.abstractmethod
    def add_widget(self, browser_window, path=None):
        pass

    @abc.abstractmethod
    def populate(self):
        pass

    @abc.abstractmethod
    def clear_widgets(self):
        pass

    @abc.abstractmethod
    def remove_widget(self, *args):
        pass

    @abc.abstractmethod
    def get_active(self, *args):
        pass

    @abc.abstractmethod
    def set_active(self, *args):
        pass


class TabWindow(AbstractDockWindow, QtWidgets.QTabWidget):

    def __init__(self):
        super().__init__()

        self.dir_path = ""

        self.setAcceptDrops(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.set_active)

    def add_widget(self, browser_window, path=None):
        self.addTab(browser_window, browser_window._leaf)
        self.setCurrentWidget(browser_window)
        MainWindow().set_active_browser(browser_window)

    def populate(self):
        for w in MainWindow().get_browser_list():
            self.add_widget(w)

    def remove_widget(self, widget):
        self.removeTab(self.indexOf(widget))

    def close_tab(self, *args):
        MainWindow().remove_browser(self.widget(args[0]))

    def clear_widgets(self):
        self.clear()

    def mouseMoveEvent(self, event):
        print("Move! {}".format(self.currentWidget().file_system_model.rootPath()))

    def dragEnterEvent(self, event):
        print("Drag!")

    def set_active(self, *args):
        MainWindow().set_active_browser(self.currentWidget())

    def get_active(self, *args):
        pass


class DockWindow(AbstractDockWindow, QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.splitter = QtWidgets.QSplitter()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.splitter)
        self._active = None

    def add_widget(self, browser_window, path=None):
        dock_widget = DockWidget(browser_window)
        dock_widget.closed_event.connect(MainWindow().remove_browser)
        self.splitter.addWidget(dock_widget)

    def remove_widget(self, dock_widget):
        MainWindow().remove_browser(dock_widget)

    def populate(self):
        for w in MainWindow().get_browser_list():
            self.add_widget(w)

    def clear_widgets(self):
        for dock in self.findChildren(DockWidget):
            dock.release_browser()

    def get_active(self, *args):
        return self._active

    def set_active(self, *args):
        pass


class DockWidget(QtWidgets.QDockWidget):
    closed_event = Signal(QtWidgets.QDockWidget)

    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window
        self.setWidget(browser_window)
        self.setWindowTitle(browser_window._leaf)

    def closeEvent(self, event):
        self.browser_window.setParent(None)
        self.hide()
        self.setParent(None)
        self.setWidget(None)
        self.closed_event.emit(self.browser_window)
        super().closeEvent(event)

    def release_browser(self):
        self.browser_window.setParent(None)
        self.setWidget(None)
        self.deleteLater()

class PinListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

        self.menu = QtWidgets.QMenu()
        self.menu_go_back = self.menu.addAction("Go Back")
        self.menu_copy_path = self.menu.addAction("Copy Path")
        self.menu_pin_item = self.menu.addAction("Pin Item")

    def mouseDoubleClickEvent(self, event):
        print("double click")
        self.open()

    def open(self):
        MainWindow().get_active_browser().set_path(self.currentItem().path, is_dir=True)

    def dragEnterEvent(self, event):

        mime = event.mimeData()
        print("Dragging! {}".format(type(self).__name__))
        event.accept()

    def dropEvent(self, event):
        print("Dropped! {}".format(type(self).__name__))
        print(event.pos())
        print(event.mimeData().text())
        self.add_pin(event.mimeData().text())

    def add_pin(self, path):
        print("adding pin {}".format(path))
        new_pin = FileItemWidget(path)
        self.addItem(new_pin)


class FileListWidget(QtWidgets.QListWidget):

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.directory = ""
        self.icon_provider = QtWidgets.QFileIconProvider()

    def set_root_directory(self, directory):
        self.clear()
        self.directory = directory
        items = os.listdir(directory)

        for path in items:
            full_path = os.path.join(directory, path)
            item_widget = FileItemWidget(full_path)
            self.addItem(item_widget)

    def dragEnterEvent(self, event):
        item = MainWindow.get_active_browser()
        assert isinstance(item, FileItemWidget)
        print(item.file_path())
        return

        print("Dragging! {}".format(type(self).__name__))
        event.mimeData().setText(item.file_path())
        print(event.mimeData().text())
        event.accept()

    def dropEvent(self, event):
        print("Dropped! {}".format(type(self).__name__))
        print(event.pos())
        print(event.mimeData().text())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        MainWindow().set_active_browser(self.parent())

class PathLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)

    # def dragEnterEvent(self, event):
    #     print("Dragging! {}".format(type(self).__name__))


class FileItemWidget(QtWidgets.QListWidgetItem):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.file_name = os.path.split(path)[-1]
        self._full_path = path

        self.fileInfo = QtCore.QFileInfo(path)
        self.setText(self.fileInfo.fileName())
        icon_provider = QtWidgets.QFileIconProvider()
        icon = icon_provider.icon(self.fileInfo)
        self.setIcon(icon)

    def file_path(self):
        return self._full_path
        pass


class MainWindow(QtWidgets.QMainWindow):
    """
    Singleton Class
    """
    _instance = None
    _initialized = False

    # Context for the browser widgets, can be tabs or dock widgets.
    _browser_context = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self):
        if self._initialized:
            return
        super().__init__()

        # Style
        self.setStyleSheet("QGroupBox {border: 0px}")

        self._browser_widgets_list = []
        self._active = None

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        self.c_layout = self.centralWidget().layout()

        # Tab Widget
        self.tab_widget = TabWindow()
        self.tab_widget.hide()


        # Dock Widget
        self.dock_widget = DockWindow()
        self.dock_widget.hide()

        # Initial Context
        self._browser_context = self.dock_widget

        # Tool Bar
        self.tool_bar = QtWidgets.QGroupBox()
        self.tool_bar.setLayout(QtWidgets.QHBoxLayout())
        self.c_layout.addWidget(self.tool_bar)

        # Back Button
        self.back_btn = QtWidgets.QPushButton("<-")
        self.back_btn.setMaximumWidth(100)
        self.tool_bar.layout().addWidget(self.back_btn)

        # View Mode
        self.browser_context_combo = QtWidgets.QComboBox()
        self.browser_context_combo.addItem(DOCK_WIDGET_VIEW_MODE)
        self.browser_context_combo.addItem(TAB_VIEW_MODE)
        self.tool_bar.layout().addWidget(self.browser_context_combo)

        # Open Tab
        self.open_tab_btn = QtWidgets.QPushButton("Open Tab +")
        self.tool_bar.layout().addWidget(self.open_tab_btn)

        self.lower_grp = QtWidgets.QGroupBox()
        self.c_layout.addWidget(self.lower_grp)
        self.lower_grp.setLayout(QtWidgets.QHBoxLayout())
        self.lower_grp.layout().setMargin(2)
        self.lower_grp.layout().setSpacing(0)


        # Fav Widget
        self.fav_grp = QtWidgets.QGroupBox()
        self.fav_grp.setLayout(QtWidgets.QVBoxLayout())
        self.fav_combo = QtWidgets.QComboBox()

        self.fav_list = PinListWidget()
        self.fav_list.setMaximumWidth(200)
        self.lower_grp.layout().addWidget(self.fav_list)
        self.lower_grp.layout().addWidget(self.tab_widget)
        self.lower_grp.layout().addWidget(self.dock_widget)

        # Signals
        self.back_btn.clicked.connect(self.go_back)
        self.open_tab_btn.clicked.connect(self.add_browser)
        self.browser_context_combo.currentIndexChanged.connect(self.set_view_mode)


        # init
        self._initialized = True

    def set_view_mode(self):
        if self._browser_context:
            self._browser_context.clear_widgets()
            self._browser_context.hide()

        if self.browser_context_combo.currentText() == DOCK_WIDGET_VIEW_MODE:
            self._browser_context = self.dock_widget
        elif self.browser_context_combo.currentText() == TAB_VIEW_MODE:
            self._browser_context = self.tab_widget

        self._browser_context.show()
        self._browser_context.populate()

        for w in self._browser_widgets_list:
            w.show()
            print(w.parent())



    def add_browser(self, path=TEST_PATH):
        browser_window = BrowserWidget(path)
        browser_window.set_path(TEST_PATH, is_dir=True)
        self._browser_widgets_list.append(browser_window)
        self._browser_context.add_widget(browser_window)
        self.set_active_browser(browser_window)

    def remove_browser(self, browser_widget):
        print("Removing widget {}".format(id(browser_widget)))
        if browser_widget in self._browser_widgets_list:
            print("Removing widget {}")
            self._browser_widgets_list.remove(browser_widget)
            self._browser_context.remove_widget(browser_widget)
        if self._active == browser_widget:
            if self._browser_widgets_list:
                self.set_active_browser(self._browser_widgets_list[0])
            else:
                self.set_active_browser(None)


    def go_back(self):
        self._active.back()

    def get_browser_list(self):
        return self._browser_widgets_list

    def get_active_browser(self):
        return self._active

    def set_active_browser(self, browser):
        for w in self._browser_widgets_list:
            w.setStyleSheet(INACTIVE_STYLE)
        self._active = browser
        if browser:
            browser.setStyleSheet(ACTIVE_STYLE)


class BrowserWidget(QtWidgets.QWidget):

    def __init__(self, path=None):
        super().__init__()

        # Data
        self._leaf = ""
        self._full_path = ""

        self._active = False
        self.history = []
        self.setWindowTitle("Browser")
        self.central_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.central_layout)

        # BROWSER PATH
        self.path_line_edit = PathLineEdit()
        self.central_layout.addWidget(self.path_line_edit)
        self.list_view = FileListWidget()
        self.central_layout.addWidget(self.list_view)
        #
        # self.file_system_model = QtWidgets.QFileSystemModel()
        # self.list_view.setModel(self.file_system_model)

        # LIST VIEW
        self.list_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.context_menu)
        self.list_view.doubleClicked.connect(self.mouseDoubleClickEvent)
        self.list_view.clicked.connect(self.mousePressEvent)

        # CONTEXT MENU
        self.menu = QtWidgets.QMenu()
        self.menu_go_back = self.menu.addAction("Go Back")
        self.menu_go_back.triggered.connect(self.back)
        self.menu_copy_path = self.menu.addAction("Copy Path")
        self.menu_pin_item = self.menu.addAction("Pin Item")
        self.menu_pin_item.triggered.connect(self.pin_item)

        # SIGNAL
        self.path_line_edit.textEdited.connect(self.set_path_edit)

        if path:
            self.set_path(path, is_dir=os.path.isdir(path))

    def set_path_edit(self):
        path = self.path_line_edit.text()
        if os.path.isdir(self.path_line_edit.text()):
            self.set_path(path, is_dir=True, set_text=False)

    def set_path(self, path, is_dir=False, history=True, set_text=True):
        self._leaf = os.path.split(path)[-1]

        if is_dir:
            self.list_view.set_root_directory(path)
            if set_text:
                self.path_line_edit.setText(path)
            if history:
                self.history.append(path)
            if self.parent():
                print(type(self.parent()).__name__)
                self.parent().setWindowTitle(self._leaf)
                self.parent().setTitle(self._leaf)

    def dragEnterEvent(self, event):
        print("Dragging! {}".format(type(self).__name__))
        event.mimeData().setText("Test")
        print(event.mimeData().text())

        event.accept()

    def dropEvent(self, event):
        print("Dropped! {}".format(type(self).__name__))
        event.accept()

    def mousePressEvent(self, event):
        self.set_active(True)

    def context_menu(self):
        cursor = QtGui.QCursor()
        self.menu.exec_(cursor.pos())

    def back(self):
        print(self.history)
        if len(self.history) > 1:
            self.history.pop(-1)
            self.set_path(self.history[-1], is_dir=True, history=False)

    def pin_item(self):
        item = self.list_view.currentItem()
        MainWindow().fav_list.add_pin(item.file_path())

    def set_dir(self):
        item = self.list_view.currentItem()
        self.set_path(item.file_path(), is_dir=item.fileInfo.isDir())

    def mouseDoubleClickEvent(self, event):
        print("double click Yarbble")
        self.set_dir()
        self.set_active(True)


    def set_active(self, active:bool):
        MainWindow().set_active_browser(self)

    def mouseMoveEvent(self, event):
        print("Move!")


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 500)

    window.setWindowTitle('File Browser')
    window.show()
    window.set_view_mode()
    window.add_browser(TEST_PATH)


    sys.exit(app.exec_())
    pass