from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QFontDialog
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5.QtWidgets import QMenu, QMenuBar, QAction
from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QFont
import sys


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Свойства окна.
        self.setWindowTitle("Osmolko")
        self.resize(620, 877)

        # Элементы.
        self.textEdit = QTextEdit()
        self.fontList = QPushButton("Sourse sans pro")
        self.enableBold = QPushButton("B")
        self.enableItalic = QPushButton("I")
        self.enableUnderline = QPushButton("U")
        self.menuBar = QMenuBar()
        self.menu = QMenu('File', self)
        self.saveAction = QAction('Save', self)
        self.openAction = QAction('Open', self)
        self.prewievAction = QAction('Prewiev', self)
        self.printAction = QAction('Print', self)

        self.menu.addAction(self.saveAction)
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.prewievAction)
        self.menu.addAction(self.printAction)
        self.menuBar.addMenu(self.menu)

        # Отображение всех элементов.
        Hbox = QHBoxLayout()
        self.enableBold.setFixedSize(30, 30)
        self.enableItalic.setFixedSize(30, 30)
        self.enableUnderline.setFixedSize(30, 30)
        Hbox.addWidget(self.fontList)
        Hbox.addWidget(self.enableBold)
        Hbox.addWidget(self.enableItalic)
        Hbox.addWidget(self.enableUnderline)

        Vbox = QVBoxLayout()
        Vbox.addWidget(self.menuBar)
        Vbox.addLayout(Hbox)
        Vbox.addWidget(self.textEdit)
        self.setLayout(Vbox)

        # Привязка действий.
        self.fontList.clicked.connect(self.showFontDialog)
        self.saveAction.triggered.connect(self.showSaveDialog)
        self.openAction.triggered.connect(self.showOpenDialog)
        self.prewievAction.triggered.connect(self.prewiewFile)
        self.printAction.triggered.connect(self.printFile)
        self.enableItalic.clicked.connect(self.doItalic)
        self.enableUnderline.clicked.connect(self.doUnderline)

        # Быстрые клавиши.
        self.saveAction.setShortcut('Ctrl+S')
        self.openAction.setShortcut('Ctrl+O')
        self.prewievAction.setShortcut('Ctrl+P')
        self.fontList.setShortcut('Ctrl+D')

    def showFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setCurrentFont(font)
            self.fontList.setText(font.family())

    def showSaveDialog(self):
        DataToSave = self.textEdit.toHtml()
        fileName = QFileDialog.getSaveFileName(self, self.tr("HTML files (*.html *.htm)"))[0]
        if fileName:
            with open(fileName, 'w') as file:
                file.write(DataToSave)

    def showOpenDialog(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if fileName:
            with open(fileName, 'r') as file:
                data = file.read()
                self.textEdit.setHtml(data)

    def printFile(self):
        printDialog = QPrintDialog()
        if printDialog.exec_() == QDialog.Accepted:
            self.textEdit.document().print_(printDialog.printer())

    def prewiewFile(self):
        prewiewDialog = QPrintPreviewDialog()
        prewiewDialog.paintRequested.connect(self.textEdit.print_)
        prewiewDialog.exec_()

    def doItalic(self):
        if self.textEdit.fontItalic():
            self.textEdit.setFontItalic(False)
        else:
            self.textEdit.setFontItalic(True)

    def doUnderline(self):
        if self.textEdit.fontUnderline():
            self.textEdit.setFontUnderline(False)
        else:
            self.textEdit.setFontUnderline(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())
