import sys
from datetime import datetime
from PySide6 import QtWidgets

from widgets import LabeledInput, HistoryTable, LabeledBox


class ExpenseHistory(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.train_data = [[datetime(2008, 12, 10), 7.21, 'daafafa', 'comm1'],
                           [datetime(2012, 5, 22), 6661, 'da', ''],
                           [datetime(2018, 4, 12), 1516, 'afafafafa', 'riririririr'],
                           [datetime(2024, 10, 8), 0.12314, '123', '']]
        self.table = HistoryTable()
        self.table.set_data(self.train_data)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('History'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


class NewExpenseAdd(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comm_input = LabeledInput('Comment:', '')
        self.paid_input = LabeledInput('Paid:', '0')
        self.cat_list = LabeledBox('Category', ['1', '2', '3'])
        self.submit_button = QtWidgets.QPushButton('Add')
        self.submit_button.clicked.connect(self.submit)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(QtWidgets.QLabel('New expense'), 0, 0)
        self.layout.addWidget(self.cat_list, 1, 0)
        self.layout.addWidget(self.paid_input, 1, 1)
        self.layout.addWidget(self.comm_input, 2, 0)
        self.layout.addWidget(self.submit_button, 3, 1)
        self.setLayout(self.layout)

    def submit(self):
        print(self.cat_list.box.currentText(), self.paid_input.text(), self.comm_input.text())


class Expense(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        exp_hist = ExpenseHistory()
        new_exp = NewExpenseAdd()
        self.layout.addWidget(exp_hist)
        self.layout.addWidget(new_exp)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    window.setWindowTitle('Expense')
    window.resize(800, 600)

    central_widget = Expense()
    window.setCentralWidget(central_widget)

    window.show()
    sys.exit(app.exec())
