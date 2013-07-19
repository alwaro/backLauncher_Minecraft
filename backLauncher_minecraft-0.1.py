#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# #######################################
#   	BackLauncher for Minecraft 
# #######################################
#
#   Version..........: 0.1
#   Supported OS.....: Mac OSX (For now)
#   Author...........: Alvaro Anaya M.
#	Web..............: http://www.archivoslog.es
#	Web2.............: http://archivoslog.wordpress.com
#
#	DESCRIPTION:
#	
#	BackLauncher  for  Minecraft  es  un  lanzador
#	pensado para  hacer un backup  de  los  mundos
#	del Minecraft justo antes de comenzar el juego
# 	de forma que pase lo que pase, siempre tengamos
#	una  opcion  de volver a restaurarlo tal y como 
#	estaba antes de comezar la partida
#	
#  INSTRUCTIONS:
# 
#	Este lanzador debe configurarse para ser lanzado,
#	en lugar del ejecutable del minecraft ya que, es
#	BackLauncher quien lo lanzara tras haber hecho el
# 	el backup de los mundos
#
#	Todas las rutas estan configuradas por defecto asi
#	como el nombre del lanzador de minecraft original
#	Los backups se almacenan dentro de la ruta del 
# 	minecraft, que es:
#   ~/Library/Application Support/minecraft/BackLauncher
#	aunque es posible modifcar esta y otras rutas en la 
# 	parte "CUSTOMIZABLE SETTINGS" del script.
#	Solo deberia modificar esta parte del script para 
#	garantizar su funcionamiento aunque si todo esta
#	en las rutas por defecto, no es necesario modificar
#	absolutamente nada
#
#	Esta version es la primera y aun le faltan muchas 
#	caracteristicas por implementar, entre ellas un
# 	sistema de informes y restauracion de los mundos 
#	que por el momento, tendra que hacerse a mano.


import os, time,sys, shutil, zipfile
from os.path import join  

# ----------------- CUSTIMIZABLE SETTINGS -------------------
rutaDestino = os.path.expanduser(os.path.join("~","Library","Application Support","minecraft","BackLauncher"))
rutaSaves = os.path.expanduser(os.path.join("~","Library","Application Support","minecraft","saves"))
minecraftAPP = "/Applications/Minecraft.app"
# ------------------------- END -----------------------------

# Console colors (Thanks to wifite :) )
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green

mineLauncher="open " + minecraftAPP
laVersion="0.1"

# Funcion sin uso aun
#def checkLastUse(origenCompleto, clonadoCompleto):
#	firstFile = os.path.getmtime(pathToFirstFile)
#	secondFile = os.path.getmtime(pathToSecondFile)
#	if firstFile > secondFile:
#		print "firstFile is the most recently modified."
#	else:
#		print "firstFile is not the most recently modified."

def doBackup(destinoCompleto, aItem,rutaDestino):
	
	# Console colors (Thanks to wifite :) )
	W  = '\033[0m'  # white (normal)
	R  = '\033[31m' # red
	G  = '\033[32m' # green
	checkOK = G+'	DONE'+W
	checkKO = R+'	FAIL'+W
	
	elResult = checkKO

	try:
		shutil.make_archive(destinoCompleto, 'zip',aItem)
		elResult = checkOK

	except Exception, e:
		pass		# raise e

	return elResult

# Si la ruta donde guardar los backups no existe, la crea
if not os.path.isdir(rutaDestino):
	os.mkdir(rutaDestino)

os.chdir(rutaSaves)
print "--------------------------------------------------------"
print ("   BackLauncher %s - Backup Your Games Before Play" % (laVersion))
print "--------------------------------------------------------"

print "	ESTADO	   MUNDO: "
print "	-------	  -------------"

try:
	for aItem in os.listdir(os.getcwd()):
		origenCompleto = os.path.expanduser(os.path.join(rutaSaves, aItem))
		if os.path.isdir(aItem):
			fileDestino = aItem + time.strftime("-%Y%m%d%H%M%S")
			destinoCompleto = os.path.expanduser(os.path.join(rutaDestino, fileDestino))
			backResult=doBackup(destinoCompleto,aItem,rutaDestino) # aItem)
		else:
			if os.path.isfile(aItem):
				aItem = aItem + R+" (Seguro que es un mundo?)"+W
		
			backResult=R+'	FAIL'+W
		
		print ( '%s	-  %s' % (backResult,aItem))
except KeyboardInterrupt:
	print "\n\nHa "+R+"CANCELADO"+W+" el proceso de backups"


try:
	raw_input("\n\nPresione INTRO para abrir Mincraft o CTRL+C para salir...")
	os.system(mineLauncher)
except KeyboardInterrupt:
	print "\n\nCancelado por el usuario\n"
	sys.exit()
