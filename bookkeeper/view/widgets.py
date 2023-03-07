from PySide6 import QtWidgets


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, text: str, placeholder: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.input = QtWidgets.QLineEdit(placeholder)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

    def text(self):
        return self.input.text()


class LabeledBox(QtWidgets.QWidget):
    def __init__(self, text: str, data: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.box = QtWidgets.QComboBox()
        self.box.addItems(data)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.box)
        self.setLayout(self.layout)


class HistoryTable(QtWidgets.QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumnCount(4)
        self.setRowCount(10)  # ne 10, a count(cat_repo.get_all())

        self.setHorizontalHeaderLabels("Дата Сумма Категория Комментарий".split())
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.verticalHeader().hide()

    def set_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.setItem(i, j, QtWidgets.QTableWidgetItem(str(x).capitalize()))



