import datetime

from PySide6 import QtWidgets, QtCore

from bookkeeper.view.utils import LabeledInput, HistoryTable, LabeledBox
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class CategoriesExists(QtWidgets.QWidget):
    def __init__(self, cat_repo: AbstractRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_repo = cat_repo
        self.columns = ('Category', 'Parent')
        self.data = []
        self.table = HistoryTable(columns=self.columns, n_rows=len(self.cat_repo.get_all()))
        self.set_data()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Categories'))
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def set_data(self) -> None:
        self.data = []
        got_all = self.cat_repo.get_all()
        if got_all:
            for cat in got_all[::-1]:
                try:
                    temp = [cat.name,
                            self.cat_repo.get(int(cat.parent)).name]
                except TypeError:
                    temp = [cat.name, '']
                self.data.append(temp)
        self.table.set_data(self.data)


class CategoryManager(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(str, str)

    def __init__(self, cat_repo: AbstractRepository,
                 exp_repo: AbstractRepository,
                 cat_ex: CategoriesExists,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_ex = cat_ex
        self.cat_repo = cat_repo
        self.exp_repo = exp_repo
        self.par_list = [cat.name for cat in self.cat_repo.get_all()][::-1]
        self.parent_choice = LabeledBox('Category', self.par_list)
        self.name_input = LabeledInput('Category name', '')
        self.set_par_choice()

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add)
        self.update_button = QtWidgets.QPushButton('Update')
        self.update_button.clicked.connect(self.update_cat)
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Category manager'))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.parent_choice)

        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.buttons_widget.setLayout(self.buttons_layout)

        self.layout.addWidget(self.buttons_widget)
        self.setLayout(self.layout)

    def set_par_choice(self):
        self.par_list = [cat.name.capitalize() for
                         cat in self.cat_repo.get_all()][::-1]
        self.parent_choice.box.clear()
        self.parent_choice.box.addItems(self.par_list)
        self.button_clicked.emit('', '')

    def submit(self, mode: str) -> None:
        try:
            self.button_clicked.emit(str(self.name_input.input.text()),
                                     str(self.parent_choice.box.currentText()))
            if True:
                self.button_clicked.connect(
                    self.edit_category(mode,
                                       str(self.name_input.input.text()),
                                       str(self.parent_choice.box.currentText())))
            self.button_clicked.connect(self.cat_ex.set_data())
            self.button_clicked.connect(self.set_par_choice())
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')

    def edit_category(self, mode: str, name: str, parent: str):
        parent_pk = self.parent_to_pk(parent)
        cat = Category(name.lower(), parent_pk)
        if parent != '' and parent_pk is None:
            QtWidgets.QMessageBox.critical(self, 'Error',
                                           'Parent doesn\'t exist!')
            return
        if mode == 'add':
            self.cat_repo.add(cat)
        elif mode == 'delete':
            cat_pk = self.cat_repo.get_all({'name': name.lower(),
                                            'parent': parent_pk})[0].pk
            self.cat_repo.delete(cat_pk)
            for exp in self.exp_repo.get_all({'category': cat_pk}):
                new_exp = Expense(exp.amount, parent_pk, exp.expense_date,
                                  exp.added_date, exp.comment, exp.pk)
                self.exp_repo.update(new_exp)
            # self.exp_sig.emit(6, '', '', datetime.datetime.now())
            # self.exp_sig.connect(print('works'))
            for cat in self.cat_repo.get_all({'parent': cat_pk}):
                new_cat = Category(cat.name, parent_pk, cat.pk)
                self.cat_repo.update(new_cat)
        elif mode == 'update':
            cat_pk = self.cat_repo.get_all({'name': name.lower()})[0].pk
            cat = type(self.cat_repo.get_all()[0])(name, parent_pk, pk=cat_pk)
            self.cat_repo.update(cat)

    def parent_to_pk(self, name: str):
        try:
            return self.cat_repo.get_all({'name': name.lower()})[0].pk
        except IndexError:
            return None

    def add(self) -> None:
        self.submit('add')

    def delete(self) -> None:
        self.submit('delete')

    def update_cat(self) -> None:
        self.submit('update')


class CategoriesTab(QtWidgets.QWidget):
    def __init__(self, cat_repo: AbstractRepository,
                 exp_repo: AbstractRepository, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp_repo = exp_repo
        self.cat_repo = cat_repo
        self.layout = QtWidgets.QVBoxLayout()
        self.act_cat = CategoriesExists(cat_repo=self.cat_repo)
        self.new_cat = CategoryManager(self.cat_repo, self.exp_repo,
                                       self.act_cat)
        self.layout.addWidget(self.act_cat)
        self.layout.addWidget(self.new_cat)
        self.setLayout(self.layout)
