import sys
from PySide6 import QtWidgets

from bookkeeper.view.interface import MainWindow
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category


class Presenter:
    def __init__(self):
        self.db: str = 'main_db.db'
        self.exp_repo = SQLiteRepository[Expense](self.db, Expense)
        self.cat_repo = SQLiteRepository[Category](self.db, Category)
        self.view: QtWidgets.QMainWindow = MainWindow(self.exp_repo, self.cat_repo)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.processEvents()
    window = Presenter()

    # window.view.central_widget.currentWidget().new_exp.button_clicked.connect(print('aaaaaa'))
    window.view.show()

    sys.exit(app.exec())
