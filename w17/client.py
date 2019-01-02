
from collections import defaultdict

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui

import sys
import json

from nio.client import RequestHandler
from employee import Employee


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


class StretchingTextBox(QtWidgets.QLineEdit):
    def __init__(self, resize_ratio: float):
        super().__init__()
        self.resize_ratio = resize_ratio
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setFont(QtGui.QFont("Arial"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class StretchingLabelTextBox:
    def __init__(self, resize_ratio: float, label_text):
        self.layout = QtWidgets.QHBoxLayout()

        self.label = StretchingLabel(resize_ratio)
        self.label.setText(label_text)
        self.label.setFont(QtGui.QFont("Arial", 80))
        self.layout.addWidget(self.label)

        self.textbox = StretchingTextBox(resize_ratio)
        self.textbox.setFont(QtGui.QFont("Arial", 20))
        self.textbox.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")
        self.layout.addWidget(self.textbox)


class AddWorkerWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("Add worker")
        layout.addWidget(self.text_label, stretch=90)

        button = self.create_addworker_button()
        self.lt_id = StretchingLabelTextBox(1, 'id')
        self.lt_name = StretchingLabelTextBox(1, 'name')
        type_group, self.rb_worker, self.rb_supervisor = self.create_worker_type_group()
        self.lt_ss = StretchingLabelTextBox(1, 'shift')
        self.lt_rb = StretchingLabelTextBox(1, 'rate')
        self.rb_worker.setChecked(True)
        self.is_worker = True

        layout.addLayout(self.lt_id.layout, stretch=20)
        layout.addLayout(self.lt_name.layout, stretch=20)
        layout.addWidget(type_group, stretch=20)
        layout.addLayout(self.lt_ss.layout, stretch=20)
        layout.addLayout(self.lt_rb.layout, stretch=20)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_addworker_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("Arial", 20))
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonConfirm")
        button_label.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")

        return button_label

    def create_worker_type_group(self):
        layout = QtWidgets.QHBoxLayout()
        r_w = QtWidgets.QRadioButton('worker')
        r_s = QtWidgets.QRadioButton('supervisor')
        layout.addWidget(r_w)
        layout.addWidget(r_s)
        r_w.clicked.connect(self.set_worker)
        r_s.clicked.connect(self.set_supvisor)
        group = QtWidgets.QGroupBox()
        group.setLayout(layout)
        return group, r_w, r_s

    def set_worker(self):
        self.lt_ss.label.setText('shift')
        self.lt_rb.label.setText('rate')
        self.is_worker = True

    def set_supvisor(self):
        self.lt_ss.label.setText('salary')
        self.lt_rb.label.setText('bonus')
        self.is_worker = False


    def button_label(self):
        button_label = StretchingButton(0.3)
        button_label.setText("Confirm to add worker")
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonA")
        button_label.setStyleSheet("QPushButton#ButtonA{background-color: black; color: white}")

        return button_label

    def init_screen(self):
        self.text_label.setText("Add Worker initialled")

    def post_service(self):
        if self.main_window.request_handler.check_existence(self.lt_id.textbox.text()):
            self.main_window.result_box.setPlainText('already exist')
        else:
            employee = Employee.make_employee({
                'id': self.lt_id.textbox.text(),
                'name': self.lt_name.textbox.text(),
                'type': 'worker' if self.is_worker else 'supervisor',
                'shift' if self.is_worker else 'salary': self.lt_ss.textbox.text(),
                'rate' if self.is_worker else 'bonus': self.lt_rb.textbox.text()
            })
            if self.main_window.request_handler.add_employee(employee):
                self.main_window.result_box.setPlainText('OK')
            else:
                self.main_window.result_box.setPlainText('Failed')


class QueryWorkerWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("Query Worker")
        button = self.button_label()
        button.clicked.connect(self.list_all)

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
        # self.main_dinw
    
    def list_all(self):
        result = str()
        for employee in self.main_window.request_handler.list_all():
            result += str(Employee.make_employee(employee)) + '\n'
        self.main_window.result_box.setPlainText(result)


class LookupWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("lookup Worker")

        self.setLayout(layout)
        self.lt_id = StretchingLabelTextBox(1, 'id')
        button = self.create_lookup_button()

        layout.addWidget(self.text_label, stretch=90)
        layout.addLayout(self.lt_id.layout, stretch=20)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_lookup_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20))
        button_label.clicked.connect(self.lookup)
        button_label.setObjectName("ButtonConfirm")
        button_label.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")

        return button_label

    def lookup(self):
        employee_id = self.lt_id.textbox.text()
        if employee_id is None or employee_id == '':
            self.main_window.result_box.setPlainText("Please enter an ID")
        elif not self.main_window.request_handler.check_existence(employee_id):
            self.main_window.result_box.setPlainText("not exist")
        else:
            self.main_window.result_box.setPlainText(str(
                self.main_window.request_handler.get_by_id(employee_id)
            ))

    def button_label(self):
        button_label = StretchingButton(0.3)
        button_label.setText("Confirm to lookup worker")
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonA")
        button_label.setStyleSheet("QPushButton#ButtonA{background-color: black; color: white}")

        return button_label

    def post_service(self):
        self.text_label.setText("Click a query")
    
    def init_screen(self):
        self.text_label.setText("lookup Worker initialled")


class DeleteWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QtWidgets.QVBoxLayout()

        self.text_label = MainWindow.text_showing_label(0.1)
        self.text_label.setText("delete Worker")
        layout.addWidget(self.text_label, stretch=90)

        self.lt_id = StretchingLabelTextBox(1, 'id')
        button = self.create_list_button()

        layout.addLayout(self.lt_id.layout, stretch=20)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def button_label(self):
        button_label = StretchingButton(0.3)
        button_label.setText("Confirm to delete worker")
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonA")
        button_label.setStyleSheet("QPushButton#ButtonA{background-color: black; color: white}")

        return button_label

    def post_service(self):
        self.text_label.setText("Click a query")
    
    def init_screen(self):
        self.text_label.setText("delete Worker initialled")

    def create_list_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20))
        button_label.clicked.connect(self.delete)
        button_label.setObjectName("ButtonConfirm")
        button_label.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")

        return button_label

    def delete(self):
        employee_id = self.lt_id.textbox.text()
        if employee_id is None or employee_id == '':
            self.main_window.result_box.setPlainText("Please enter an ID")
        elif not self.main_window.request_handler.check_existence(employee_id):
            self.main_window.result_box.setPlainText("not exist")
        else:
            self.main_window.request_handler.delete_employee(employee_id)
            self.main_window.result_box.setPlainText("OK!")


class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.widget_dict = dict()

        self.widget_dict['add_worker'] = self.addWidget(AddWorkerWidget(self.main_window))
        self.widget_dict['query_worker'] = self.addWidget(QueryWorkerWidget(self.main_window))
        self.widget_dict['lookup'] = self.addWidget(LookupWidget(self.main_window))
        self.widget_dict['delete'] = self.addWidget(DeleteWidget(self.main_window))

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.init_screen()


class DynamicWidget(QtWidgets.QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        layout = QtWidgets.QHBoxLayout()
        self.function_widget = FunctionWidget(self.main_window)
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
        layout.addWidget(self.button_label("lookup"), stretch=20)
        layout.addWidget(self.button_label("delete"), stretch=20)
        self.setLayout(layout)
        
    def button_label(self, name):
        button_label = StretchingButton(0.1)
        button_label.setText(name)
        button_label.clicked.connect(lambda: self.function_widget.update_widget(name))
        button_label.setObjectName("button_{}".format(name))
        button_label.setStyleSheet("QPushButton#button_"+name+"{background-color: white; color: black}")

        return button_label


class MainWindow:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.request_handler = RequestHandler(self.host, self.port)

    def get_main_window(self):
        main_window = QtWidgets.QWidget()
        main_window.setObjectName("main_window")
        main_window.setStyleSheet("QWidget#main_window{{border-image: url(\"{}\")}};".format("base.png"))

        result_box = QtWidgets.QPlainTextEdit()
        self.result_box = result_box

        layout = QtWidgets.QVBoxLayout()
        header = self.text_showing_label(0.5)
        header.setText("Employee management system")

        dynamic_part = DynamicWidget(self)

        layout.addWidget(header, stretch=10)
        layout.addWidget(dynamic_part, stretch=90)
        layout.addWidget(result_box, stretch=20)

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

    main_window.show()
    sys.exit(app.exec_())
