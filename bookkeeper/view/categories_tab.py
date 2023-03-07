from datetime import datetime
from PySide6 import QtWidgets, QtCore

from simple_widgets import LabeledInput, HistoryTable, LabeledBox


class CategoriesExists(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columns = ('Category', 'Parent')
        self.train_data = [['1241.41241', '5000'],
                           ['4332.111', '15000'],
                           ['6156.12', '50000']]
        self.table = HistoryTable(columns=self.columns)

        self.table.set_data(self.train_data)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Categories'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class NewCategory(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(str, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_input = LabeledInput('Category name', '')
        self.parent_input = LabeledInput('Parent (if needed)', '')

        self.submit_button = QtWidgets.QPushButton('Add')
        self.submit_button.clicked.connect(self.submit)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('New category'))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.parent_input)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def submit(self):
        try:
            self.button_clicked.emit(str(self.name_input.text()), str(self.parent_input.text()))
            self.button_clicked.connect(print('Category-Click'))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')


class Categories(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        act_cat = CategoriesExists()
        new_cat = NewCategory()
        self.layout.addWidget(act_cat)
        self.layout.addWidget(new_cat)
        self.setLayout(self.layout)
