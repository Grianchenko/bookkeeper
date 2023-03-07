from datetime import datetime
from PySide6 import QtWidgets, QtCore

from simple_widgets import LabeledInput, HistoryTable, LabeledBox


class ExpenseHistory(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columns = ('Date', 'Paid', 'Category', 'Comment')
        self.train_data = [[datetime(2008, 12, 10), 7.21, 'daafafa', 'comm1'],
                           [datetime(2012, 5, 22), 6661, 'da', ''],
                           [datetime(2018, 4, 12), 1516, 'afafafafa', 'riririririr'],
                           [datetime(2024, 10, 8), 0.12314, '123', '']]
        self.table = HistoryTable(columns=self.columns)
        self.table.set_data(self.train_data)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('History'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class NewExpenseAdd(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(int, str, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comm_input = LabeledInput('Comment:', '')
        self.paid_input = LabeledInput('Paid:', '0')
        self.cat_choice = LabeledBox('Category', ['1', '2', '3'])
        self.submit_button = QtWidgets.QPushButton('Add')
        self.submit_button.clicked.connect(self.submit)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(QtWidgets.QLabel('New expense'), 0, 0)
        self.layout.addWidget(self.cat_choice, 1, 0)
        self.layout.addWidget(self.paid_input, 1, 1)
        self.layout.addWidget(self.comm_input, 2, 0)
        self.layout.addWidget(self.submit_button, 3, 1)
        self.setLayout(self.layout)

    def submit(self):
        try:
            self.button_clicked.emit(int(self.paid_input.text()), str(self.cat_choice.box.currentText()),
                                     str(self.comm_input.text()))
            self.button_clicked.connect(print('Expense-Click'))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')


class Expense(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        exp_hist = ExpenseHistory()
        new_exp = NewExpenseAdd()
        self.layout.addWidget(exp_hist)
        self.layout.addWidget(new_exp)
        self.setLayout(self.layout)
