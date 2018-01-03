# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\Projects\GoDaddyDNSApp\GoDaddyDNSApp\ui\apikeyentry.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ApiKeyEntry(object):
    def setupUi(self, ApiKeyEntry):
        ApiKeyEntry.setObjectName("ApiKeyEntry")
        ApiKeyEntry.resize(445, 122)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApiKeyEntry.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ApiKeyEntry)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMinimumSize(QtCore.QSize(55, 0))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.secretKeyEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.secretKeyEdit.setObjectName("secretKeyEdit")
        self.horizontalLayout_3.addWidget(self.secretKeyEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(55, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.publikKeyEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.publikKeyEdit.setObjectName("publikKeyEdit")
        self.horizontalLayout_2.addWidget(self.publikKeyEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.importButton = QtWidgets.QPushButton(self.centralwidget)
        self.importButton.setObjectName("importButton")
        self.horizontalLayout_4.addWidget(self.importButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_4.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout_4, 4, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        ApiKeyEntry.setCentralWidget(self.centralwidget)

        self.retranslateUi(ApiKeyEntry)
        QtCore.QMetaObject.connectSlotsByName(ApiKeyEntry)

    def retranslateUi(self, ApiKeyEntry):
        _translate = QtCore.QCoreApplication.translate
        ApiKeyEntry.setWindowTitle(_translate("ApiKeyEntry", "GoDaddy API Key"))
        self.label_2.setText(_translate("ApiKeyEntry", "Secret Key"))
        self.label.setText(_translate("ApiKeyEntry", "Public Key"))
        self.label_3.setText(_translate("ApiKeyEntry", "Access keys for Goddady Account."))
        self.importButton.setText(_translate("ApiKeyEntry", "Import Domains"))
        self.saveButton.setText(_translate("ApiKeyEntry", "Save"))
        self.cancelButton.setText(_translate("ApiKeyEntry", "Cancel"))

