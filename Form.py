from PyQt4.QtCore import *
from PyQt4.QtGui import *
import psycopg2
import qgis

nameField = None
myDialog = None

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

## Connexion aux bd postgresql
con_qgis = psycopg2.connect("dbname="+ dbname + " user=" + user + " host=" + host + " password=" + password)
cur_qgis = con_qgis.cursor()

dbname_odk = 'odk_prod'
host_odk = readline(2)
port_odk = readline(4)

con_odk = psycopg2.connect("dbname="+ dbname_odk + " user=" + user + " host=" + host_odk + " port=" + port_odk + " password=" + password)
cur_odk = con_odk.cursor()

##############################################################
################ Formulaire Travaux Realises #################
##############################################################

def formTravROpen(dialog,layerid,featureid):
	## Connexion des objets du formulaire
	global myDialog
	myDialog = dialog
	buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
	
	global open
	open = dialog.findChild(QToolButton,"open")
	
	global list_action_filtre
	list_action_filtre = dialog.findChild(QListWidget,"list_action_filtre")	
	global combo_site
	combo_site = dialog.findChild(QComboBox,"site_nom_list")
	global combo_site_2
	combo_site_2 = dialog.findChild(QComboBox,"site_nom_list_2")
	global combo_groupe_gestion
	combo_groupe_gestion = dialog.findChild(QComboBox,"groupe_gestion_list")
	global combo_gestion_lib
	combo_gestion_lib = dialog.findChild(QComboBox,"gestion_lib_list")
	global combo_type_porte_outils
	combo_type_porte_outils = dialog.findChild(QComboBox,"type_porte_outils_list")
	global combo_type_outils
	combo_type_outils = dialog.findChild(QComboBox,"type_outils_list")
	global combo_type_prestation
	combo_type_prestation = dialog.findChild(QComboBox,"type_prestation_list")
	
	global id_odk
 	id_odk = dialog.findChild(QLineEdit,"id_odk")
	id_odk.setVisible(0)
	global site_nom
	site_nom = dialog.findChild(QLineEdit,"site_nom")
	site_nom.setVisible(0)
	global id_site
	id_site = dialog.findChild(QLineEdit,"id_site")
	global groupe_gestion
	groupe_gestion = dialog.findChild(QLineEdit,"groupe_gestion")
	groupe_gestion.setVisible(0)
	global gestion_lib
	gestion_lib = dialog.findChild(QLineEdit,"gestion_lib")
	gestion_lib.setVisible(0)
	global id_gestion
	id_gestion = dialog.findChild(QLineEdit,"id_gestion")
	id_gestion.setVisible(0)
	global type_porte_outils
	type_porte_outils = dialog.findChild(QLineEdit,"type_porte_outils")
	type_porte_outils.setVisible(0)
	global type_porte_outils_code
	type_porte_outils_code = dialog.findChild(QLineEdit,"type_porte_outils_code")
	type_porte_outils_code.setVisible(0)
	global type_outils
	type_outils = dialog.findChild(QLineEdit,"type_outils")
	type_outils.setVisible(0)
	global type_outils_code
	type_outils_code = dialog.findChild(QLineEdit,"type_outils_code")
	type_outils_code.setVisible(0)
	global type_prestation_code
	type_prestation_code = dialog.findChild(QLineEdit,"type_prestation_code")
	type_prestation_code.setVisible(0)
	global type_prestation
	type_prestation = dialog.findChild(QLineEdit,"type_prestation")
	type_prestation.setVisible(0)
	global nbpassages
	nbpassages = dialog.findChild(QLineEdit,"nbpassages")
	global commentaire
	commentaire = dialog.findChild(QPlainTextEdit,"commentaire")
	global problemes
	problemes = dialog.findChild(QPlainTextEdit,"problemes")
	global debouche
	debouche = dialog.findChild(QPlainTextEdit,"debouche")
	global quantite
	quantite = dialog.findChild(QPlainTextEdit,"quantite")
	global duree
	duree = dialog.findChild(QLineEdit,"duree")
	
	global datedebut
	datedebut = dialog.findChild(QLineEdit,"datedebut")
	global datefin
	datefin = dialog.findChild(QLineEdit,"datefin")
	
	global deux_mois
	deux_mois = dialog.findChild(QCheckBox,"deux_mois")	
	deux_mois.setChecked(1)
	global supr_filtre
	supr_filtre = dialog.findChild(QPushButton,"supr_filtre")	
	global class_alpha
	class_alpha = dialog.findChild(QRadioButton,"class_alpha")
	class_alpha.setChecked(1)
	global class_date
	class_date = dialog.findChild(QRadioButton,"class_date")
	global open
 	open = dialog.findChild(QToolButton,"open")
	
	# Generation des listes
	if deux_mois.isChecked() == 1:
		global list_action
		cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.datefin > current_date - interval '2 month' ORDER BY list_action")
		list_action = cur_odk.fetchall()
	else :
		global list_action
		cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises ORDER BY list_action")
		list_action = cur_odk.fetchall()
	global list_site
	cur_odk.execute("SELECT DISTINCT site_nom || ' | ' || site_id AS liste FROM odk_ref.sites ORDER BY liste")
	list_site = cur_odk.fetchall()
	global list_groupe_gestion
	cur_odk.execute("SELECT DISTINCT niveau3 AS liste FROM odk_ref.gestion ORDER BY liste")
	list_groupe_gestion = cur_odk.fetchall()
	global list_gestion_lib
	cur_odk.execute("SELECT DISTINCT type_gestion || ' | ' || code_gestion AS liste FROM odk_ref.gestion ORDER BY liste")
	list_gestion_lib = cur_odk.fetchall()
	global list_type_porte_outils
	cur_odk.execute("""SELECT DISTINCT "type_porte-outils"  || ' | ' || "code_porte-outils" AS liste FROM odk_ref.porteoutils ORDER BY liste""")
	list_type_porte_outils = cur_odk.fetchall()
	global list_type_outils
	cur_odk.execute("SELECT DISTINCT type_outils || ' | ' || code_outils AS liste FROM odk_ref.outils ORDER BY liste")
	list_type_outils = cur_odk.fetchall()
	global list_type_prestation
	cur_odk.execute("SELECT DISTINCT type_prestation || ' | ' || code_prestation AS liste FROM odk_ref.prestation ORDER BY liste")
	list_type_prestation = cur_odk.fetchall()
	
	CurrentLayer=qgis.utils.iface.activeLayer() # Definition de la couche courante
	if CurrentLayer.isEditable() == True: # indique quels elements sont editable dans le formulaire
		id_site.setEnabled(False)
		combo_site.setEnabled(True)
		combo_groupe_gestion.setEnabled(True)
		combo_gestion_lib.setEnabled(True)
		combo_type_porte_outils.setEnabled(True)
		combo_type_outils.setEnabled(True)
		combo_type_prestation.setEnabled(True)

	else:
		id_site.setEnabled(False)
		combo_site.setEnabled(False)
		combo_groupe_gestion.setEnabled(False)
		combo_gestion_lib.setEnabled(False)
		combo_type_porte_outils.setEnabled(False)
		combo_type_outils.setEnabled(False)
		combo_type_prestation.setEnabled(False)
		open.setVisible(0)
		
	#Affichage dun formulaire vierge a la premiere ouverture
	if id_odk.text() != "" and id_odk.text() != "NULL":
		myDialog.resize(701,726)
		
		#*****action
		list_action_filtre.clear()
		i = 0
		while i < len(list_action):
			list_action_filtre.addItems(list_action[i])
			i=i+1
			
		combo_site_2.clear()
		i = 0
		while i < len(list_site):
			combo_site_2.addItems(list_site[i])
			i=i+1		
		combo_site_2.setCurrentIndex(-1)		

	else :
		#*****action
		list_action_filtre.clear()
		i = 0
		while i < len(list_action):
			list_action_filtre.addItems(list_action[i])
			i=i+1
			
		combo_site_2.clear()
		i = 0
		while i < len(list_site):
			combo_site_2.addItems(list_site[i])
			i=i+1		
		combo_site_2.setCurrentIndex(-1)		
	# Recuperation de donnee deja saisie dans qgis
	#********site
	valeur_id_site = id_site.text()

	if valeur_id_site == "" or valeur_id_site == "NULL" :
		combo_site.clear()
		i = 0
		while i < len(list_site):
			combo_site.addItems(list_site[i])
			i=i+1		
		combo_site.setCurrentIndex(-1)
	
	else :
		cur_odk.execute("SELECT DISTINCT site_nom FROM odk_ref.sites WHERE site_id = '" + valeur_id_site + "'")
		id_site_filtre = cur_odk.fetchall()
		list_id_site_filtre = id_site_filtre[0][0]		
		
		combo_site.clear()
		i = 0
		j = -1
		
		while i < len(list_site):
			liste_site = list_site[i][0]
			combo_site.addItems(list_site[i])
			if list_id_site_filtre == liste_site[0:(liste_site.find('|') - 1)] :
				j = i
			i=i+1		
		combo_site.setCurrentIndex(j)
	
	#******groupe_gestion
	valeur_groupe_gestion = groupe_gestion.text()
	valeur_groupe_gestion_modif = valeur_groupe_gestion.replace("'","''")
	
	if valeur_groupe_gestion_modif == "" or valeur_groupe_gestion_modif == "NULL" :
		combo_groupe_gestion.clear()
		i = 0
		while i < len(list_groupe_gestion):
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			i=i+1		
		combo_groupe_gestion.setCurrentIndex(-1)
		
	else:		
		cur_odk.execute("SELECT DISTINCT niveau3 FROM odk_ref.gestion WHERE niveau3 = '" + valeur_groupe_gestion_modif + "'")
		groupe_gestion_filtre = cur_odk.fetchall()
		list_groupe_gestion_filtre = groupe_gestion_filtre[0][0]		
		
		combo_groupe_gestion.clear()
		i = 0
		j = -1
		
		while i < len(list_groupe_gestion):
			liste_groupe_gestion = list_groupe_gestion[i][0]
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			if list_groupe_gestion_filtre == liste_groupe_gestion :
				j = i
			i=i+1		
		combo_groupe_gestion.setCurrentIndex(j)
	
	#******gestion_lib
	valeur_id_gestion = id_gestion.text()
	
	if valeur_id_gestion == "" or valeur_id_gestion == "NULL" :
		combo_gestion_lib.clear()
		i = 0
		while i < len(list_gestion_lib):
			combo_gestion_lib.addItems(list_gestion_lib[i])
			i=i+1		
		combo_gestion_lib.setCurrentIndex(-1)
	
	else :
		cur_odk.execute("SELECT DISTINCT type_gestion FROM odk_ref.gestion WHERE code_gestion = '" + valeur_id_gestion + "'")
		gestion_lib_filtre = cur_odk.fetchall()
		list_gestion_lib_filtre = gestion_lib_filtre[0][0]		
		
		combo_gestion_lib.clear()
		i = 0
		j = -1
		
		while i < len(list_gestion_lib):
			liste_gestion_lib = list_gestion_lib[i][0]
			combo_gestion_lib.addItems(list_gestion_lib[i])
			if list_gestion_lib_filtre == liste_gestion_lib[0:(liste_gestion_lib.find('|') - 1)] :
				j = i
			i=i+1		
		combo_gestion_lib.setCurrentIndex(j)

	#******type_porte_outils
	valeur_type_porte_outils_code = type_porte_outils_code.text()

	if valeur_type_porte_outils_code == "" or valeur_type_porte_outils_code == "NULL" :
		combo_type_porte_outils.clear()
		i = 0
		while i < len(list_type_porte_outils):
			combo_type_porte_outils.addItems(list_type_porte_outils[i])
			i=i+1		
		combo_type_porte_outils.setCurrentIndex(-1)
	
	else:
		cur_odk.execute("""SELECT DISTINCT "type_porte-outils" FROM odk_ref.porteoutils WHERE "code_porte-outils" = '""" + valeur_type_porte_outils_code + "'")
		type_porte_outils_filtre = cur_odk.fetchall()
		list_type_porte_outils_filtre = type_porte_outils_filtre[0][0]		
		
		combo_type_porte_outils.clear()
		i = 0
		j = -1
		
		while i < len(list_type_porte_outils):
			liste_type_porte_outils = list_type_porte_outils[i][0]
			combo_type_porte_outils.addItems(list_type_porte_outils[i])
			if list_type_porte_outils_filtre == liste_type_porte_outils[0:(liste_type_porte_outils.find('|') - 1)] :
				j = i
			i=i+1		
		combo_type_porte_outils.setCurrentIndex(j)
	
	#******type_outils
	valeur_type_outils_code = type_outils_code.text()

	if valeur_type_outils_code == "" or valeur_type_outils_code == "NULL" :
		combo_type_outils.clear()
		i = 0
		while i < len(list_type_outils):
			combo_type_outils.addItems(list_type_outils[i])
			i=i+1		
		combo_type_outils.setCurrentIndex(-1)
	
	else:
		cur_odk.execute("SELECT DISTINCT type_outils FROM odk_ref.outils WHERE code_outils = '" + valeur_type_outils_code + "'")
		type_outils_filtre = cur_odk.fetchall()
		list_type_outils_filtre = type_outils_filtre[0][0]		
		
		combo_type_outils.clear()
		i = 0
		j = -1
		
		while i < len(list_type_outils):
			liste_type_outils = list_type_outils[i][0]
			combo_type_outils.addItems(list_type_outils[i])
			if list_type_outils_filtre == liste_type_outils[0:(liste_type_outils.find('|') - 1)] :
				j = i
			i=i+1		
		combo_type_outils.setCurrentIndex(j)
		
	#******type_prestation
	valeur_type_prestation_code = type_prestation_code.text()

	if valeur_type_prestation_code == "" or valeur_type_prestation_code == "NULL" :
		combo_type_prestation.clear()
		i = 0
		while i < len(list_type_prestation):
			combo_type_prestation.addItems(list_type_prestation[i])
			i=i+1		
		combo_type_prestation.setCurrentIndex(-1)
	
	else:
		cur_odk.execute("SELECT DISTINCT type_prestation FROM odk_ref.prestation WHERE code_prestation = '" + valeur_type_prestation_code + "'")
		type_prestation_filtre = cur_odk.fetchall()
		list_type_prestation_filtre = type_prestation_filtre[0][0]		
		
		combo_type_prestation.clear()
		i = 0
		j = -1
		
		while i < len(list_type_prestation):
			liste_type_prestation = list_type_prestation[i][0]
			combo_type_prestation.addItems(list_type_prestation[i])
			if list_type_prestation_filtre == liste_type_prestation[0:(liste_type_prestation.find('|') - 1)] :
				j = i
			i=i+1		
		combo_type_prestation.setCurrentIndex(j)
	
	#*****date	
	valeur_datedebut = datedebut.text()
	if valeur_datedebut == "" or valeur_datedebut == "NULL" :
		datedebut.setText('yyyy-MM-dd')
	else :
		datedebut.setText(valeur_datedebut)
		
	valeur_datefin = datefin.text()
	if valeur_datefin == "" or valeur_datefin == "NULL" :
		datefin.setText('yyyy-MM-dd')
	else :
		datefin.setText(valeur_datefin)

	QObject.connect(list_action_filtre, SIGNAL("currentRowChanged(int)"), liaison_combo)
	QObject.connect(list_action_filtre, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), change_action)		# Lance la fonction change_action qui permet de recuperer le id_odk de l action dans odk

	QObject.connect(deux_mois, SIGNAL("clicked()"), filtre_list_action)
	QObject.connect(combo_site_2, SIGNAL("currentIndexChanged(int)"), filtre_list_action)
	QObject.connect(class_date, SIGNAL("clicked()"), filtre_list_action)
	QObject.connect(class_alpha, SIGNAL("clicked()"), filtre_list_action)
	QObject.connect(supr_filtre, SIGNAL("clicked()"), filtre_supr)
	
	QObject.connect(combo_site, SIGNAL("currentIndexChanged(int)"), change_site)
	QObject.connect(combo_groupe_gestion, SIGNAL("currentIndexChanged(int)"), change_groupe_gestion)
	QObject.connect(combo_groupe_gestion, SIGNAL("currentIndexChanged(int)"), liaison_combo)
	QObject.connect(combo_gestion_lib, SIGNAL("currentIndexChanged(int)"), change_gestion_lib)
	QObject.connect(combo_type_porte_outils, SIGNAL("currentIndexChanged(int)"), change_type_porte_outils)
	QObject.connect(combo_type_outils, SIGNAL("currentIndexChanged(int)"), change_type_outils)
	QObject.connect(combo_type_prestation, SIGNAL("currentIndexChanged(int)"), change_type_prestation)
	
	QObject.connect(open, SIGNAL("clicked()"), fct_agrandir)
	
# Fonction pour supprimer les filtres de la liste des travaux saisis dans odk	
def filtre_supr():	
	deux_mois.setChecked(0)
	class_alpha.setChecked(1)
	combo_site_2.setCurrentIndex(-1)
	global list_action
	cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises ORDER BY list_action")
	list_action = cur_odk.fetchall()
	
	list_action_filtre.clear()
	i = 0
	while i < len(list_action):
		list_action_filtre.addItems(list_action[i])
		i=i+1
# Focntion pour filtrer les travaux saisis dans odk	
def filtre_list_action():
	text_filtre_site = combo_site_2.currentText()
	id_filtre_site = text_filtre_site[(text_filtre_site.find('|') + 2):]
	
	if id_filtre_site != "" and id_filtre_site != "NULL":	# Par site
		if class_alpha.isChecked() == 1:					# Par ordre alphabetique
			if deux_mois.isChecked() == 1:					# Pour les deux derniers mois
				global list_action
				cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_site = '" + id_filtre_site + "' AND odk_ref.travaux_realises.datefin > current_date - interval '2 month' ORDER BY list_action")
				list_action = cur_odk.fetchall()
			else :
				global list_action
				cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_site = '" + id_filtre_site + "' ORDER BY list_action")
				list_action = cur_odk.fetchall()	

		elif class_date.isChecked() == 1:				# Par date decroissante
			if deux_mois.isChecked() == 1:
				global list_action
				cur_odk.execute("SELECT DISTINCT substring(datefin::text from 0 for 11) ||' | '|| site_nom ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_site = '" + id_filtre_site + "' AND odk_ref.travaux_realises.datefin > current_date - interval '2 month' ORDER BY list_action DESC")
				list_action = cur_odk.fetchall()
			else :
				global list_action
				cur_odk.execute("SELECT DISTINCT substring(datefin::text from 0 for 11) ||' | '|| site_nom ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_site = '" + id_filtre_site + "' ORDER BY list_action")
				list_action = cur_odk.fetchall()
	else :
		if class_alpha.isChecked() == 1:
			if deux_mois.isChecked() == 1:
				global list_action
				cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.datefin > current_date - interval '2 month' ORDER BY list_action")
				list_action = cur_odk.fetchall()
			else :
				global list_action
				cur_odk.execute("SELECT DISTINCT site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises ORDER BY list_action")
				list_action = cur_odk.fetchall()	

		elif class_date.isChecked() == 1:
			if deux_mois.isChecked() == 1:
				global list_action
				cur_odk.execute("SELECT DISTINCT substring(datefin::text from 0 for 11) ||' | '|| site_nom ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.datefin > current_date - interval '2 month' ORDER BY list_action DESC")
				list_action = cur_odk.fetchall()
			else :
				global list_action
				cur_odk.execute("SELECT DISTINCT substring(datefin::text from 0 for 11) ||' | '|| site_nom ||' | '|| gestion_lib AS list_action FROM odk_ref.travaux_realises ORDER BY list_action")
				list_action = cur_odk.fetchall()
	
	list_action_filtre.clear()
	i = 0
	while i < len(list_action):
		list_action_filtre.addItems(list_action[i])
		i=i+1	
	
	## Fonction qui lie les combo entre elles
def liaison_combo():
	text_combo_groupe_gestion = combo_groupe_gestion.currentText()
	text_combo_groupe_gestion_modif = text_combo_groupe_gestion.replace("'","''")
	
	cur_odk.execute("SELECT DISTINCT type_gestion || ' | ' || code_gestion AS liste FROM odk_ref.gestion WHERE niveau3 = '" + text_combo_groupe_gestion_modif + "' ORDER BY liste")
	gestion_lib_filtre = cur_odk.fetchall()
		
	combo_gestion_lib.clear()
	i = 0
	while i < len(gestion_lib_filtre):
		combo_gestion_lib.addItems(gestion_lib_filtre[i])
		i=i+1		
	combo_gestion_lib.setCurrentIndex(-1)
	
	## Fonction qui recupere toute les donnees de la table odk_trav_realises pour l action choisie
def change_action():
	text_list_action_filtre = list_action_filtre.currentItem().text()
	text_list_action_filtre_modif = text_list_action_filtre.replace("'","''")
	
	if class_alpha.isChecked() == 1:
	## Recupere le id_odk de l action selectionee
		cur_odk.execute("SELECT DISTINCT id_odk FROM odk_ref.travaux_realises WHERE site_nom ||' | '|| substring(datefin::text from 0 for 11) ||' | '|| gestion_lib LIKE '" + text_list_action_filtre_modif + "'")

	elif class_date.isChecked() == 1: 
		cur_odk.execute("SELECT DISTINCT id_odk FROM odk_ref.travaux_realises WHERE substring(datefin::text from 0 for 11) ||' | '|| site_nom ||' | '|| gestion_lib LIKE '" + text_list_action_filtre_modif + "'")
		
	list_id_odk = cur_odk.fetchall()
	text_id_odk = list_id_odk[0][0]
	id_odk.setText(text_id_odk)
	
	# Recupere site
	cur_odk.execute("SELECT DISTINCT id_site FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	id_site_filtre = cur_odk.fetchall()
	valeur_id_site = id_site_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(id_site) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_site.clear()
		i = 0
		while i < len(list_site):
			combo_site.addItems(list_site[i])
			i=i+1		
		combo_site.setCurrentIndex(-1)
	
	else:
		id_site.setText(valeur_id_site)
		
		cur_odk.execute("SELECT DISTINCT site_nom FROM odk_ref.sites WHERE site_id = '" + valeur_id_site + "'")
		id_site_filtre = cur_odk.fetchall()
		valeur_id_site = id_site_filtre[0][0]

		combo_site.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_site):
			liste_site = list_site[i][0]
			combo_site.addItems(list_site[i])
			if valeur_id_site == liste_site[0:(liste_site.find('|') - 1)] :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_site.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j

	## Recupere groupe_gestion
	cur_odk.execute("SELECT DISTINCT code_niveau3 FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	code_niveau3_filtre = cur_odk.fetchall()
	valeur_code_niveau3 = code_niveau3_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(code_niveau3) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_groupe_gestion.clear()
		i = 0
		while i < len(list_groupe_gestion):
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			i=i+1		
		combo_groupe_gestion.setCurrentIndex(-1)
	
	else:
		cur_odk.execute("SELECT DISTINCT niveau3 AS liste FROM odk_ref.gestion WHERE code_niveau3 = '" + valeur_code_niveau3 + "' GROUP BY liste")
		groupe_gestion_filtre = cur_odk.fetchall()
		valeur_groupe_gestion = groupe_gestion_filtre[0][0]

		combo_groupe_gestion.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_groupe_gestion):
			liste_groupe_gestion = list_groupe_gestion[i][0]
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			if valeur_groupe_gestion == liste_groupe_gestion :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_groupe_gestion.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j
	
	## Recupere gestion_lib
	cur_odk.execute("SELECT DISTINCT id_gestion FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	id_gestion_filtre = cur_odk.fetchall()
	valeur_id_gestion = id_gestion_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(id_gestion) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_gestion_lib.clear()
		i = 0
		while i < len(list_gestion_lib):
			combo_gestion_lib.addItems(list_gestion_lib[i])
			i=i+1		
		combo_gestion_lib.setCurrentIndex(-1)
	
	else:
		id_gestion.setText(valeur_id_gestion)
		
		cur_odk.execute("SELECT DISTINCT type_gestion FROM odk_ref.gestion WHERE code_gestion = '" + valeur_id_gestion + "'")
		gestion_lib_filtre = cur_odk.fetchall()
		valeur_gestion_lib = gestion_lib_filtre[0][0]

		combo_gestion_lib.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_gestion_lib):
			liste_gestion_lib = list_gestion_lib[i][0]
			combo_gestion_lib.addItems(list_gestion_lib[i])
			if valeur_gestion_lib == liste_gestion_lib[0:(liste_gestion_lib.find('|') - 1)] :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_gestion_lib.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j
	
	## Recupere type_porte_outils
	cur_odk.execute("SELECT DISTINCT type_porte_outils_code FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	type_porte_outils_code_filtre = cur_odk.fetchall()
	valeur_type_porte_outils_code = type_porte_outils_code_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(type_porte_outils_code) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_type_porte_outils.clear()
		i = 0
		while i < len(list_type_porte_outils):
			combo_type_porte_outils.addItems(list_type_porte_outils[i])
			i=i+1		
		combo_type_porte_outils.setCurrentIndex(-1)
	
	else:
		type_porte_outils_code.setText(valeur_type_porte_outils_code)
		
		cur_odk.execute("""SELECT DISTINCT "type_porte-outils" FROM odk_ref.porteoutils WHERE "code_porte-outils" = '""" + valeur_type_porte_outils_code + "'")
		type_porte_outils_filtre = cur_odk.fetchall()
		valeur_type_porte_outils = type_porte_outils_filtre[0][0]

		combo_type_porte_outils.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_type_porte_outils):
			liste_type_porte_outils = list_type_porte_outils[i][0]
			combo_type_porte_outils.addItems(list_type_porte_outils[i])
			if valeur_type_porte_outils == liste_type_porte_outils[0:(liste_type_porte_outils.find('|') - 1)] :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_type_porte_outils.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j
	
	## Recupere type_outils
	cur_odk.execute("SELECT DISTINCT type_outils_code FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	type_outils_code_filtre = cur_odk.fetchall()
	valeur_type_outils_code = type_outils_code_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(type_outils_code) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_type_outils.clear()
		i = 0
		while i < len(list_type_outils):
			combo_type_outils.addItems(list_type_outils[i])
			i=i+1		
		combo_type_outils.setCurrentIndex(-1)
	
	else :
		type_outils_code.setText(valeur_type_outils_code)

		cur_odk.execute("SELECT DISTINCT type_outils FROM odk_ref.outils WHERE code_outils = '" + valeur_type_outils_code + "'")
		type_outils_filtre = cur_odk.fetchall()
		valeur_type_outils = type_outils_filtre[0][0]

		combo_type_outils.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_type_outils):
			liste_type_outils = list_type_outils[i][0]
			combo_type_outils.addItems(list_type_outils[i])
			if valeur_type_outils == liste_type_outils[0:(liste_type_outils.find('|') - 1)] :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_type_outils.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j
	
	## Recupere type_prestation
	cur_odk.execute("SELECT DISTINCT type_prestation_code FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	type_prestation_code_filtre = cur_odk.fetchall()
	valeur_type_prestation_code = type_prestation_code_filtre[0][0]
	
	cur_odk.execute("SELECT DISTINCT count(type_prestation_code) FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk = '" + text_id_odk + "'")
	count = cur_odk.fetchone()
	if count[0] == 0 :
		combo_type_prestation.clear()
		i = 0
		while i < len(list_type_prestation):
			combo_type_prestation.addItems(list_type_prestation[i])
			i=i+1		
		combo_type_prestation.setCurrentIndex(-1)
		
	else :	
		type_prestation_code.setText(valeur_type_prestation_code)

		cur_odk.execute("SELECT DISTINCT type_prestation FROM odk_ref.prestation WHERE code_prestation = '" + valeur_type_prestation_code + "'")
		type_prestation_filtre = cur_odk.fetchall()
		valeur_type_prestation = type_prestation_filtre[0][0]

		combo_type_prestation.clear() # vide la liste de la comboBox
		i = 0
		j = -1

		while i < len(list_type_prestation):
			liste_type_prestation = list_type_prestation[i][0]
			combo_type_prestation.addItems(list_type_prestation[i])
			if valeur_type_prestation == liste_type_prestation[0:(liste_type_prestation.find('|') - 1)] :
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_type_prestation.setCurrentIndex(j) # CurrentIndex permet de faire commencer la liste au point j
	
	## Recupere nbpassages
	cur_odk.execute("SELECT DISTINCT nbpassages FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "'")
	nbpassages_filtre = cur_odk.fetchall()
	valeur_nbpassages = nbpassages_filtre[0][0]
	nbpassages.setText(str(valeur_nbpassages))
	
	## Recupere commentaire
	cur_odk.execute("SELECT DISTINCT commentaire as liste FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "' ORDER BY liste")
	commentaire_filtre = cur_odk.fetchall()
	valeur_commentaire = commentaire_filtre[0][0]
	commentaire.setPlainText(valeur_commentaire)
	
	## Recupere problemes
	cur_odk.execute("SELECT DISTINCT problemes as liste FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "' ORDER BY liste")
	problemes_filtre = cur_odk.fetchall()
	valeur_problemes = problemes_filtre[0][0]
	problemes.setPlainText(valeur_problemes)
	
	## Recupere debouche
	cur_odk.execute("SELECT DISTINCT debouche as liste FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "' ORDER BY liste")
	debouche_filtre = cur_odk.fetchall()
	valeur_debouche = debouche_filtre[0][0]
	debouche.setPlainText(valeur_debouche)
	
	## Recupere quantite
	cur_odk.execute("SELECT DISTINCT quantite as liste FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "' ORDER BY liste")
	quantite_filtre = cur_odk.fetchall()
	valeur_quantite = quantite_filtre[0][0]
	quantite.setPlainText(valeur_quantite)
	
	## Recupere datedebut
	cur_odk.execute("SELECT DISTINCT datedebut FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "'")
	datedebut_filtre = cur_odk.fetchall()
	valeur_datedebut = str(datedebut_filtre[0][0])
	text_datedebut = valeur_datedebut[0:(valeur_datedebut.find(' ') -0)]
	datedebut.setText(text_datedebut)
	
	## Recupere datefin
	cur_odk.execute("SELECT DISTINCT datefin FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "'")
	datefin_filtre = cur_odk.fetchall()
	valeur_datefin = str(datefin_filtre[0][0])
	text_datefin = valeur_datefin[0:(valeur_datefin.find(' ') -0)]
	datefin.setText(text_datefin)
	
	## Recupere duree
	cur_odk.execute("SELECT DISTINCT duree as liste FROM odk_ref.travaux_realises WHERE odk_ref.travaux_realises.id_odk LIKE '" + text_id_odk + "' ORDER BY liste")
	duree_filtre = cur_odk.fetchall()
	valeur_duree = duree_filtre[0][0]
	duree.setText(str(valeur_duree))

def change_site():
	text_combo_site = combo_site.currentText()
	site_nom.setText(text_combo_site[0:(text_combo_site.find('|') - 1)])
	id_site.setText(text_combo_site[(text_combo_site.find('|') + 2):])	

def change_groupe_gestion():
	text_combo_groupe_gestion = combo_groupe_gestion.currentText()
	groupe_gestion.setText(text_combo_groupe_gestion)
	
def change_gestion_lib():
	text_combo_gestion_lib = combo_gestion_lib.currentText()
	gestion_lib.setText(text_combo_gestion_lib[0:(text_combo_gestion_lib.find('|') - 1)])
	id_gestion.setText(text_combo_gestion_lib[(text_combo_gestion_lib.find('|') + 2):])

def change_type_porte_outils():
	text_combo_type_porte_outils = combo_type_porte_outils.currentText()
	type_porte_outils.setText(text_combo_type_porte_outils[0:(text_combo_type_porte_outils.find('|') - 1)])
	type_porte_outils_code.setText(text_combo_type_porte_outils[(text_combo_type_porte_outils.find('|') + 2):])
	
def change_type_outils():
	text_combo_type_outils = combo_type_outils.currentText()
	type_outils.setText(text_combo_type_outils[0:(text_combo_type_outils.find('|') - 1)])
	type_outils_code.setText(text_combo_type_outils[(text_combo_type_outils.find('|') + 2):])
	
def change_type_prestation():
	text_combo_type_prestation = combo_type_prestation.currentText()
	type_prestation.setText(text_combo_type_prestation[0:(text_combo_type_prestation.find('|') - 1)])
	type_prestation_code.setText(text_combo_type_prestation[(text_combo_type_prestation.find('|') + 2):])
	
def fct_agrandir():
	if(myDialog.width() != 1263):
		myDialog.resize(1263,726)

	else:
		myDialog.resize(701,726)
	
##############################################################
################ Formulaire Travaux Prevus ###################
##############################################################	
	
def formTravPOpen(dialog,layerid,featureid):
	## Connexion des objets du formulaire
	global myDialog
	myDialog = dialog
	buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
	
	global combo_gestion_lib
	combo_gestion_lib = dialog.findChild(QComboBox,"gestion_lib_list")
	global combo_groupe_gestion
	combo_groupe_gestion = dialog.findChild(QComboBox,"groupe_gestion_list")
	
	global groupe_gestion
	groupe_gestion = dialog.findChild(QLineEdit,"groupe_gestion")
	groupe_gestion.setVisible(0)	
	global gestion_lib
	gestion_lib = dialog.findChild(QLineEdit,"gestion_lib")
	gestion_lib.setVisible(0)
	global id_gestion
	id_gestion = dialog.findChild(QLineEdit,"id_gestion")
	id_gestion.setVisible(0)
	global commentaire
	commentaire = dialog.findChild(QPlainTextEdit,"commentaire")
	global datedebut
	datedebut = dialog.findChild(QLineEdit,"datedebut")
	global datefin
	datefin = dialog.findChild(QLineEdit,"datefin")
	global surface_ha
	surface_ha = dialog.findChild(QLineEdit,"surface_ha")
	global surface_m2
	surface_m2 = dialog.findChild(QLineEdit,"surface_m2")

	valeur_datedebut = datedebut.text()
	if valeur_datedebut == "" or valeur_datedebut == "NULL" :
		datedebut.setText('yyyy-MM-dd')
	else :
		datedebut.setText(valeur_datedebut)
		
	valeur_datefin = datefin.text()
	if valeur_datefin == "" or valeur_datefin == "NULL" :
		datefin.setText('yyyy-MM-dd')
	else :
		datefin.setText(valeur_datefin)
	
	# Generation des listes
	global list_gestion_lib
	cur_odk.execute("SELECT DISTINCT type_gestion || ' | ' || code_gestion AS liste FROM odk_ref.gestion ORDER BY liste")
	list_gestion_lib = cur_odk.fetchall()
	global list_groupe_gestion
	cur_odk.execute("SELECT DISTINCT niveau3 AS liste FROM odk_ref.gestion ORDER BY liste")
	list_groupe_gestion = cur_odk.fetchall()
	
	CurrentLayer=qgis.utils.iface.activeLayer() # Definition de la couche courante
	if CurrentLayer.isEditable() == True: # indique quels elements sont editable dans le formulaire
		combo_gestion_lib.setEnabled(True)
		combo_groupe_gestion.setEnabled(True)		
	else:
		combo_gestion_lib.setEnabled(False)
		combo_groupe_gestion.setEnabled(False)
	#Affichage dun formulaire vierge a la premiere ouverture
	#******groupe_gestion
	valeur_groupe_gestion = groupe_gestion.text()
	valeur_groupe_gestion_modif = valeur_groupe_gestion.replace("'","''")
	
	if valeur_groupe_gestion_modif == "" or valeur_groupe_gestion_modif == "NULL" :
		combo_groupe_gestion.clear()
		i = 0
		while i < len(list_groupe_gestion):
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			i=i+1		
		combo_groupe_gestion.setCurrentIndex(-1)
		
	else:		
		cur_odk.execute("SELECT DISTINCT niveau3 FROM odk_ref.gestion WHERE niveau3 = '" + valeur_groupe_gestion_modif + "'")
		groupe_gestion_filtre = cur_odk.fetchall()
		list_groupe_gestion_filtre = groupe_gestion_filtre[0][0]		
		
		combo_groupe_gestion.clear()
		i = 0
		j = -1
		
		while i < len(list_groupe_gestion):
			liste_groupe_gestion = list_groupe_gestion[i][0]
			combo_groupe_gestion.addItems(list_groupe_gestion[i])
			if list_groupe_gestion_filtre == liste_groupe_gestion :
				j = i
			i=i+1		
		combo_groupe_gestion.setCurrentIndex(j)
	
	#******gestion_lib
	valeur_id_gestion = id_gestion.text()
	
	if valeur_id_gestion == "" or valeur_id_gestion == "NULL" :
		combo_gestion_lib.clear()
		i = 0
		while i < len(list_gestion_lib):
			combo_gestion_lib.addItems(list_gestion_lib[i])
			i=i+1		
		combo_gestion_lib.setCurrentIndex(-1)
	
	else :
		cur_odk.execute("SELECT DISTINCT type_gestion FROM odk_ref.gestion WHERE code_gestion = '" + valeur_id_gestion + "'")
		gestion_lib_filtre = cur_odk.fetchall()
		list_gestion_lib_filtre = gestion_lib_filtre[0][0]		
		
		combo_gestion_lib.clear()
		i = 0
		j = -1
		
		while i < len(list_gestion_lib):
			liste_gestion_lib = list_gestion_lib[i][0]
			combo_gestion_lib.addItems(list_gestion_lib[i])
			if list_gestion_lib_filtre == liste_gestion_lib[0:(liste_gestion_lib.find('|') - 1)] :
				j = i
			i=i+1		
		combo_gestion_lib.setCurrentIndex(j)

	QObject.connect(combo_gestion_lib, SIGNAL("currentIndexChanged(int)"), change_gestion_lib)
	QObject.connect(combo_groupe_gestion, SIGNAL("currentIndexChanged(int)"), change_groupe_gestion)
	QObject.connect(combo_groupe_gestion, SIGNAL("currentIndexChanged(int)"), liaison_combo)

	## Fonction qui lie les combo entre elles
def liaison_combo():
	text_combo_groupe_gestion = combo_groupe_gestion.currentText()
	text_combo_groupe_gestion_modif = text_combo_groupe_gestion.replace("'","''")
	
	cur_odk.execute("SELECT DISTINCT type_gestion || ' | ' || code_gestion AS liste FROM odk_ref.gestion WHERE niveau3 = '" + text_combo_groupe_gestion_modif + "' ORDER BY liste")
	gestion_lib_filtre = cur_odk.fetchall()
		
	combo_gestion_lib.clear()
	i = 0
	while i < len(gestion_lib_filtre):
		combo_gestion_lib.addItems(gestion_lib_filtre[i])
		i=i+1		
	combo_gestion_lib.setCurrentIndex(-1)
	
def change_groupe_gestion():
	text_combo_groupe_gestion = combo_groupe_gestion.currentText()
	groupe_gestion.setText(text_combo_groupe_gestion)
	
def change_gestion_lib():
	text_combo_gestion_lib = combo_gestion_lib.currentText()
	gestion_lib.setText(text_combo_gestion_lib[0:(text_combo_gestion_lib.find('|') - 1)])
	id_gestion.setText(text_combo_gestion_lib[(text_combo_gestion_lib.find('|') + 2):])
	
	
##############################################################
#################### Formulaire Habitat ######################
##############################################################	
	

def formHabOpen(dialog,layerid,featureid):
	## con_qgisexion des objets du formulaire
	global myDialog
	myDialog = dialog
	myDialog.resize(520,555)
	buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
	
	global groupBox
	groupBox = dialog.findChild(QGroupBox,"groupBox")
	groupBox.resize(501,151)
	global groupBox_2
	groupBox_2 = dialog.findChild(QGroupBox,"groupBox_2")
	groupBox_2.resize(501,90)
	
	global agrandir_01
	agrandir_01 = dialog.findChild(QToolButton,"agrandir_01")
	global agrandir_02
	agrandir_02 = dialog.findChild(QToolButton,"agrandir_02")
	global combo_01
	combo_01 = dialog.findChild(QComboBox,"lb_cb97_fr_list_01")
	global libelle_01
 	libelle_01 = dialog.findChild(QLineEdit,"lb_cb97_fr_01")
	libelle_01.setVisible(0)
	global code_01
 	code_01 = dialog.findChild(QLineEdit,"cd_cb_01")
	code_01.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
	
	global combo_02
	combo_02 = dialog.findChild(QComboBox,"lb_cb97_fr_list_02")
	global libelle_02
 	libelle_02 = dialog.findChild(QLineEdit,"lb_cb97_fr_02")
	libelle_02.setVisible(0)
	global code_02
 	code_02 = dialog.findChild(QLineEdit,"cd_cb_02")
	
	global combo_03
	combo_03 = dialog.findChild(QComboBox,"lb_cb97_fr_list_03")
	global libelle_03
 	libelle_03 = dialog.findChild(QLineEdit,"lb_cb97_fr_03")
	libelle_03.setVisible(0)
	global code_03
 	code_03 = dialog.findChild(QLineEdit,"cd_cb_03")
		
	global surface_m2
 	surface_m2 = dialog.findChild(QLineEdit,"surface_m2")
	global surface_ha
 	surface_ha = dialog.findChild(QLineEdit,"surface_ha")
	global milieu_code
 	milieu_code = dialog.findChild(QLineEdit,"milieu_code")
	milieu_code.resize(350,20)
	milieu_code.setVisible(0)
	global milieu_code_label
 	milieu_code_label = dialog.findChild(QLabel,"milieu_code_label")
	milieu_code_label.setVisible(0)
	global milieu_libelle
 	milieu_libelle = dialog.findChild(QLineEdit,"milieu_libelle")
	milieu_libelle.resize(395,20)
	global commentaire
	commentaire = dialog.findChild(QPlainTextEdit,"commentaire")
	commentaire.resize(485,60)
	
	global items # Generation de liste deroulante
	cur_qgis.execute("SELECT DISTINCT cd_cb ||' : '|| lb_cb97_fr as liste FROM ref.typo_corine_biotopes ORDER BY liste")
	items = cur_qgis.fetchall()
	
	cur_qgisrentLayer=qgis.utils.iface.activeLayer() # Definition de la couche courante
	
	## Recuperation de la valeur lorsque le champ est deja saisie
	#***01
	if libelle_01.text() != "" and libelle_01.text() != "NULL":
		valeur = code_01.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste") # recupere la valeur du referentiel correspondant a la valeur saisie
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0] # sauvegarde la valeur recuperer dans une variable
		
		combo_01.clear() # vide la liste de la comboBox
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(items):
			liste = items[i][0]
			combo_01.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]: # ou coupe au niveau des deux point et enleve 1 caractere
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		combo_01.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j
		
		if cur_qgisrentLayer.isEditable() == True: # indique quels elements sont editable dans le formulaire
			combo_01.setEnabled(True)
			combo_02.setEnabled(True)
			combo_03.setEnabled(True)
			surface_m2.setEnabled(False)
			surface_ha.setEnabled(False)
			milieu_code.setEnabled(False)
			milieu_libelle.setEnabled(True)

		else:
			combo_01.setEnabled(False)
			combo_02.setEnabled(False)
			combo_03.setEnabled(False)
			surface_m2.setEnabled(False)
			surface_ha.setEnabled(False)
			milieu_code.setEnabled(False)
			milieu_libelle.setEnabled(False)

	else :
		combo_01.clear()
		i = 0
		while i < len(items):
			combo_01.addItems(items[i])
			i=i+1		
		combo_01.setCurrentIndex(-1)
		
		if cur_qgisrentLayer.isEditable() == True:
			combo_01.setEnabled(True)
			combo_02.setEnabled(True)
			combo_03.setEnabled(True)
			surface_m2.setEnabled(False)
			surface_ha.setEnabled(False)
			milieu_code.setEnabled(False)
			milieu_libelle.setEnabled(True)

		else:
			combo_01.setEnabled(False)
			combo_02.setEnabled(False)
			combo_03.setEnabled(False)
			surface_m2.setEnabled(False)
			surface_ha.setEnabled(False)
			milieu_code.setEnabled(False)
			milieu_libelle.setEnabled(False)
	
	#***02
	if libelle_02.text() != "" and libelle_02.text() != "NULL":
		valeur = code_02.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste")
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0]
		
		combo_02.clear()
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(items):
			liste = items[i][0]
			combo_02.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]:
				j = i
			i=i+1			
		combo_02.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j
		
		myDialog.resize(790,455)
		groupBox.resize(771,151)
		groupBox_2.resize(771,90)
		milieu_libelle.resize(668,20)
		milieu_code.resize(620,20)
		commentaire.resize(755,60)
		
		milieu_code.setVisible(1)
		milieu_code_label.setVisible(1)

	else :
		combo_02.clear()
		i = 0
		while i < len(items):
			combo_02.addItems(items[i])
			i=i+1		
		combo_02.setCurrentIndex(-1)
		
	#***03
	if libelle_03.text() != "" and libelle_03.text() != "NULL":
		valeur = code_03.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste")
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0]
		
		combo_03.clear()
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(items):
			liste = items[i][0]
			combo_03.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]:
				j = i
			i=i+1			
		combo_03.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j

		myDialog.resize(1060,455)
		groupBox.resize(1041,151)
		groupBox_2.resize(1041,90)
		milieu_libelle.resize(945,20)
		milieu_code.resize(892,20)
		commentaire.resize(1020,60)
		
		milieu_code.setVisible(1)
		milieu_code_label.setVisible(1)

	else :
		combo_03.clear()
		i = 0
		while i < len(items):
			combo_03.addItems(items[i])
			i=i+1		
		combo_03.setCurrentIndex(-1)

	
	## con_qgisexion des fonctions
	QObject.connect(combo_01, SIGNAL("currentIndexChanged(int)"), change_hab_01) # Lance la fonction change_hab
	QObject.connect(code_01, SIGNAL("editingFinished()"), edit_code_01) # Lance la focntion edit_code qd modifie le code_01
	QObject.connect(combo_02, SIGNAL("currentIndexChanged(int)"), change_hab_02) # Lance la fonction change_hab
	QObject.connect(code_02, SIGNAL("editingFinished()"), edit_code_02) # Lance la focntion edit_code qd modifie le code_02
	QObject.connect(combo_03, SIGNAL("currentIndexChanged(int)"), change_hab_03) # Lance la fonction change_hab
	QObject.connect(code_03, SIGNAL("editingFinished()"), edit_code_03) # Lance la focntion edit_code qd modifie le code_03
	QObject.connect(agrandir_01, SIGNAL("clicked()"), fct_agrandir_01)
	QObject.connect(agrandir_02, SIGNAL("clicked()"), fct_agrandir_02)

	code_01.textChanged.connect(code_01_couleur) # Fonction changement de couleur
	buttonBox.accepted.disconnect(myDialog.accept) # Deconnecte le signal de QGIS
	buttonBox.accepted.connect(validate) # connecte la fonction validate
	buttonBox.rejected.connect(myDialog.reject)	
	
	## Fonction qui permet de stocke valeur liste deroulante dans les lineEdit
def change_hab_01():
	text_combo_01 = combo_01.currentText()
	text_code_01 = text_combo_01[0:(text_combo_01.find(':') - 1)]
	text_libelle_01 = text_combo_01[(text_combo_01.find(':') + 2):]
	code_01.setText(text_code_01)
	libelle_01.setText(text_libelle_01)
def change_hab_02():
	text_combo_02 = combo_02.currentText()
	text_code_02 = text_combo_02[0:(text_combo_02.find(':') - 1)]
	text_libelle_02 = text_combo_02[(text_combo_02.find(':') + 2):]
	code_02.setText(text_code_02)
	libelle_02.setText(text_libelle_02)
def change_hab_03():
	text_combo_03 = combo_03.currentText()
	text_code_03 = text_combo_03[0:(text_combo_03.find(':') - 1)]
	text_libelle_03 = text_combo_03[(text_combo_03.find(':') + 2):]
	code_03.setText(text_code_03)
	libelle_03.setText(text_libelle_03)
	
	## Fonction pour changer la comboBox lorsquon edite le LineEdit code_XX
def edit_code_01():
	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_01.text() + "'")
	count = cur_qgis.fetchone() # compte le nombre de correspondace entre le referentiel et la valeur saisie
	if count[0] == 1:
		valeur = code_01.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste")
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0]
		
		combo_01.clear()
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la combo_01Box
		while i < len(items):
			liste = items[i][0]
			combo_01.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]:
				j = i
			i=i+1			
		combo_01.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j
	
def edit_code_02():
	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_02.text() + "'")
	count = cur_qgis.fetchone()
	if count[0] == 1:
		valeur = code_02.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste")
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0]
		
		combo_02.clear()
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(items):
			liste = items[i][0]
			combo_02.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]:
				j = i
			i=i+1			
		combo_02.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j

def edit_code_03():
	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_03.text() + "'")
	count = cur_qgis.fetchone()
	if count[0] == 1:
		valeur = code_03.text()
		cur_qgis.execute("SELECT DISTINCT cd_cb as liste FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + valeur + "' ORDER BY liste")
		items_filtre = cur_qgis.fetchall()
		liste_filtre = items_filtre[0][0]
		
		combo_03.clear()
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(items):
			liste = items[i][0]
			combo_03.addItems(items[i])
			if liste_filtre == liste[0:(liste.find(':') - 1)]:
				j = i
			i=i+1			
		combo_03.setCurrentIndex(j) # cur_qgisrentIndex permet de faire commencer la liste au point j

	## Fonction de validation des donnees saisies
def validate():
	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_01.text() + "'")
	count_01 = cur_qgis.fetchone() # compte le nombre de correspondace entre le referentiel et la valeur saisie

	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_02.text() + "'")
	count_02 = cur_qgis.fetchone()
	
	cur_qgis.execute("SELECT DISTINCT count(cd_cb) FROM ref.typo_corine_biotopes WHERE ref.typo_corine_biotopes.cd_cb LIKE '" + code_03.text() + "'")
	count_03 = cur_qgis.fetchone()

	if code_01.text() == "" or code_01.text() == "NULL":
		code_01.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
		QMessageBox.warning(None, "Oups :", "Veuillez renseigner au moins un type de d'habitat")
		
	elif count_01[0] == 0:
		QMessageBox.warning(None, "Oups :", "Le code 01 saisie ne figure pas dans le referentiel")
		
	else:
		if code_02.text() == "" or code_02.text() == "NULL":
			myDialog.accept()
		elif count_02[0] == 0:
			QMessageBox.warning(None, "Oups :", "Le code 02 saisie ne figure pas dans le referentiel")
		else:
			if code_03.text() == "" or code_03.text() == "NULL":
				myDialog.accept()
			elif count_03[0] == 0:
				QMessageBox.warning(None, "Oups :", "Le code 03 saisie ne figure pas dans le referentiel")
			else:
				myDialog.accept()
	
	## Fonction pour changer de couleur si le champ est faux
def code_01_couleur(text):
	if code_01.text() == "NULL" or code_01.text() == "":
		code_01.setStyleSheet("background-color: rgba(255, 107, 107, 150);")
	else:
		code_01.setStyleSheet("")

def fct_agrandir_01():
	if(myDialog.width() != 790):
		myDialog.resize(790,455)
		groupBox.resize(771,151)
		groupBox_2.resize(771,90)
		milieu_libelle.resize(668,20)
		milieu_code.resize(620,20)
		commentaire.resize(755,60)
		
		milieu_code.setVisible(1)
		milieu_code_label.setVisible(1)
	else:
		myDialog.resize(520,455)
		groupBox.resize(501,151)
		groupBox_2.resize(501,90)
		milieu_libelle.resize(395,20)
		milieu_code.resize(350,20)
		commentaire.resize(485,60)
		
		milieu_code.setVisible(0)
		milieu_code_label.setVisible(0)
def fct_agrandir_02():
	if(myDialog.width() != 1060):
		myDialog.resize(1060,455)
		groupBox.resize(1041,151)
		groupBox_2.resize(1041,90)
		milieu_libelle.resize(945,20)
		milieu_code.resize(892,20)
		commentaire.resize(1020,60)
		
		milieu_code.setVisible(1)
		milieu_code_label.setVisible(1)
	else:
		myDialog.resize(790,455)
		groupBox.resize(771,151)
		groupBox_2.resize(771,90)		
		milieu_libelle.resize(665,20)
		milieu_code.resize(620,20)
		commentaire.resize(755,60)
		
		milieu_code.setVisible(1)
		milieu_code_label.setVisible(1)
		
##############################################################
################## Formulaire Contour site ###################
##############################################################

def formContOpen(dialog,layerid,featureid):
	## Connexion des objets du formulaire
	global myDialog
	myDialog = dialog
	buttonBox = dialog.findChild(QDialogButtonBox,"buttonBox")
	
	global type_site_combo
	type_site_combo = dialog.findChild(QComboBox,"type_site_combo")
	global type_milieu_combo
	type_milieu_combo = dialog.findChild(QComboBox,"type_milieu_combo")
	global referent_combo
	referent_combo = dialog.findChild(QComboBox,"referent_combo")
	global utilisateur_combo
	utilisateur_combo = dialog.findChild(QComboBox,"utilisateur_combo")
	
	global type_site
 	type_site = dialog.findChild(QLineEdit,"type_site")
	type_site.setVisible(0)
	global type_milieu
	type_milieu = dialog.findChild(QLineEdit,"type_milieu")
	type_milieu.setVisible(0)
	global referent
	referent = dialog.findChild(QLineEdit,"referent")
	referent.setVisible(0)
	global utilisateur
	utilisateur = dialog.findChild(QLineEdit,"utilisateur")
	utilisateur.setVisible(0)
	
	# Generation des listes
	global list_type_site
	cur_qgis.execute("SELECT DISTINCT type_site as liste FROM ref.type_site ORDER BY liste")
	list_type_site = cur_qgis.fetchall()
	global list_type_milieu
	cur_qgis.execute("SELECT DISTINCT type_milieu as liste FROM ref.type_milieu ORDER BY liste")
	list_type_milieu = cur_qgis.fetchall()
	global list_referent
	cur_qgis.execute("SELECT DISTINCT referent as liste FROM ref.cen_ra ORDER BY liste")
	list_referent = cur_qgis.fetchall()
	
	CurrentLayer=qgis.utils.iface.activeLayer()
	if CurrentLayer.isEditable() == True: # indique quels elements sont editable dans le formulaire
		referent_combo.setEnabled(True)
		utilisateur_combo.setEnabled(True)
		type_milieu_combo.setEnabled(True)
		type_site_combo.setEnabled(True)

	else:
		referent_combo.setEnabled(False)
		utilisateur_combo.setEnabled(False)
		type_milieu_combo.setEnabled(False)
		type_site_combo.setEnabled(False)
		
	#***type_site
	if type_site.text() != "" and type_site.text() != "NULL":
		valeur = type_site.text()
		valeur_modif = valeur.replace("'","''") # Resou le pb des apostrophes
		cur_qgis.execute("SELECT DISTINCT type_site as liste FROM ref.type_site  WHERE ref.type_site.type_site LIKE '" + valeur_modif + "' ORDER BY liste") # recupere la valeur du referentiel correspondant a la valeur saisie
		type_site_filtre = cur_qgis.fetchall()
		liste_type_site_filtre = type_site_filtre[0][0] # sauvegarde la valeur recuperer dans une variable
		
		type_site_combo.clear() # vide la liste de la comboBox
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(list_type_site):
			liste_type_site = list_type_site[i][0]
			type_site_combo.addItems(list_type_site[i])
			if liste_type_site_filtre == liste_type_site: # ou coupe au niveau des deux point et enleve 1 caractere
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		type_site_combo.setCurrentIndex(j)
		
	else :
		type_site_combo.clear()
		i = 0
		while i < len(list_type_site):
			type_site_combo.addItems(list_type_site[i])
			i=i+1		
		type_site_combo.setCurrentIndex(-1)
	
	#***type_milieu
	if type_milieu.text() != "" and type_milieu.text() != "NULL":
		valeur = type_milieu.text()
		valeur_modif = valeur.replace("'","''")
		cur_qgis.execute("SELECT DISTINCT type_milieu as liste FROM ref.type_milieu  WHERE ref.type_milieu.type_milieu LIKE '" + valeur_modif + "' ORDER BY liste") # recupere la valeur du referentiel correspondant a la valeur saisie
		type_milieu_filtre = cur_qgis.fetchall()
		liste_type_milieu_filtre = type_milieu_filtre[0][0] # sauvegarde la valeur recuperer dans une variable
		
		type_milieu_combo.clear() # vide la liste de la comboBox
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(list_type_milieu):
			liste_type_milieu = list_type_milieu[i][0]
			type_milieu_combo.addItems(list_type_milieu[i])
			if liste_type_milieu_filtre == liste_type_milieu: # ou coupe au niveau des deux point et enleve 1 caractere
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		type_milieu_combo.setCurrentIndex(j)
		
	else :
		type_milieu_combo.clear()
		i = 0
		while i < len(list_type_milieu):
			type_milieu_combo.addItems(list_type_milieu[i])
			i=i+1		
		type_milieu_combo.setCurrentIndex(-1)

	#***utilisateur
	if utilisateur.text() != "" and utilisateur.text() != "NULL":
		valeur = utilisateur.text()
		valeur_modif = valeur.replace("'","''")
		cur_qgis.execute("SELECT DISTINCT referent as liste FROM ref.cen_ra  WHERE ref.cen_ra.referent LIKE '" + valeur_modif + "' ORDER BY liste") # recupere la valeur du utilisateuriel correspondant a la valeur saisie
		utilisateur_filtre = cur_qgis.fetchall()
		liste_utilisateur_filtre = utilisateur_filtre[0][0] # sauvegarde la valeur recuperer dans une variable
		
		utilisateur_combo.clear() # vide la liste de la comboBox
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(list_referent):
			liste_referent = list_referent[i][0]
			utilisateur_combo.addItems(list_referent[i])
			if liste_utilisateur_filtre == liste_referent: # ou coupe au niveau des deux point et enleve 1 caractere
				j = i # si valeur saisie = a une valeur du utilisateuriel on enregistre j
			i=i+1			
		utilisateur_combo.setCurrentIndex(j)
		
	else :
		utilisateur_combo.clear()
		i = 0
		while i < len(list_referent):
			utilisateur_combo.addItems(list_referent[i])
			i=i+1		
		utilisateur_combo.setCurrentIndex(-1)
		
	#***referent
	if referent.text() != "" and referent.text() != "NULL":
		valeur = referent.text()
		valeur_modif = valeur.replace("'","''")
		cur_qgis.execute("SELECT DISTINCT referent as liste FROM ref.cen_ra  WHERE ref.cen_ra.referent LIKE '" + valeur_modif + "' ORDER BY liste") # recupere la valeur du referentiel correspondant a la valeur saisie
		referent_filtre = cur_qgis.fetchall()
		liste_referent_filtre = referent_filtre[0][0] # sauvegarde la valeur recuperer dans une variable
		
		referent_combo.clear() # vide la liste de la comboBox
		i = 0
		j = -1
		# Boucle qui permet de tester quel item ou index est deja saisie pour l'afficher comme valeur dans la comboBox
		while i < len(list_referent):
			liste_referent = list_referent[i][0]
			referent_combo.addItems(list_referent[i])
			if liste_referent_filtre == liste_referent: # ou coupe au niveau des deux point et enleve 1 caractere
				j = i # si valeur saisie = a une valeur du referentiel on enregistre j
			i=i+1			
		referent_combo.setCurrentIndex(j)
		
	else :
		referent_combo.clear()
		i = 0
		while i < len(list_referent):
			referent_combo.addItems(list_referent[i])
			i=i+1		
		referent_combo.setCurrentIndex(-1)
	
	QObject.connect(type_site_combo, SIGNAL("currentIndexChanged(int)"), change_type_site)
	QObject.connect(type_milieu_combo, SIGNAL("currentIndexChanged(int)"), change_type_milieu)
	QObject.connect(referent_combo, SIGNAL("currentIndexChanged(int)"), change_referent)
	QObject.connect(utilisateur_combo, SIGNAL("currentIndexChanged(int)"), change_utilisateur)
	
def change_type_site():
	text_type_site = type_site_combo.currentText()
	type_site.setText(text_type_site)

def change_type_milieu():
	text_type_milieu = type_milieu_combo.currentText()
	type_milieu.setText(text_type_milieu)

def change_utilisateur():
	text_utilisateur = utilisateur_combo.currentText()
	utilisateur.setText(text_utilisateur)
	
def change_referent():
	text_referent = referent_combo.currentText()
	referent.setText(text_referent)
