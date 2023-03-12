from datetime import datetime
from PySide6 import QtWidgets, QtCore

from bookkeeper.view.utils import LabeledInput, HistoryTable, LabeledBox
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense


class ExpenseHistory(QtWidgets.QWidget):
    def __init__(self, exp_repo: AbstractRepository, cat_repo: AbstractRepository,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.columns = ('Date', 'Paid', 'Category', 'Comment')
        self.table = HistoryTable(columns=self.columns)
        self.data = []
        self.set_data()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('History'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def set_data(self) -> None:
        self.data = []
        got_all = self.exp_repo.get_all()
        if got_all:
            for exp in got_all[::-1]:
                temp = [exp.expense_date, exp.amount,
                        self.cat_repo.get(int(exp.category)).name, exp.comment]
                self.data.append(temp)
        self.table.set_data(self.data)


class ExpenseManager(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(int, str, str, datetime)

    def __init__(self, exp_repo: AbstractRepository, cat_repo: AbstractRepository,
                 exp_hist: ExpenseHistory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_hist = exp_hist
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.cat_list = []
        self.comm_input = LabeledInput('Comment:', '')
        self.paid_input = LabeledInput('Paid:', '0')
        self.cat_choice = LabeledBox('Category', self.cat_list)
        self.set_cat_list()

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

    def set_cat_list(self):
        self.cat_list = [cat.name.capitalize() for
                         cat in self.cat_repo.get_all()]
        self.cat_choice.box.clear()
        self.cat_choice.box.addItems(self.cat_list)

    def submit(self, mode: str) -> None:
        try:
            self.button_clicked.emit(int(self.paid_input.input.text()),
                                     str(self.cat_choice.box.currentText()),
                                     str(self.comm_input.input.text()),
                                     str(datetime.strptime(self.date_input.text(),
                                                           '%d.%m.%Y %H:%M')))
            if True:
                self.button_clicked.connect(self.edit_expense(mode,
                                                              int(self.paid_input.input.text()),
                                                              self.cat_choice.box.
                                                              currentText(),
                                                              self.comm_input.input.text(),
                                                              datetime.strptime
                                                              (self.date_input.text(),
                                                               '%d.%m.%Y %H:%M')))
            self.button_clicked.connect(self.exp_hist.set_data())
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')

    def edit_expense(self, mode: str, amount: int,
                     cat: str, comm: str, date: datetime) -> None:
        cat_pk = self.cat_to_pk(cat)
        exp = Expense(amount, cat_pk, expense_date=date, comment=comm)
        if mode == 'add':
            self.exp_repo.add(exp)
        elif mode == 'delete':
            exp_pk = self.exp_repo.get_all({'amount': amount,
                                            'category': cat_pk,
                                            'expense_date': str(date)})[0].pk
            self.exp_repo.delete(exp_pk)
        elif mode == 'update':
            exp_pk = self.exp_repo.get_all({'comment': comm,
                                            'expense_date': str(date)})[0].pk
            exp = Expense(int(amount), cat_pk, expense_date=date,
                          comment=comm, pk=exp_pk)
            print(exp)
            self.exp_repo.update(exp)

    def cat_to_pk(self, cat) -> int:
        return self.cat_repo.get_all({'name': cat.lower()})[0].pk

    def add(self) -> None:
        self.submit('add')

    def delete(self) -> None:
        self.submit('delete')

    def update_exp(self) -> None:
        self.submit('update')


class ExpenseTab(QtWidgets.QWidget):
    def __init__(self, exp_repo: AbstractRepository, cat_repo: AbstractRepository,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.layout = QtWidgets.QVBoxLayout()
        self.exp_hist = ExpenseHistory(self.exp_repo, self.cat_repo)
        self.new_exp = ExpenseManager(self.exp_repo, self.cat_repo, self.exp_hist)
        self.layout.addWidget(self.exp_hist)
        self.layout.addWidget(self.new_exp)
        self.setLayout(self.layout)
