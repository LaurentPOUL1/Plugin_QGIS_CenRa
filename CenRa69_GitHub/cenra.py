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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from cenradialog import CenRaDialog
from table_postgisdialog import table_postgisDialog

import os.path
import webbrowser, os
import sys
import psycopg2

class CenRa:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'cenra_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = CenRaDialog()
        self.dlgAjout = table_postgisDialog()
		
    def initGui(self):
        self.toolBar = self.iface.addToolBar("CEN-RA")
        self.toolBar.setObjectName("CEN-RA")
		
	    # ***Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/CenRa/page_new.png"),
            u"Création d'un dossier", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.creation)

        # Add toolbar button and menu item
        self.toolBar.addAction(self.action)		
        self.iface.addPluginToMenu(u"CenRa", self.action)
		
        # ***Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/CenRa/page_ajout.png"),
            u"Ajout d'une table", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.ajout)

        # Add toolbar button and menu item
        self.toolBar.addAction(self.action)
        self.iface.addPluginToMenu(u"&CenRa", self.action)

        # ***Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/CenRa/help.png"),
            u"Aide", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.doHelp)

        # Add toolbar button and menu item
        self.toolBar.addAction(self.action)
        self.iface.addPluginToMenu(u"CenRa", self.action)
		
        self.menu = QMenu()
        self.menu.setTitle( QCoreApplication.translate( "CENRA","&CenRa" ) )

        self.cenra_new = QAction( QIcon(":/plugins/CenRa/page_new.png"), QCoreApplication.translate("CENRA", u"Création d'un dossier" ), self.iface.mainWindow() )
        self.cenra_ajout = QAction( QIcon(":/plugins/CenRa/page_ajout.png"), QCoreApplication.translate("CENRA", "Ajout d'une table" ), self.iface.mainWindow() )
        self.cenra_help = QAction( QIcon(":/plugins/CenRa/help.png"), QCoreApplication.translate("CENRA", "Aide" ), self.iface.mainWindow() )
		
        self.menu.addActions( [self.cenra_new, self.cenra_ajout, self.cenra_help] )
		
        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[ len( actions ) - 1 ]
        menu_bar.insertMenu( lastAction, self.menu )
		
        self.cenra_new.triggered.connect(self.creation)
        self.cenra_ajout.triggered.connect(self.ajout)
        self.cenra_help.triggered.connect(self.doHelp)
		
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&CenRa", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def creation(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            
#**********************************Debut_script****************************************
            import psycopg2
			
            ### config.txt
            config = "//chemin/fichier/config.txt" # Chemin du fichier config

                # Fonction de lecture des lignes du fichier config
            def readline(n):
              with open(config, "r") as f:
                for lineno, line in enumerate(f):
                  if lineno == n:
                    return line.strip() # Permet d'enlever les retours chariots

                # Recuperation des donnees
            host = readline(10)
            port = readline(12)
            dbname = readline(14)
            user = readline(16)
            password = readline(18)

            ### Creation du schema pour le nouveau site
            if self.dlg.at.isChecked():
				schema = "_" + self.dlg.dept.currentText() + "_at_" + self.dlg.nom.text().lower() # Ajout de "_" pour eviter pb de numero en premier caractere
            else :			
				schema = "_" + self.dlg.dept.currentText() + "_" + self.dlg.nom.text().lower() # Ajout de "_" pour eviter pb de numero en premier caractere
				
            if self.dlg.nom.text() == "" or self.dlg.nom.text() == "NULL":
				QMessageBox.warning(None, "Oups :", "Veuillez renseigner un nom de dossier.")
				return
			
            ch = [u"à", u"À", u"â", u"Â", u"ä", u"Ä", u"å", u"Å", u"ç", u"Ç", u"é", u"É", u"è", u"È", u"ê", u"Ê", u"ë", u"Ë", u"î", u"Î", u"ï", u"Ï", u"ô", u"Ô", u"ö", u"Ö", u"ù", u"Ù", u"û", u"Û", u"ü", u"Ü", u"ÿ", u"Ÿ", u"'", u"-", u" "]
            for car in ch :
				if self.dlg.nom.text().find(car) != -1 :
					QMessageBox.warning(None, "Oups :", u"Le nom de dossier ne doit pas comporter de caractères spéciaux, ni d'espaces !\n\n\t" + self.dlg.nom.text().lower() )
					return
            
            con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password)
            cur = con.cursor()

            SQL_schema = "CREATE SCHEMA " + schema + " AUTHORIZATION postgres;"

            cur.execute(SQL_schema)

            ### Creation de la table contour
            if self.dlg.couche_contour.isChecked(): # Verifie si la checkbox est cochee
                if 	self.dlg.annee_1.text() == 'aaaa' or self.dlg.annee_1.text() == '':
					tablename = schema + "_contour"					
                else :
					tablename = schema + "_contour_" + self.dlg.annee_1.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(21)
                champ_contour = readline(32)

                SQL_contour = "CREATE TABLE " + schema + "."+ tablename + champ_contour
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'contour_modele'"""
				
                cur.execute(SQL_contour)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
				
                con.commit()
				
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

            ### Creation de la table habitat
            if self.dlg.couche_habitat.isChecked():
                if 	self.dlg.annee_2.text() == 'aaaa' or self.dlg.annee_2.text() == '':
					tablename = schema + "_habitat"					
                else :
					tablename = schema + "_habitat_" + self.dlg.annee_2.text()			
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(22)
                champ_habitat = readline(35)

                SQL_habitat = "CREATE TABLE " + schema + "."+ tablename + champ_habitat
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
                SQL_trigger_concat_cd_cb = "CREATE TRIGGER concat_cd_cb" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.concat_cd_cb();"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'habitat_modele'"""
								
                cur.execute(SQL_habitat)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)
                cur.execute(SQL_trigger_concat_cd_cb)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table travaux realises
            if self.dlg.couche_travaux_realises.isChecked():
					#******Poly
                if 	self.dlg.annee_3.text() == 'aaaa' or self.dlg.annee_3.text() == '':
					tablename = schema + "_travaux_realises_poly"					
                else :
					tablename = schema + "_travaux_realises_poly_" + self.dlg.annee_3.text()					
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(23)
                champ_travaux_realises = readline(38)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_poly_modele'"""
				
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#*********Ligne
                if 	self.dlg.annee_3.text() == 'aaaa' or self.dlg.annee_3.text() == '':
					tablename = schema + "_travaux_realises_ligne"					
                else :
					tablename = schema + "_travaux_realises_ligne_" + self.dlg.annee_3.text()	
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(24)
                champ_travaux_realises = readline(39)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_ligne_modele'"""
								
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_length_m)
                cur.execute(SQL_trigger_length_km)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
					#*********Point
                if 	self.dlg.annee_3.text() == 'aaaa' or self.dlg.annee_3.text() == '':
					tablename = schema + "_travaux_realises_point"					
                else :
					tablename = schema + "_travaux_realises_point_" + self.dlg.annee_3.text()	
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(25)
                champ_travaux_realises = readline(40)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_point_modele'"""
								
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_coordonnees)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table travaux prevus
            if self.dlg.couche_travaux_prevus.isChecked():
					#**********Poly
                if 	self.dlg.annee_5.text() == 'aaaa' or self.dlg.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_poly"					
                else :
					tablename = schema + "_travaux_prevus_poly_" + self.dlg.annee_5.text()						
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(26)
                champ_travaux_prevus = readline(43)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_poly_modele'"""
				
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#**********ligne
                if 	self.dlg.annee_5.text() == 'aaaa' or self.dlg.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_ligne"					
                else :
					tablename = schema + "_travaux_prevus_ligne_" + self.dlg.annee_5.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(27)
                champ_travaux_prevus = readline(44)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_ligne_modele'"""
								
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_length_m)
                cur.execute(SQL_trigger_length_km)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#**********point
                if 	self.dlg.annee_5.text() == 'aaaa' or self.dlg.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_point"					
                else :
					tablename = schema + "_travaux_prevus_point_" + self.dlg.annee_5.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(28)
                champ_travaux_prevus = readline(45)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_point_modele'"""
								
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_coordonnees)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)
				
                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table vierge
            if self.dlg.couche_vierge.isChecked():
                if 	self.dlg.annee_4.text() == 'aaaa' or self.dlg.annee_4.text() == '':
					tablename = schema + "_" + self.dlg.nom_couche_vierge.text().lower()				
                else :
					tablename = schema + "_" + self.dlg.nom_couche_vierge.text().lower() + "_" + self.dlg.annee_4.text()			
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(29)                
                champ_viergePolygone = readline(48)
                champ_viergeLigne = readline(49)
                champ_viergePoint = readline(50)

                if self.dlg.couche_vierge_point.isChecked() == 1 :
                    champ_vierge = champ_viergePoint

                if self.dlg.couche_vierge_ligne.isChecked() == 1 :
                    champ_vierge = champ_viergeLigne

                if self.dlg.couche_vierge_polygone.isChecked() == 1 :
                    champ_vierge = champ_viergePolygone                    

                SQL_vierge = "CREATE TABLE " + schema + "."+ tablename + champ_vierge
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"

                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"				
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"				
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"				

                cur.execute(SQL_vierge)
                cur.execute(SQL_pkey)
				
                if self.dlg.couche_vierge_point.isChecked() == 1 :
					cur.execute(SQL_trigger_coordonnees)

                if self.dlg.couche_vierge_ligne.isChecked() == 1 :
					cur.execute(SQL_trigger_length_m)
					cur.execute(SQL_trigger_length_km)					

                if self.dlg.couche_vierge_polygone.isChecked() == 1 :
					cur.execute(SQL_trigger_area_m2)
					cur.execute(SQL_trigger_area_ha)
					
                con.commit()                
           
                ### Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            else :
                con.commit()
                
            con.close()
            pass

		### Outil Aide
    def doHelp(self):
        webbrowser.open("http://lien.vers.plateformesig_tutos/")

		### Outil Ajout de nouvelles couche a un dossier		
    def ajout(self):
        import psycopg2
		
        config = "//chemin/fichier/config.txt" # Chemin du fichier config		
                # Fonction de lecture des lignes du fichier config		
        def readline(n):
          with open(config, "r") as f:
            for lineno, line in enumerate(f):
              if lineno == n:
                return line.strip() # Permet d'enlever les retours chariots
				
        host = readline(10)				
        port = readline(12)				
        dbname = readline(14)				
        user = readline(16)				
        password = readline(18)
		
        con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password)
        cur = con.cursor()
					# Creation de la liste des schemas de la base de donnees
        SQL = """WITH list_schema AS (
	SELECT catalog_name, schema_name
            FROM information_schema.schemata
            WHERE schema_name <> 'information_schema'
            AND schema_name !~ E'^pg_'
            ORDER BY schema_name
            )

        SELECT string_agg(schema_name,',')
            FROM list_schema
            GROUP BY catalog_name"""

        cur.execute(SQL)

        list_brut = str(cur.next())

        list = list_brut [3:-3]
        listItems = list.split(",")

        con.close()
        
        self.dlgAjout.ui.schema.clear()
        self.dlgAjout.ui.schema.addItems(listItems)
        self.dlgAjout.ui.schema.setCurrentIndex(-1) # Pour ne pas commencer la liste au premier schema
		
        # show the dialog
        self.dlgAjout.show()
        # Run the dialog event loop
        result = self.dlgAjout.exec_()
        # See if OK was pressed
        if result == 1:
#******************************debut script*********************************
            ### config.txt
            config = "//chemin/fichier/config.txt" # Chemin du fichier config

                # Fonction de lecture des lignes du fichier config
            def readline(n):
              with open(config, "r") as f:
                for lineno, line in enumerate(f):
                  if lineno == n:
                    return line.strip() # Permet d'enlever les retours chariots

                # Recuperation des donnees
            host = readline(10)
            port = readline(12)
            dbname = readline(14)
            user = readline(16)
            password = readline(18)
			
            con = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password)
            cur = con.cursor()
			
            if self.dlgAjout.ui.schema.currentIndex() == -1 :
				QMessageBox.warning(None, "Oups :", "Veuillez choisir un nom de dossier.")
				return			
			
            schema = self.dlgAjout.ui.schema.currentText()
			
            ### Creation de la table contour
            if self.dlgAjout.ui.couche_contour.isChecked(): # Verifie si la checkbox est cochee
                if 	self.dlgAjout.ui.annee_1.text() == 'aaaa' or self.dlgAjout.ui.annee_1.text() == '':
					tablename = schema + "_contour"					
                else :
					tablename = schema + "_contour_" + self.dlgAjout.ui.annee_1.text()	
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(21)
                champ_contour = readline(32)

                SQL_contour = "CREATE TABLE " + schema + "."+ tablename + champ_contour
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'contour_modele'"""
								
                cur.execute(SQL_contour)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
                
            ### Creation de la table habitat
            if self.dlgAjout.ui.couche_habitat.isChecked():
                if 	self.dlgAjout.ui.annee_2.text() == 'aaaa' or self.dlgAjout.ui.annee_2.text() == '':
					tablename = schema + "_habitat"					
                else :
					tablename = schema + "_habitat_" + self.dlgAjout.ui.annee_2.text()	
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(22)
                champ_habitat = readline(35)

                SQL_habitat = "CREATE TABLE " + schema + "."+ tablename + champ_habitat
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
                SQL_trigger_concat_cd_cb = "CREATE TRIGGER concat_cd_cb" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.concat_cd_cb();"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'habitat_modele'"""
								
                cur.execute(SQL_habitat)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)
                cur.execute(SQL_trigger_concat_cd_cb)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table travaux realises
            if self.dlgAjout.ui.couche_travaux_realises.isChecked():
					#******Poly
                if 	self.dlgAjout.ui.annee_3.text() == 'aaaa' or self.dlgAjout.ui.annee_3.text() == '':
					tablename = schema + "_travaux_realises_poly"					
                else :
					tablename = schema + "_travaux_realises_poly_" + self.dlgAjout.ui.annee_3.text()						
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(23)
                champ_travaux_realises = readline(38)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_poly_modele'"""
								
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#*********Ligne
                if 	self.dlgAjout.ui.annee_3.text() == 'aaaa' or self.dlgAjout.ui.annee_3.text() == '':
					tablename = schema + "_travaux_realises_ligne"					
                else :
					tablename = schema + "_travaux_realises_ligne_" + self.dlgAjout.ui.annee_3.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(24)
                champ_travaux_realises = readline(39)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_ligne_modele'"""
				
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_length_m)
                cur.execute(SQL_trigger_length_km)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
					#*********Point
                if 	self.dlgAjout.ui.annee_3.text() == 'aaaa' or self.dlgAjout.ui.annee_3.text() == '':
					tablename = schema + "_travaux_realises_point"					
                else :
					tablename = schema + "_travaux_realises_point_" + self.dlgAjout.ui.annee_3.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(25)
                champ_travaux_realises = readline(40)

                SQL_travaux_realises = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_realises
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_realises_point_modele'"""
				
                cur.execute(SQL_travaux_realises)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_coordonnees)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table travaux prevus
            if self.dlgAjout.ui.couche_travaux_prevus.isChecked():
					#**********Poly
                if 	self.dlgAjout.ui.annee_5.text() == 'aaaa' or self.dlgAjout.ui.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_poly"					
                else :
					tablename = schema + "_travaux_prevus_poly_" + self.dlgAjout.ui.annee_5.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(26)
                champ_travaux_prevus = readline(43)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_poly_modele'"""
				
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_area_m2)
                cur.execute(SQL_trigger_area_ha)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#**********ligne
                if 	self.dlgAjout.ui.annee_5.text() == 'aaaa' or self.dlgAjout.ui.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_ligne"					
                else :
					tablename = schema + "_travaux_prevus_ligne_" + self.dlgAjout.ui.annee_5.text()
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(27)
                champ_travaux_prevus = readline(44)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_ligne_modele'"""
				
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_length_m)
                cur.execute(SQL_trigger_length_km)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")

					#**********point
                if 	self.dlgAjout.ui.annee_5.text() == 'aaaa' or self.dlgAjout.ui.annee_5.text() == '':
					tablename = schema + "_travaux_prevus_point"					
                else :
					tablename = schema + "_travaux_prevus_point_" + self.dlgAjout.ui.annee_5.text()					
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(28)
                champ_travaux_prevus = readline(45)

                SQL_travaux_prevus = "CREATE TABLE " + schema + "."+ tablename + champ_travaux_prevus
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"
                SQL_trigger_date_creation = "CREATE TRIGGER date_creation" + tablename + " BEFORE INSERT ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_creation();"				
                SQL_trigger_date_maj = "CREATE TRIGGER date_maj" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.date_maj();"
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"
				
                SQL_style =	"""INSERT INTO layer_styles (f_table_catalog, f_table_schema, f_table_name, f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, update_time) 
                SELECT f_table_catalog, '""" + schema + "', '" + tablename + """', f_geometry_column, stylename, styleqml, stylesld, useasdefault, "owner", ui, now() 
                FROM layer_styles
                WHERE description = 'travaux_prevus_point_modele'"""
				
                cur.execute(SQL_travaux_prevus)
                cur.execute(SQL_pkey)
                cur.execute(SQL_trigger_date_creation)
                cur.execute(SQL_trigger_date_maj)
                cur.execute(SQL_trigger_coordonnees)				
                cur.execute(SQL_style)	## Enregistrement du style (comme style par defaut) dans la table layer_styles
                
                con.commit()
            
                ## Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            ### Creation de la table vierge
            if self.dlgAjout.ui.couche_vierge.isChecked():
                if 	self.dlgAjout.ui.annee_4.text() == 'aaaa' or self.dlgAjout.ui.annee_4.text() == '':
					tablename = schema + "_" + self.dlgAjout.ui.nom_couche_vierge.text().lower()					
                else :
					tablename = schema + "_" + self.dlgAjout.ui.nom_couche_vierge.text().lower() + "_" + self.dlgAjout.ui.annee_4.text()			
                tablename_qgis = tablename[1:]  # Permet d'enlever le "_", ajouter a la premiere etape, dans qgis
                geom = readline(6)
                style = readline(29)                
                champ_viergePolygone = readline(48)
                champ_viergeLigne = readline(49)
                champ_viergePoint = readline(50)

                if self.dlgAjout.ui.couche_vierge_point.isChecked() == 1 :
                    champ_vierge = champ_viergePoint

                if self.dlgAjout.ui.couche_vierge_ligne.isChecked() == 1 :
                    champ_vierge = champ_viergeLigne

                if self.dlgAjout.ui.couche_vierge_polygone.isChecked() == 1 :
                    champ_vierge = champ_viergePolygone                    

                SQL_vierge = "CREATE TABLE " + schema + "."+ tablename + champ_vierge
                SQL_pkey =  "ALTER TABLE " + schema + "." + tablename + " ADD CONSTRAINT " + tablename + "_pkey" + " PRIMARY KEY (gid)"

                SQL_trigger_area_m2 = "CREATE TRIGGER area_m2" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_m2();"
                SQL_trigger_area_ha = "CREATE TRIGGER area_ha" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.area_ha();"				
                SQL_trigger_length_m = "CREATE TRIGGER length_m" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_m();"
                SQL_trigger_length_km = "CREATE TRIGGER length_km" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.length_km();"				
                SQL_trigger_coordonnees = "CREATE TRIGGER coordonnees" + tablename + " BEFORE INSERT OR UPDATE ON " + schema + "." + tablename + " FOR EACH ROW EXECUTE PROCEDURE ref.coordonnees();"				

                cur.execute(SQL_vierge)
                cur.execute(SQL_pkey)
				
                if self.dlgAjout.ui.couche_vierge_point.isChecked() == 1 :
					cur.execute(SQL_trigger_coordonnees)

                if self.dlgAjout.ui.couche_vierge_ligne.isChecked() == 1 :
					cur.execute(SQL_trigger_length_m)
					cur.execute(SQL_trigger_length_km)					

                if self.dlgAjout.ui.couche_vierge_polygone.isChecked() == 1 :
					cur.execute(SQL_trigger_area_m2)
					cur.execute(SQL_trigger_area_ha)
					
                con.commit()                
           
                ### Affichage de la table
                uri = QgsDataSourceURI()
                  # set host name, port, database name, username and password
                uri.setConnection(host ,port ,dbname ,user ,password)
                  # set database schema, table name, geometry column and optionaly subset (WHERE clause)
                uri.setDataSource(schema, tablename, geom)

                layer = self.iface.addVectorLayer(uri.uri(), tablename_qgis, "postgres")
				
            else :
                con.commit()
                
            con.close()
            pass