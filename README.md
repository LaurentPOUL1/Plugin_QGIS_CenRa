Plugin_QGIS_CenRa
=================
	-----------------
	I - Présentation
	-----------------
	
1- L'utilisateur ouvre QGIS --> Chargement du Plugin CenRa

2- Ce Plugin à pour fonction :
		- La création de schémas dans la base de données (équivalent d'un dossier pour les utilisateurs)
		- La création de couches thématiques formatées avec des champs prédéfinis
		- La liaison d'un style par défaut à la couche crée, dans la table layer_style de PostGis
   Pour fonctionner (connexion à la bd Postgis, création des tables) le plugin à besoin du fichier "config.txt" stocké sur le serveur
   
3- Le style par défaut permet d'appeler un formulaire spécifique (.ui stocké sur le serveur aussi) pour chaque thématique qui va représenter une aide à la saisie.
   Ces formulaires sont également en relation avec un fichier python, "Form.py", amenant des fonctions supplémentaires aux formulaires.
   
4- L'utilisateur enregistre l'ensemble de la donnée créée dans PostGis

	---------------------------------
	II - Installation / Paramétrages
	---------------------------------
	
1- Placer les formulaires et le fichier config.txt sur le serveur

2- Modifier le fichier config.txt, Form.py, et .py du plugin pour faire références à la base de données et aux fichiers stockés sur le serveur

3- Placer le plugin dans le dossier adéquat :  ..\.qgis2\python\plugins

4- Placer le fichier Form.py dans le dossier "bin" d'installation de QGIS : C:\Program Files\QGIS Valmiera\bin
