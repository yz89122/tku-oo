from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui

import sys


class StretchingLabel(QtWidgets.QLabel):
    def __init__(self, resize_ratio: float):
        super().__init__()
        self.resize_ratio = resize_ratio
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setFont(QtGui.QFont("Arial"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class StretchingButton(QtWidgets.QPushButton):
    def __init__(self, resize_ratio: float):
        super().__init__()
        self.resize_ratio = resize_ratio
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setFont(QtGui.QFont("Arial"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class AddWorkerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("Add worker")
        button = self.button_label()

        layout.addWidget(self.text_label, stretch=90)
        layout.addWidget(button, stretch=10)

        self.setLayout(layout)

    def button_label(self):
        button_label = StretchingButton(0.3)
        button_label.setText("Confirm to add worker")
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonA")
        button_label.setStyleSheet("QPushButton#ButtonA{background-color: black; color: white}")

        return button_label

    def post_service(self):
        self.text_label.setText("Click an addition")

    def init_screen(self):
        self.text_label.setText("Add Worker initialled")


class QueryWorkerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("Query Worker")
        button = self.button_label()

        layout.addWidget(self.text_label, stretch=90)
        layout.addWidget(button, stretch=10)

        self.setLayout(layout)

    def button_label(self):
        button_label = StretchingButton(0.3)
        button_label.setText("Confirm to query worker")
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonA")
        button_label.setStyleSheet("QPushButton#ButtonA{background-color: black; color: white}")

        return button_label

    def post_service(self):
        self.text_label.setText("Click a query")
    
    def init_screen(self):
        self.text_label.setText("Query Worker initialled")


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()

        self.widget_dict = dict()

        self.widget_dict['add_worker'] = self.addWidget(AddWorkerWidget())
        self.widget_dict['query_worker'] = self.addWidget(QueryWorkerWidget())

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.init_screen()


class DynamicWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()
        self.function_widget = FunctionWidget()
        self.function_widget.update_widget("add_worker")

        layout.addWidget(ControlMenu(self.function_widget), stretch=20)
        layout.addWidget(self.function_widget, stretch=80)

        self.setLayout(layout)


class ControlMenu(QtWidgets.QWidget):
    def __init__(self, function_widget):
        super().__init__()

        self.function_widget = function_widget

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button_label("add_worker"), stretch=20)
        layout.addWidget(self.button_label("query_worker"), stretch=20)
        self.setLayout(layout)
        
    def button_label(self, name):
        button_label = StretchingButton(0.1)
        button_label.setText(name)
        button_label.clicked.connect(lambda: self.function_widget.update_widget(name))
        button_label.setObjectName("button_{}".format(name))
        button_label.setStyleSheet("QPushButton#button_"+name+"{background-color: white; color: black}")

        return button_label


class MainWindow:
    def get_main_window(self):
        main_window = QtWidgets.QWidget()
        main_window.setObjectName("main_window")
        main_window.setStyleSheet("QWidget#main_window{{border-image: url(\"{}\")}};".format("base.png"))

        layout = QtWidgets.QVBoxLayout()
        header = self.text_showing_label(0.5)
        header.setText("Employee management system")

        dynamic_part = DynamicWidget()

        layout.addWidget(header, stretch=10)
        layout.addWidget(dynamic_part, stretch=90)

        main_window.setLayout(layout)
        return main_window

    @staticmethod
    def text_showing_label(ratio):
        text_label = StretchingLabel(resize_ratio=ratio)
        text_label.setAlignment(QtCore.Qt.AlignLeft)
        text_label.setStyleSheet("color: black;")
        return text_label


if __name__ == '__main__':

    app = QApplication([])
    main_window = MainWindow().get_main_window()

#    main_window.showFullScreen()
    main_window.show()
    sys.exit(app.exec_())
