from PySide6 import QtWidgets


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, text: str, placeholder: int | str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(text)
        self.input = QtWidgets.QLineEdit(placeholder)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)


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
    def __init__(self, rows: tuple = (), columns: tuple = (), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setColumnCount(len(columns))
        if len(rows) == 0:
            rows = ('',) * 10

        self.setRowCount(len(rows))

        header = self.horizontalHeader()

        if len(columns) > 2:
            count = 0
            for i in range(len(columns) - 1):
                count = i
                header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(count+1, QtWidgets.QHeaderView.Stretch)
        else:
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Preferred)

        if len(rows) > 3:
            self.verticalHeader().hide()
        else:
            self.setVerticalHeaderLabels(rows)
        self.setHorizontalHeaderLabels(columns)

    def set_data(self, data: list[list[str]]) -> None:
        for i, row in enumerate(data):
            for number, x in enumerate(row):
                self.setItem(i, number, QtWidgets.QTableWidgetItem(str(x).capitalize()))
