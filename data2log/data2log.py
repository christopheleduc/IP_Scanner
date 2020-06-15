#!/usr/bin/env python
# data2log : format print from input to writing in text file
#coding:utf-8

# This file is part of ip-scanner with Python3
# See wiki doc for more information
# Copyright (C) CryptoDox <cryptodox@cryptodox.net>
# This program is published under a GPLv2 license

__author__ = "Christophe LEDUC"
__date__ =  "11 decembre 2019"

"""
    Fonctions de formatage des output pour les consigner dans un fichier texte

    Usage:

    >>> from data2log import Data2log
"""

__version__ = "1.0.0"

# Pour test d'ecriture de fichiers
import os, os.path
# Pour test OS
import sys
from sys import platform

__all__ = ['Data2log']

class Data2log():

    def __init__(self):
        self.variables()

    def variables(self):
        self.separatorEtoiles = ('***************************************************************** \n')
        # self.Exploit = platform # OS type
        # self.NomFichier = 'mac_ip.txt' # Fichier texte
        self.folder = os.path.join(os.path.expanduser('~'),'.Ip_scanner')
        self.Exploit = sys.platform # OS type

    # Affiche les log dans un fichier texte
    def textLog(self, textFile = 'mac_ip.txt'):
        if self.Exploit == 'win32':
            os.popen(os.path.join(self.folder,textFile))
        else:
            os.popen(textFile)
        
    # Méthode fichier texte
    def texteLog(self, myTextes, xFile = 'mac_ip.txt'):
        # Variables
        myTexte = str(myTextes)# Convertie les data en String
        self.NomFichier = xFile # Fichier texte

        # création et ouverture du fichier mac_ip.txt ou celui passé en paramètres
        # Si le repertoire n'existe pas...
        if not os.path.exists(self.folder):
            # on le crée
            os.mkdir(self.folder)
        Fichier = open(os.path.join(os.path.expanduser('~'),'.Ip_scanner',self.NomFichier),'a') # instanciation de l'objet Fichier
        Fichier.write(myTexte) # écriture dans le fichier avec la méthode write()
        # fermeture du fichier avec la méthode close()
        Fichier.close()
        # if Exploit == 'win32':
        #     os.popen(os.path.join(os.path.expanduser('~'),'Documents',"mac_ip.txt"))
        # else:
        #     os.popen("mac_ip.txt")
    
    # Supprime le fichier au cas ou il contienne des infos confidentiel
    def textFile2Del(self, location = '.Ip_scanner', fileText = 'mac_ip.txt'):
        os.remove(os.path.join(os.path.expanduser('~'), location, fileText))

if __name__ == '__main__':
    Data2log()