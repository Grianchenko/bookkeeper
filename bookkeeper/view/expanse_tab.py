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
    button_clicked = QtCore.Signal(int, str, str, datetime)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comm_input = LabeledInput('Comment:', '')
        self.paid_input = LabeledInput('Paid:', '0')
        self.cat_choice = LabeledBox('Category', ['1', '2', '3'])

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add)
        self.update_button = QtWidgets.QPushButton('Update')
        self.update_button.clicked.connect(self.update_exp)
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete)

        self.date_input = QtWidgets.QDateTimeEdit()
        self.date_input.setDateTime(QtCore.QDateTime.currentDateTime())

        self.main_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addWidget(QtWidgets.QLabel('New expense'))

        self.inputs_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.cat_choice, 0, 0)
        self.layout.addWidget(self.paid_input, 0, 1)
        self.layout.addWidget(self.date_input, 1, 1)
        self.layout.addWidget(self.comm_input, 1, 0)
        self.inputs_widget.setLayout(self.layout)
        self.main_layout.addWidget(self.inputs_widget)

        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.buttons_widget.setLayout(self.buttons_layout)
        self.main_layout.addWidget(self.buttons_widget)

        self.setLayout(self.main_layout)

    def submit(self, mode: str):
        try:
            self.button_clicked.emit(int(self.paid_input.text()),
                                     str(self.cat_choice.box.currentText()),
                                     str(self.comm_input.text()),
                                     str(datetime.strptime(self.date_input.text(),
                                                           '%d.%m.%Y %H:%M')))
            if mode == 'add':
                self.button_clicked.connect(print('Add-Expense-Click'))
            elif mode == 'delete':
                self.button_clicked.connect(print('Delete-Expense-Click'))
            elif mode == 'update':
                self.button_clicked.connect(print('Update-Expense-Click'))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')

    def add(self):
        self.submit('add')

    def delete(self):
        self.submit('delete')

    def update_exp(self):
        self.submit('update')


class Expense(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        exp_hist = ExpenseHistory()
        new_exp = NewExpenseAdd()
        self.layout.addWidget(exp_hist)
        self.layout.addWidget(new_exp)
        self.setLayout(self.layout)
