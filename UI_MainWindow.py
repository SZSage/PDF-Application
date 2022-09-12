import os
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QMainWindow, QLineEdit, \
    QInputDialog, QFileDialog, QListWidgetItem, QListWidget, QProgressBar, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyPDF2 import PdfFileMerger, PdfFileReader


class Thread(QThread):
    """Progress bar count"""
    change_value = pyqtSignal(int)

    def run(self):
        self.count = 0
        while self.count < 100:
            self.count += 1
            self.change_value.emit(self.count)


class MainWindow(QWidget):
    """Main Window application"""

    def __init__(self):
        super().__init__()
        # sets application name
        self.setWindowTitle("PDF Merge")
        # size of application
        self.resize(720, 480)
        self.initUI()

    def initUI(self):
        """Ini UI"""

        # ini widgets
        main_layout = QVBoxLayout()
        output_window = QHBoxLayout()
        button_layout = QHBoxLayout()
        # creates empty text box widget
        self.pdf_list_widget = QListWidget(self)  # imports QListWidget box
        self.progress_bar = progress_bar()
        self.progress_bar.setValue(0)

        self.output_file = output_field()  # set output_file to box class
        self.output_file.setReadOnly(True)  # sets text box to read only
        output_window.addWidget(self.output_file)  # adds box widget

        self.button_file = button("Select Files")  # calls button class and names button
        self.button_merge = button("Merge Files")
        self.button_remove = button("Remove file")

        output_window.addWidget(self.button_file)  # adds button widget to box widget
        output_window.addWidget(self.button_merge)
        output_window.addWidget(self.button_remove)

        self.button_file.clicked.connect(self.select_files)
        self.button_merge.clicked.connect(self.pdf_merge)
        self.button_merge.clicked.connect(self.start_progress_bar)
        self.button_remove.clicked.connect(self.remove_file)
        # adds widgets to main layout
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.pdf_list_widget)
        main_layout.addLayout(output_window)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
    def select_files(self):
        """Opens file selector and select"""
        path = "/users/Sage/Documents/Coding/PDFMerge"
        os.chdir(path)  # changes default directory to path
        self.file_name = QFileDialog.getOpenFileNames()
        # reads selected file
        self.path = self.file_name[0]
        self.list_files_in_viewer(self.path)

    def list_files_in_viewer(self, file_name):
        """Adds item to pdf list widget"""
        for pdf in file_name:
            item = QListWidgetItem(pdf)
            item.setText(pdf)
            self.pdf_list_widget.addItem(item)

    def pdf_merge(self):
        """Merges selected files"""
        path = "/users/Sage/Documents/Coding/PDFMerge"
        os.chdir(path)  # changes default directory to path
        merger = PdfFileMerger()

        for pdf in self.path:
            merger.append(pdf)
        merger.write("Merged PDF File.pdf")

    def remove_file(self):
        """Removes selected files"""
        items = self.pdf_list_widget.selectedItems()
        for file in items:
            self.pdf_list_widget.takeItem(self.pdf_list_widget.row(file))

    def set_progress_value(self, val):
        """Creates progress bar value"""
        self.progress_bar.setValue(val)

    def start_progress_bar(self):
        """Starts progress bar when merge button is selected"""
        self.thread = Thread()
        self.thread.change_value.connect(self.set_progress_value)
        self.thread.start()
        self.progress_bar.setFormat("%p%    Merge Complete")


class button(QPushButton):
    """Creates buttons. Changes font & size"""
    def __init__(self, label_text):
        super().__init__()
        self.setText(label_text)
        self.setStyleSheet("""
            font-size: 20px;
            width: 120px;
            height: 50px;
        """)


class progress_bar(QProgressBar):
    """ Create progress bar"""
    def __init__(self):
        super().__init__()
        self.width = 900
        self.setFixedWidth(self.width)


class output_field(QLineEdit):
    """Create output field box"""
    def __init__(self):
        super().__init__()
        self.height = 50
        self.setStyleSheet("font-size: 20px;")
        self.setFixedHeight(self.height)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
