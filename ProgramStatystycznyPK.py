#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QSizePolicy, QStyleFactory, QTabWidget, QTextEdit, QVBoxLayout, QWidget, QMessageBox)
from PyQt5 import QtGui, QtWidgets, QtCore
import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib
matplotlib.style.use('ggplot')

fileName = "plik.csv"


class Programik(QDialog):
    def __init__(self, parent=None):
        super(Programik, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Styl:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Standardowa paleta")
        self.useStylePaletteCheckBox.setChecked(True)

        self.createGroupBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)

        

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)

        self.createTabWidget()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.GroupBox, 1, 0)
        mainLayout.addWidget(self.TabWidget, 2, 0)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        
        self.resize(400, 500)
        self.setWindowTitle("Programik Statystyczny")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):  # dodatki ze zmianą stylu
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())

        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):

        curVal = self.progressBar.value()

        maxVal = self.progressBar.maximum()

        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createTabWidget(
            self):  # tabelka i tekst- puste, tylko na ozdobę gdy nie są jeszcze wyświetlone dane z pliku
        self.TabWidget = QTabWidget()
        self.TabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        tab2 = QWidget()
        textEdit = QTextEdit()
        textEdit.setPlainText("Narazie brak notatek")
        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.TabWidget.addTab(tab2, "&Notatki")

    def createGroupBox(self):
        self.GroupBox = QGroupBox("Wybór zbioru danych")
        self.GroupBox.setCheckable(True)
        self.GroupBox.setChecked(True)
        self.pushButton1 = QPushButton("&Liczę statystyki")
        self.pushButton2 = QPushButton("&Chcę wykresy")
        self.pushButton3 = QPushButton("&Pokaż korelację")
        self.pushButton1.clicked.connect(Statystyki)
        self.pushButton2.clicked.connect(Wykresy)
        self.pushButton3.clicked.connect(Korelacja)

        layout = QVBoxLayout()
        layout.addWidget(self.pushButton1)
        layout.addWidget(self.pushButton2)
        layout.addWidget(self.pushButton3)
        layout.addStretch(1)

        self.GroupBox.setLayout(layout)
        

    def createProgressBar(self):  # pasek postępu
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

    def closeEvent(self, event):  # zapytanie, czy chcesz opuścić program
        reply = QMessageBox.question(self, 'Message', "Czy na pewno chcesz wyjść?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Statystyki(QDialog):
    def __init__(self, parent=None):
        super(Statystyki, self).__init__()
        dane = pd.read_csv(fileName, usecols=[2], parse_dates=True, sep=";").replace(",", ".")
        dataset = np.array([s.replace(",", ".") for s in dane.get_values().flatten()]).astype(np.float)

        myDialog = QDialog();
        myDialog.setModal(True)
        
        self.mean = np.mean(dataset)
        self.g = stats.gmean(dataset)
        self.h = stats.hmean(dataset)
        self.median = np.median(dataset)
        self.s = stats.mode(dataset, axis=None)
        self.std = np.std(dataset)
        self.var = np.var(dataset)
        self.ptp = np.ptp(dataset)
        self.skew = stats.skew(dataset)
        self.kur = stats.kurtosis(dataset, axis=0, fisher=False)


        print(self.s)
        l1 = QLabel()
        l1.setText("Średnia arytmetyczna: {1:.4f}".format("wartosc", self.mean))
        l2 = QLabel()
        l2.setText("Średnia geometryczna: {1:.4f}".format("wartosc", self.g))
        l3 = QLabel()
        l3.setText("Srednia harmoniczna: {1:.4f}".format("wartosc", self.h))
        l4 = QLabel()
        l4.setText("Mediana: {1:.4f}".format("wartosc", self.median))
        l6 = QLabel()
        l6.setText("Odchylenie standardowe: {1:.4f}".format("wartosc", self.std))
        l7 = QLabel()
        l7.setText("Wariancja: {1:.4f}".format("wartosc", self.var))
        l8 = QLabel()
        l8.setText("Rozstęp: {1:.4f}".format("wartosc", self.ptp))
        l9 = QLabel()
        l9.setText("Skoczność: {1:.4f}".format("wartosc", self.skew))
        l10 = QLabel()
        l10.setText("Kurtoza: {1:.4f}".format("wartosc", self.kur))

        vbox = QVBoxLayout()
        vbox.addWidget(l1)
        vbox.addStretch()
        vbox.addWidget(l2)
        vbox.addStretch()
        vbox.addWidget(l3)
        vbox.addStretch()
        vbox.addWidget(l4)
        vbox.addStretch()
        vbox.addWidget(l6)
        vbox.addStretch()
        vbox.addWidget(l7)
        vbox.addStretch()
        vbox.addWidget(l8)
        vbox.addStretch()
        vbox.addWidget(l9)
        vbox.addStretch()
        vbox.addWidget(l10)
        vbox.addStretch()

        myDialog.setLayout(vbox)
        myDialog.setWindowTitle("Statystyki")
        myDialog.show()
        myDialog.exec()

class Wykresy():
    def __init__(self, parent=None):
        super(Wykresy, self).__init__()
        dane = pd.read_csv(fileName, usecols=[2], parse_dates=True, sep=";").replace(",", ".")

        # wykres zwykły
        dataset = np.array([s.replace(",", ".") for s in dane.get_values().flatten()]).astype(np.float)

        plt.boxplot(dataset)  # wykres pudełkowy
        plt.show()
        plt.hist(dataset, bins=10, edgecolor='black')  # histogram
        plt.show()
        
        


class Korelacja():
    def __init__(self,  parent=None):
        super(Korelacja, self).__init__()
        dane1 = pd.read_csv(fileName, usecols=[2], parse_dates=True, sep=";").replace(",", ".")
        dane2 = pd.read_csv(fileName, usecols=[3], parse_dates=True, sep=";").replace(",", ".")
        # wykres zwykły
        dataset1 = np.array([s.replace(",", ".") for s in dane1.get_values().flatten()]).astype(np.float)
        dataset2 = np.array([s.replace(",", ".") for s in dane2.get_values().flatten()]).astype(np.float)
        x = dataset1
        y = dataset2
        plt.scatter(x, y, color='r')  # wykresy korelacji
        plt.show()
       
        self.corr = stats.pearsonr(x, y)
       
        
        print("Współczynnik korelacji:", self.corr)
        
        

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Load Csv File!")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonWrite = QtWidgets.QPushButton(self)
        self.pushButtonWrite.setText("Write Csv File!")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pushButtonLoad)
        self.layoutVertical.addWidget(self.pushButtonWrite)

        self.resize(300, 300)
        self.setWindowTitle("&Dane")
        self.show()

    def loadCsv(self):
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)

    def writeCsv(self):
        with open(fileName, "a") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)

    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv()

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.loadCsv()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dane = MyWindow()
    main = Programik()
    main.show()
    sys.exit(app.exec_())
