# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CenRa
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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load CenRa class from file CenRa
    from cenra import CenRa
    return CenRa(iface)
