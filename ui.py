# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets
from PIL import Image

import main


class Ui_Dialog(object):

    def __init__(self):
        self.nfa = None
        self.dfa = None
        self.file = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(772, 391)
        self.Button2 = QtWidgets.QPushButton(Dialog)
        self.Button2.setEnabled(False)
        self.Button2.setGeometry(QtCore.QRect(490, 230, 75, 23))
        self.Button2.setObjectName("Button2")
        self.Button3 = QtWidgets.QPushButton(Dialog)
        self.Button3.setEnabled(False)
        self.Button3.setGeometry(QtCore.QRect(650, 230, 111, 23))
        self.Button3.setMinimumSize(QtCore.QSize(0, 0))
        self.Button3.setObjectName("Button3")
        self.Button1 = QtWidgets.QPushButton(Dialog)
        self.Button1.setGeometry(QtCore.QRect(350, 310, 75, 23))
        self.Button1.setObjectName("Button1")
        self.lineEdit2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit2.setGeometry(QtCore.QRect(100, 190, 113, 20))
        self.lineEdit2.setObjectName("lineEdit2")
        self.label1 = QtWidgets.QLabel(Dialog)
        self.label1.setGeometry(QtCore.QRect(30, 190, 61, 16))
        self.label1.setObjectName("label1")
        self.Button4 = QtWidgets.QPushButton(Dialog)
        self.Button4.setEnabled(False)
        self.Button4.setGeometry(QtCore.QRect(120, 240, 75, 23))
        self.Button4.setObjectName("Button4")
        self.lineEdit1 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit1.setGeometry(QtCore.QRect(560, 190, 113, 20))
        self.lineEdit1.setObjectName("lineEdit1")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(500, 190, 31, 16))
        self.label2.setObjectName("label2")
        self.Ilabel = QtWidgets.QLabel(Dialog)
        self.Ilabel.setGeometry(QtCore.QRect(300, 80, 201, 71))
        self.Ilabel.setText("")
        self.Ilabel.setObjectName("Ilabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.connectButtons()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Button2.setText(_translate("Dialog", "NFA -> DFA"))
        self.Button3.setText(_translate("Dialog", "Minimize DFA"))
        self.Button1.setText(_translate("Dialog", "Choose File"))
        self.label1.setText(_translate("Dialog", "Input String"))
        self.Button4.setText(_translate("Dialog", "Check"))
        self.label2.setText(_translate("Dialog", "Name"))

    def connectButtons(self):
        self.Button2.clicked.connect(self.NFA_DFA)
        self.Button3.clicked.connect(self.minDFA)
        self.Button1.clicked.connect(self.choosefile)
        self.Button4.clicked.connect(self.checkString)

    def choosefile(self):
        x = QtWidgets.QFileDialog.getOpenFileName(None, '', '', "Text (*.txt)")
        if x[0] == '':
            return
        self.nfa = main.NFA()
        self.file = open(x[0], 'r', encoding='utf-8')
        text = self.file.readline()
        text = text.replace(' ', '')
        a = text.find('{', text.find('{') + 1)
        j = text.find('}', a)
        x = text[a + 1:j].split(',')
        for i in x:
            self.nfa.alpht.append(i)
        i = text.find('{')
        j = text.find('}')
        x = text[i + 1:j].split(',')
        for k in x:
            self.nfa.states.append(main.StateNFA(k, len(self.nfa.alpht)))
        i = text.find('{', a + 1)
        j = text.find('}', i + 1)
        x = text[i + 1:j].split(',')
        for k in x:
            r = self.nfa.getstate(k)
            r.accept = True
            self.nfa.accepts.append(r)
        i = text.find('{', i + 1)
        j = text.find('}', j + 1)
        x = text[i + 1:j]
        r = self.nfa.getstate(x)
        r.start = True
        self.nfa.start = r
        text = self.file.readline()
        while text != '':
            text = text.replace(' ', '')
            m = text[text.find('(') + 1:text.find(')')].split(',')
            e = text[text.find('=') + 1:].replace('\n', '')
            if m[1] == '??':
                self.nfa.getstate(m[0]).map[len(self.nfa.alpht)].append(self.nfa.getstate(e))
            else:
                self.nfa.getstate(m[0]).map[self.nfa.alpht.index(m[1])].append(self.nfa.getstate(e))
            text = self.file.readline()
        self.Button2.setEnabled(True)

    def NFA_DFA(self):
        if self.lineEdit1.text() == '':
            self.Ilabel.setText('Enter Name')
            return
        self.dfa = self.nfa.convertDFA()
        self.dfa.showimage(self.lineEdit1.text())
        img = Image.open(self.lineEdit1.text() + '.png')
        img.show()
        self.Button3.setEnabled(True)
        self.Button4.setEnabled(True)

    def minDFA(self):
        if self.lineEdit1.text() == '':
            self.Ilabel.setText('Enter Name')
            return
        self.dfa.minimization()
        self.dfa.showimage(self.lineEdit1.text())
        img = Image.open(self.lineEdit1.text() + '.png')
        img.show()
        self.Button4.setEnabled(True)

    def checkString(self):
        accept = self.dfa.checkstring(self.lineEdit2.text())
        if accept:
            self.Ilabel.setText('Accept')
        else:
            self.Ilabel.setText('Reject')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
