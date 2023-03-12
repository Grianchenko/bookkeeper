from datetime import datetime, timedelta, date
from PySide6 import QtWidgets, QtCore

from bookkeeper.view.utils import LabeledInput, HistoryTable, LabeledBox
from bookkeeper.repository.sqlite_repository import AbstractRepository
from bookkeeper.models.budget import Budget


def start_date(days_ago):
    if days_ago == 7:
        return datetime.strptime(str(date.today() -
                                     timedelta(days=datetime.weekday(
                                         date.today()))), '%Y-%m-%d')
    elif days_ago == 1:
        return datetime.strptime(str(datetime.today().date()), '%Y-%m-%d')
    elif days_ago in [28, 29, 30, 31]:
        return datetime.strptime(str(date.today() -
                                     timedelta(days=int(datetime.strftime(
                                         datetime.now(), '%d'))-1)),
                                 '%Y-%m-%d')


class ActiveBudgets(QtWidgets.QWidget):
    def __init__(self, exp_repo: AbstractRepository,
                 bud_repo: AbstractRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo
        self.rows = ('Day', 'Week', 'Month')
        self.columns = ('Paid', 'Limit')

        self.data = []
        self.table = HistoryTable(self.rows, self.columns)
        self.set_data()
        if self.data[0][0] > self.data[0][1] or \
                self.data[1][0] > self.data[1][1] or \
                self.data[2][0] > self.data[2][1]:
            QtWidgets.QMessageBox.critical(self, "You'll be poor!",
                                           'You shouldn\'t spend that much!!!')

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Budgets'))
        self.layout.addWidget(QtWidgets.QLabel('Today:\n' +
                                               str(date.today()) + ', ' +
                                               str(datetime.weekday(
                                                   datetime.now())) +
                                               'th day of week'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(500, self)

    def timerEvent(self, event):
        self.set_data()

    @QtCore.Slot()
    def set_data(self) -> None:
        data_bud = []
        for i in [1, 7, 30]:
            data_bud.append(self.bud_repo.get_all({'length': i})[::-1][0].amount)
        got_exp = self.exp_repo.get_all()[::-1]
        d, w, m = 0, 0, 0
        for exp in got_exp:
            exp_date = datetime.strptime(exp.expense_date, '%Y-%m-%d %H:%M:%S')
            if exp_date >= start_date(1):
                m += exp.amount
                d += exp.amount
                w += exp.amount
            elif exp_date >= start_date(7):
                m += exp.amount
                w += exp.amount
            elif exp_date >= start_date(30):
                m += exp.amount
        self.data = [[d, data_bud[0]],
                     [w, data_bud[1]],
                     [m, data_bud[2]]]

        self.table.set_data(self.data)


class BudgetManager(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(str, int)

    def __init__(self, bud_repo: AbstractRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bud_repo = bud_repo
        self.length_choice = LabeledBox('Category', ['day', 'week', 'month'])
        self.limit_input = LabeledInput('New budget', '1000')
        self.submit_button = QtWidgets.QPushButton('Update')
        self.submit_button.clicked.connect(self.submit)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Budget manager'))
        self.layout.addWidget(self.length_choice)
        self.layout.addWidget(self.limit_input)
        self.layout.addWidget(self.submit_button)
        self.setLayout(self.layout)

    def submit(self) -> None:
        try:
            self.button_clicked.emit(str(self.length_choice.box.currentText()),
                                     int(self.limit_input.input.text()))
            self.button_clicked.connect(self.new_budget(str(
                self.length_choice.box.currentText()),
                int(self.limit_input.input.text())))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')

    def new_budget(self, duration: str, limit: int) -> None:
        dur = 7
        if duration == 'day':
            dur = 1
        elif duration == 'week':
            dur = 7
        elif duration == 'month':
            dur = 30
        bud = Budget(limit, length=dur, start_date=start_date(dur))
        self.bud_repo.add(bud)


class BudgetTab(QtWidgets.QWidget):
    def __init__(self, exp_repo: AbstractRepository,
                 bud_repo: AbstractRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo
        self.layout = QtWidgets.QVBoxLayout()
        self.act_bud = ActiveBudgets(self.exp_repo, self.bud_repo)
        self.edit_bud = BudgetManager(self.bud_repo)
        self.layout.addWidget(self.act_bud)
        self.layout.addWidget(self.edit_bud)
        self.setLayout(self.layout)
