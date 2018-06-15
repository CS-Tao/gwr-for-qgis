# -*- coding: utf-8 -*-
import os

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'result_display_base.ui'))


class result_displayDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(result_displayDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        formIcon = QIcon()
        formIcon.addFile(self.tr(":/plugins/gwr/icons/earth.png"))
        self.setWindowIcon(formIcon)
        saveIcon = QIcon()
        saveIcon.addFile(self.tr(":/plugins/gwr/icons/mapcalc_save.png"))
        self.pushButton_SaveGlobal.setIcon(saveIcon)
        self.pushButton_SaveGlobal.setIconSize(QSize(30, 30))
        self.pushButton_SaveCsv.setIcon(saveIcon)
        self.pushButton_SaveCsv.setIconSize(QSize(30, 30))
        self.pushButton_SaveGlobal.clicked.connect(self.saveGlobalResults)
        self.pushButton_SaveCsv.clicked.connect(self.saveCsv)
        # self.tableWidget_Results.itemSelectionChanged.connect(self.appendRecordToLayer)
        self.vectorLayer = None
        self.statisticData = None
        self.tableHeader = []
        self.tableData = []

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('gwr', message)

    def showResult(self, layer, statisticData, tableHeader, tableData):
        self.vectorLayer = layer
        self.textEdit_GlobalResults.setText(statisticData)
        self.statisticData = statisticData
        self.tableHeader = tableHeader
        self.tableData = tableData
        if len(tableHeader) == 0 or len(tableData) == 0 or len(tableHeader) != len(tableData[0]):
            self.show()
            return
        self.tableWidget_Results.setRowCount(len(tableData))
        self.tableWidget_Results.setColumnCount(len(tableData[0]))
        tempTableWidgetItem = QTableWidgetItem()
        col = 0
        for header in tableHeader:
            tempTableWidgetItem = QTableWidgetItem()
            tempTableWidgetItem.setText(header)
            self.tableWidget_Results.setHorizontalHeaderItem(col, tempTableWidgetItem)
            col += 1
        row = 0
        for rowData in tableData:
            col = 0
            for data in rowData:
                tempTableWidgetItem = QTableWidgetItem()
                tempTableWidgetItem.setText(str(data))
                self.tableWidget_Results.setItem(row, col, tempTableWidgetItem)
                col += 1
            row += 1
        self.show()


    def saveGlobalResults(self):
        fileName, _ = QFileDialog.getSaveFileName(self, '保存文件', os.path.dirname(__file__), r'txt(*.txt)')
        if not fileName:
            return
        resultFile = open(fileName, "w")
        resultFile.write(self.statisticData)
        resultFile.close()


    def saveCsv(self):
        fileName, _ = QFileDialog.getSaveFileName(self, '保存文件', os.path.dirname(__file__), r'csv(*.csv)')
        if not fileName:
            return
        csvFile = open(fileName, "w")
        col = 0
        for head in self.tableHeader:
            if col != (len(self.tableHeader) - 1):
                csvFile.write(str(head) + ',')
            else:
                csvFile.write(str(head) + '\n')
            col += 1
        for rowData in self.tableData:
            col = 0
            for data in rowData:
                if col != (len(rowData) - 1):
                    csvFile.write(str(data) + ',')
                else:
                    csvFile.write(str(data) + '\n')
                col += 1
        csvFile.close()


    def appendRecordToLayer(self):
        # colIndex = self.tableWidget_Results.currentColumn()
        # self.vectorLayer.addAttribute(QgsField(self.tr(str(self.tableWidget_Results.takeHorizontalHeaderItem(colIndex)))))
        # QMessageBox.question(self, 'test', str(self.tableWidget_Results.currentColumn()), QMessageBox.Ok)
        pass
        