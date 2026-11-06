import sys
import sqlite3
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.db_path = None

        self.setWindowTitle("Labs №3 — PyQt and SQL")
        self.resize(900, 600)

        self.create_menu()
        self.create_interface()

    def create_menu(self):
        menu = self.menuBar().addMenu("Menu")

        set_connection = QtWidgets.QAction("Set connection", self)
        close_connection = QtWidgets.QAction("Close connection", self)
        custom_query = QtWidgets.QAction("Custom query", self)

        set_connection.triggered.connect(self.set_connection)
        close_connection.triggered.connect(self.close_connection)
        custom_query.triggered.connect(self.open_query_dialog)

        menu.addAction(set_connection)
        menu.addAction(close_connection)
        menu.addSeparator()
        menu.addAction(custom_query)

    def create_interface(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.bt1 = QtWidgets.QPushButton('bt1 "SELECT name"')
        self.bt2 = QtWidgets.QPushButton('bt2 "Tables"')
        self.bt3 = QtWidgets.QPushButton('bt3 "Indexes"')

        self.combo_columns = QtWidgets.QComboBox()
        self.combo_columns.addItem("Columns")

        controls = QtWidgets.QGridLayout()
        controls.addWidget(self.bt1, 0, 0)
        controls.addWidget(self.combo_columns, 0, 1)
        controls.addWidget(self.bt2, 1, 0)
        controls.addWidget(self.bt3, 1, 1)

        self.tabs = QtWidgets.QTabWidget()
        self.tables = []

        for i in range(5):
            table = QtWidgets.QTableWidget()
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table.horizontalHeader().setStretchLastSection(True)
            self.tables.append(table)
            self.tabs.addTab(table, f"Tab{i + 1}")

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(controls)
        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

        self.bt1.clicked.connect(self.query_names)
        self.bt2.clicked.connect(self.query_tables)
        self.bt3.clicked.connect(self.query_indexes)
        self.combo_columns.currentTextChanged.connect(self.query_selected_column)

        self.set_controls_enabled(False)

    def set_controls_enabled(self, enabled):
        self.bt1.setEnabled(enabled)
        self.bt2.setEnabled(enabled)
        self.bt3.setEnabled(enabled)
        self.combo_columns.setEnabled(enabled)

    def set_connection(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Choose SQLite database",
            "",
            "SQLite database (*.db *.sqlite *.sqlite3);;All files (*)"
        )

        if not filename:
            return

        self.close_connection()

        try:
            self.connection = sqlite3.connect(filename)
            self.db_path = filename
            self.set_controls_enabled(True)

            self.run_query("SELECT * FROM sqlite_master", self.tables[0])
            self.load_columns()

            self.statusBar().showMessage(f"Connected: {filename}")

        except sqlite3.Error as error:
            QtWidgets.QMessageBox.critical(self, "Connection error", str(error))

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

        self.connection = None
        self.db_path = None

        for table in self.tables:
            table.clear()
            table.setRowCount(0)
            table.setColumnCount(0)

        self.combo_columns.blockSignals(True)
        self.combo_columns.clear()
        self.combo_columns.addItem("Columns")
        self.combo_columns.blockSignals(False)

        self.set_controls_enabled(False)
        self.statusBar().showMessage("Connection closed")

    def check_connection(self):
        if self.connection is None:
            QtWidgets.QMessageBox.warning(
                self,
                "No connection",
                "Set connection to database first."
            )
            return False
        return True

    def run_query(self, query, table):
        if not self.check_connection():
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            if cursor.description is None:
                self.connection.commit()
                table.clear()
                table.setRowCount(1)
                table.setColumnCount(1)
                table.setHorizontalHeaderLabels(["Result"])
                table.setItem(0, 0, QtWidgets.QTableWidgetItem("Query completed"))
                return

            rows = cursor.fetchall()
            columns = [item[0] for item in cursor.description]

            table.clear()
            table.setColumnCount(len(columns))
            table.setHorizontalHeaderLabels(columns)
            table.setRowCount(len(rows))

            for row_index, row in enumerate(rows):
                for column_index, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem("" if value is None else str(value))
                    table.setItem(row_index, column_index, item)

            table.resizeColumnsToContents()

        except sqlite3.Error as error:
            QtWidgets.QMessageBox.critical(self, "SQL error", str(error))

    def query_names(self):
        self.run_query("SELECT name FROM sqlite_master", self.tables[1])
        self.tabs.setCurrentIndex(1)

    def load_columns(self):
        self.combo_columns.blockSignals(True)
        self.combo_columns.clear()
        self.combo_columns.addItem("Columns")

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' "
            "ORDER BY name"
        )

        for table_name, in cursor.fetchall():
            cursor.execute(f'PRAGMA table_info("{table_name}")')
            for row in cursor.fetchall():
                column_name = row[1]
                self.combo_columns.addItem(
                    f"{table_name}.{column_name}",
                    (table_name, column_name)
                )

        self.combo_columns.blockSignals(False)

    def query_selected_column(self, text):
        if text == "Columns" or not self.check_connection():
            return

        data = self.combo_columns.currentData()
        if not data:
            return

        table_name, column_name = data
        query = f'SELECT "{column_name}" FROM "{table_name}"'

        self.run_query(query, self.tables[2])
        self.tabs.setCurrentIndex(2)

    def query_tables(self):
        self.run_query(
            "SELECT name, sql FROM sqlite_master WHERE type='table'",
            self.tables[3]
        )
        self.tabs.setCurrentIndex(3)

    def query_indexes(self):
        self.run_query(
            "SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'",
            self.tables[4]
        )
        self.tabs.setCurrentIndex(4)

    def open_query_dialog(self):
        if not self.check_connection():
            return

        dialog = QueryDialog(self)
        dialog.exec_()


class QueryDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        self.setWindowTitle("Custom SQL query")
        self.resize(650, 450)

        self.query_edit = QtWidgets.QPlainTextEdit()
        self.query_edit.setPlaceholderText("Enter SQL query...")

        self.run_button = QtWidgets.QPushButton("Run")
        self.close_button = QtWidgets.QPushButton("Close")

        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.run_button)
        buttons.addWidget(self.close_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("SQL query:"))
        layout.addWidget(self.query_edit)
        layout.addLayout(buttons)
        layout.addWidget(self.result_table)
        self.setLayout(layout)

        self.run_button.clicked.connect(self.run_query)
        self.close_button.clicked.connect(self.close)

    def run_query(self):
        query = self.query_edit.toPlainText().strip()
        if not query:
            return
        self.main_window.run_query(query, self.result_table)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
