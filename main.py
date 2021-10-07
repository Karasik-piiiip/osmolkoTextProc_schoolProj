from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QFontDialog
from PyQt5.QtWidgets import QFileDialog, QDialog
from PyQt5.QtWidgets import QMenu, QMenuBar, QAction, QComboBox
from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog
import sys


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Свойства окна.
        self.setWindowTitle('Osmolko')
        self.setFixedSize(630, 900)

        # Элементы.
        self.textEdit = QTextEdit()
        self.fontList = QPushButton('Sourse sans pro')
        self.enableFontSize = QComboBox()
        self.enableFontSize.addItems(list(str(i) for i in range(1, 250)))
        self.enableItalic = QPushButton('I')
        self.enableUnderline = QPushButton('U')
        self.menuBar = QMenuBar()
        self.menu = QMenu('File', self)
        self.saveAction = QAction('Save', self)
        self.openAction = QAction('Open', self)
        self.prewievAction = QAction('Preview', self)
        self.printAction = QAction('Print', self)

        self.__addAllMenuActions(self.menu, (self.saveAction, self.openAction, self.prewievAction, self.printAction))
        self.menuBar.addMenu(self.menu)

        # Отображение всех элементов.
        Hbox = QHBoxLayout()
        self.enableFontSize.setFixedSize(45, 25)
        self.enableItalic.setFixedSize(30, 25)
        self.enableUnderline.setFixedSize(30, 25)
        self.__addAllWidgetsToLayout(Hbox, (self.fontList, self.enableFontSize, self.enableItalic, self.enableUnderline))

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
        self.enableFontSize.activated.connect(self.resetFontSize)

        # Быстрые клавиши.
        self.saveAction.setShortcut('Ctrl+S')
        self.openAction.setShortcut('Ctrl+O')
        self.prewievAction.setShortcut('Ctrl+P')
        self.fontList.setShortcut('Ctrl+D')

    def __addAllMenuActions(self, menu, list):
        for act in list:
            menu.addAction(act)

    def __addAllWidgetsToLayout(self, layout, list):
        for widget in list:
            layout.addWidget(widget)

    def showFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setCurrentFont(font)
            self.fontList.setText(font.family())

    def showSaveDialog(self):
        DataToSave = self.textEdit.toHtml()
        fileName = QFileDialog.getSaveFileName(self, self.tr("Сохраните файл"), '', self.tr("HTML files (*.html *.htm)"))[0] + '.html'
        if fileName:
            with open(fileName, 'w') as file:
                file.write(DataToSave)

    def showOpenDialog(self):
        """Диалог открытия файла"""
        fileName = QFileDialog.getOpenFileName(self, 'Откройте файл.', '', self.tr("HTML files (*.html *.htm)"))[0]
        if fileName:
            with open(fileName, 'r') as file:
                data = file.read()
                self.textEdit.setHtml(data)

    def printFile(self):
        """Печать файла без предпросмотра. """
        printDialog = QPrintDialog()
        if printDialog.exec_() == QDialog.Accepted:
            self.textEdit.document().print_(printDialog.printer())

    def prewiewFile(self):
        """Диалог предпросмотра файла перед печатью. """
        prewiewDialog = QPrintPreviewDialog()
        prewiewDialog.paintRequested.connect(self.textEdit.print_)
        prewiewDialog.exec_()

    def doItalic(self):
        """Добавляет курсивность всему следующему тексту."""
        if self.textEdit.fontItalic():
            self.textEdit.setFontItalic(False)
        else:
            self.textEdit.setFontItalic(True)

    def doUnderline(self):
        """Добавляет подчеркивание всему следующему тексту."""
        if self.textEdit.fontUnderline():
            self.textEdit.setFontUnderline(False)
        else:
            self.textEdit.setFontUnderline(True)

    def resetFontSize(self):
        """Замена текущего размера шрифта."""
        self.textEdit.setFontPointSize(int(self.enableFontSize.currentText()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())
