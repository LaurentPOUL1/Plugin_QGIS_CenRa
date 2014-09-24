# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CenRaDialog
                                 A QGIS plugin
 Conservatoire d'Espaces Naturels de Rhône-Alpes
                             -------------------
        begin                : 2014-03-27
        copyright            : (C) 2014 by Conservatoire d'Espaces Naturels de Rhône-Alpes
        email                : guillaume.costes@espaces-naturels.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_cenra import Ui_cenra
# create the dialog for zoom to point


class CenRaDialog(QtGui.QDialog, Ui_cenra):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
