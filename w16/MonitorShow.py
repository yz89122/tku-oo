from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui

import sys
# import requests
import json


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


class AddWorkerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout()

        text_label = self.create_addworker_label()
        button = self.create_addworker_button()

        layout.addWidget(text_label, stretch=80)
        layout.addWidget(button, stretch=20)

        self.setLayout(layout)

    def create_addworker_label(self):
        addworker_label = StretchingLabel(0.2)
        addworker_label.setText("新增員工")
        return addworker_label

    def create_addworker_button(self):
        button_label = StretchingButton(0.5)
        button_label.setText("確認")
        button_label.setFont(QtGui.QFont("微軟正黑體", 20, QtGui.QFont.Bold))
        button_label.clicked.connect(self.post_service)
        button_label.setObjectName("ButtonConfirm")
        button_label.setStyleSheet("QPushButton#ButtonConfirm{background-color: black; color: white}")

        return button_label

    def post_service(self):
        response = requests.post(
            url="http://127.0.0.1:9000/add_worker",
            data={
                "worker_id": 99,
                "worker_name": "Kevin"
            },
            verify=False
        )

        if (response.status_code == requests.codes.ok):
            response_json = json.loads(response.text)
            self.text_label.setText(response_json["status"])
        else:
            self.text_label.setText("Fail")


class MainWindow:
    def __init__(self):
        pass

    def get_main_window(self):
        main_window = QtWidgets.QWidget()
        main_window.setObjectName("main_window")
        main_window.setStyleSheet("QWidget#main_window{{border-image: url(\"{}\")}};".format("base.png"))

        layout = QtWidgets.QVBoxLayout()
        header = self.create_header_label()

        dynamic_part = AddWorkerWidget()

        layout.addWidget(header, stretch=20)
        layout.addWidget(dynamic_part, stretch=80)

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

#    main_window.showFullScreen()
    main_window.show()
    sys.exit(app.exec_())
