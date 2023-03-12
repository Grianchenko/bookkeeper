from PySide6 import QtWidgets, QtCore

from bookkeeper.view.utils import LabeledInput, HistoryTable


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


class CategoryManager(QtWidgets.QWidget):
    button_clicked = QtCore.Signal(str, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_input = LabeledInput('Category name', '')
        self.parent_input = LabeledInput('Parent (if needed)', '')

        self.add_button = QtWidgets.QPushButton('Add')
        self.add_button.clicked.connect(self.add)
        self.update_button = QtWidgets.QPushButton('Update')
        self.update_button.clicked.connect(self.update_cat)
        self.delete_button = QtWidgets.QPushButton('Delete')
        self.delete_button.clicked.connect(self.delete)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel('Category manager'))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.parent_input)

        self.buttons_widget = QtWidgets.QWidget()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.update_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.buttons_widget.setLayout(self.buttons_layout)

        self.layout.addWidget(self.buttons_widget)
        self.setLayout(self.layout)

    def submit(self, mode: str) -> None:
        try:
            self.button_clicked.emit(str(self.name_input.input.text()),
                                     str(self.parent_input.input.text()))
            if mode == 'add':
                self.button_clicked.connect(print('Add-Category-Click'))
            elif mode == 'delete':
                self.button_clicked.connect(print('Delete-Category-Click'))
            elif mode == 'update':
                self.button_clicked.connect(print('Update-Category-Click'))
        except ValueError:
            QtWidgets.QMessageBox.critical(self, 'Error', 'Incorrect input!')

    def add(self) -> None:
        self.submit('add')

    def delete(self) -> None:
        self.submit('delete')

    def update_cat(self) -> None:
        self.submit('update')


class Categories(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        act_cat = CategoriesExists()
        new_cat = CategoryManager()
        self.layout.addWidget(act_cat)
        self.layout.addWidget(new_cat)
        self.setLayout(self.layout)
