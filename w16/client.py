
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
        self.setFont(QtGui.QFont("微軟正黑體"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class StretchingButton(QtWidgets.QPushButton):
    def __init__(self, resize_ratio: float):
        super().__init__()
        self.resize_ratio = resize_ratio
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setFont(QtGui.QFont("微軟正黑體"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class StretchingTextBox(QtWidgets.QLineEdit):
    def __init__(self, resize_ratio: float):
        super().__init__()
        self.resize_ratio = resize_ratio
        self.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.setFont(QtGui.QFont("微軟正黑體"))

    def resizeEvent(self, *args, **kwargs):
        font = self.font()
        font.setPixelSize(self.height() * self.resize_ratio)
        self.setFont(font)


class StretchingLabelTextBox:
    def __init__(self, resize_ratio: float, label_text):
        self.layout = QtWidgets.QHBoxLayout()

        self.label = StretchingLabel(resize_ratio)
        self.label.setText(label_text)
        self.label.setFont(QtGui.QFont("微軟正黑體", 80, QtGui.QFont.Bold))
        self.layout.addWidget(self.label)

        self.textbox = StretchingTextBox(resize_ratio)
        self.textbox.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
        self.textbox.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")
        self.layout.addWidget(self.textbox)


class AddWorkerWidget(QtWidgets.QWidget):
    def __init__(self, main):
        super().__init__()

        self.main_window = main

        layout = QtWidgets.QVBoxLayout()

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
        button_label.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
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


class ListAllWidget(QtWidgets.QWidget):
    def __init__(self, main):
        super().__init__()

        self.main_window = main

        layout = QtWidgets.QVBoxLayout()

        button = self.create_list_button()

        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_list_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
        button_label.clicked.connect(self.delete)
        button_label.setObjectName("ButtonConfirm")
        button_label.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")

        return button_label

    def delete(self):
        result = str()
        for employee in self.main_window.request_handler.list_all():
            result += str(Employee.make_employee(employee)) + '\n'
        self.main_window.result_box.setPlainText(result)


class LookupWidget(QtWidgets.QWidget):
    def __init__(self, main):
        super().__init__()

        self.main_window = main

        layout = QtWidgets.QVBoxLayout()

        self.lt_id = StretchingLabelTextBox(1, 'id')
        button = self.create_list_button()

        layout.addLayout(self.lt_id.layout, stretch=20)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_list_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
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


class DeleteWidget(QtWidgets.QWidget):
    def __init__(self, main):
        super().__init__()

        self.main_window = main

        layout = QtWidgets.QVBoxLayout()

        self.lt_id = StretchingLabelTextBox(1, 'id')
        button = self.create_list_button()

        layout.addLayout(self.lt_id.layout, stretch=20)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_list_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
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


class MainWindow:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.request_handler = RequestHandler(self.host, self.port)

    def get_main_window(self):
        main_window = QtWidgets.QWidget()
        main_window.setObjectName("main_window")
        main_window.setStyleSheet("QWidget#main_window{{border-image: url(\"{}\")}};".format("base.png"))

        layout = QtWidgets.QVBoxLayout()
        header = self.create_header_label()

        tabs = QtWidgets.QTabWidget()

        add_worker = AddWorkerWidget(self)
        list_all = ListAllWidget(self)
        lookup = LookupWidget(self)
        delete = DeleteWidget(self)

        tabs.addTab(add_worker, 'add')
        tabs.addTab(list_all, 'list all')
        tabs.addTab(lookup, 'lookup')
        tabs.addTab(delete, 'delete')

        result_box = QtWidgets.QPlainTextEdit()
        self.result_box = result_box

        layout.addWidget(header, stretch=20)
        layout.addWidget(tabs, stretch=80)
        layout.addWidget(result_box, stretch=80)

        main_window.setLayout(layout)
        return main_window

    def create_header_label(self):
        header = StretchingLabel(0.4)
        header.setText("員工管理系統")
        header.setAlignment(QtCore.Qt.AlignLeft)
        header.setStyleSheet("color: blue;")

        return header


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow().get_main_window()

    main_window.show()
    sys.exit(app.exec_())
