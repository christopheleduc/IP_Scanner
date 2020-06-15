#!/usr/bin/env python
# main : Interface graphique
# -*- coding: utf-8 -*-

# This file is part of ip-scanner with Python3
# See wiki doc for more information
# Copyright (C) CryptoDox <cryptodox@cryptodox.net>
# This program is published under a GPLv2 license

__author__ = "CodeKiller"
__date__ =  "12 juin 2020"

# Pour test d'ecriture de fichiers
import os, os.path
# Pour test OS
import sys
from sys import platform
# Import GUI
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
from tkinter.constants import RIGHT, LEFT, Y, BOTH
# import librairie graphique pour les stats (matplotlib)
# import matplotlib.pyplot as plt
# import librairie tiers
from tkinter import simpledialog
# Gestion des Thread
import threading
# import base64

# Modules perso pour IP-Scanner
import sleeper.sleeper as sl
from data2log import Data2log
#from ssh2serv import ssh2serv

# Modules perso pour detection
from monitor2all import sniffer
from icmp2echo import icmp2echo
from arping2tex import arping2tex


"""
Le moyen le plus simple pour un Ops de manipuler des données, 
c'est de lui fournir une inteface graphique avec des GROS boutons
"""

__version__ = "1.0.0 Beta"

# requests.packages.urllib3.disable_warnings()


class IpScannerFenetre(tk.Tk):
    def __init__(self, master, **kwargs):
        self.master = master
        self.creation()
    
    def creation(self):
        self.master.resizable(False,True)
        self.master.title ("IP Scanner v1.0.0 (Beta)")

        # Variables global
        self.Data2text = Data2log() # Librairie data2log
        self.Exploit = sys.platform # OS type
        self.Thr = threading.Thread # Librairie pour executer des Thread
        self.qn=int()
        self.qnp=int()
        self.text_result_01 = tk.StringVar()
        self.text_result_02 = tk.StringVar()
        self.folder = os.path.join(os.path.expanduser('~'),'.Ip_scanner')

        ##### Menu #####
        barreMenu = tk.Menu(self.master)
        
        ##### Menu <Actions> #####
        menuActions = tk.Menu(barreMenu, tearoff=0)
        menuActions.add_separator()
        menuActions.add_command(label="Quitter", command=self.cleanDestroy)
        barreMenu.add_cascade( label="Actions", menu=menuActions)

        ##### Menu <Scan> #####
        menuScan = tk.Menu(barreMenu, tearoff=0)
        menuScan.add_command(label="Scan IP", command=self.Icmp2echo)
        menuScan.add_command(label="Scan MAC", command=self.Arping2tex)
        barreMenu.add_cascade( label="Scan", menu=menuScan)

        ##### Menu <Options> #####
        menuOptions = tk.Menu(barreMenu, tearoff=0)
        menuOptions.add_separator()
        menuOptions.add_command(label="Afficher les MAC/IP ?", command=self.scanToggle)
        barreMenu.add_cascade( label="Options", menu=menuOptions)

        ##### Menu <Aide> #####
        menuAide = tk.Menu(barreMenu, tearoff=0)
        menuAide.add_command(label="Aide", command=self.helpNotice)
        menuAide.add_command(label="Contact", command=self.contactMe)
        menuAide.add_separator()
        menuAide.add_command(label="About", command=self.aboutUs)
        barreMenu.add_cascade( label="Aide", menu=menuAide)
        
        self.master.config(menu = barreMenu)

        # LabelFrame blabla 1
        self.presentationBase = tk.LabelFrame(self.master, text="Cryptodox Copyright 2020", padx=5, pady=5)
        self.presentationBase.pack(fill="both", expand="yes")

        # Label blabla 1
        self.photo = tk.PhotoImage(file='media/Ip_Scanner.png')
        self.presentation = tk.Label(self.presentationBase, image=self.photo)
        self.presentation.pack(fill="both", expand="yes")

        # Label options d'affichage
        self.options = tk.LabelFrame(self.master, text="Options", padx=5, pady=5)
        self.options.pack(fill="both", expand="yes")

        # Label options d'affichage
        self.optionsLog = tk.LabelFrame(self.master, text="Affichage des log", padx=5, pady=5)
        self.optionsLog.pack(fill="both", expand="yes")
        
        # Case à cocher (sortie fichier texte pour le Scan MAC/IP)
        self.check_textScan = tk.IntVar()
        self.check_textScan.set(0)
        self.scan_valide = tk.Checkbutton(self.optionsLog, text="Afficher les MAC/IP ? ", variable=self.check_textScan, onvalue = 1, offvalue = 0)
        self.scan_valide.pack(side=tk.RIGHT, padx=5, pady=5)

        # Label Saisies optionnelles recherches IP/Hostname/CIDR
        self.special_finding = tk.LabelFrame(self.master, text="Saisie IP / Hostname / CIDR", padx=10, pady=10)
        self.special_finding.pack(fill="both", expand="yes")

        self.cadre_02 = tk.PanedWindow(self.special_finding, orient=tk.VERTICAL)
        self.cadre_02.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)

        # label 1                                             Adresse IP
        self.label1 = tk.Label(self.special_finding, text="                    Adresse IP :                    ", bg="green")
        self.label1.pack()
        self.cadre_02.add(self.label1)

        # entrée 1
        self.value1 = tk.StringVar() 
        self.value1.set("Adesse IP V4. Eg. 192.168.0.10")
        self.entree1 = tk.Entry(self.special_finding, textvariable=self.value1, width=30)
        self.entree1.pack()
        self.cadre_02.add(self.entree1)

        # label 2                                                 CIDR
        self.label2 = tk.Label(self.special_finding, text="                        IP / CIDR :                         ", bg="green")
        self.label2.pack()
        self.cadre_02.add(self.label2)

        # entrée 2
        self.value2 = tk.StringVar() 
        self.value2.set("Entrer une plage suivie du CIDR. Eg. 192.168.0.0/24")
        self.entree2 = tk.Entry(self.special_finding, textvariable=self.value2, width=30)
        self.entree2.pack()
        self.cadre_02.add(self.entree2)
        self.cadre_02.pack()

        # scanneurs
        self.scanner = tk.LabelFrame (self.master, text="Scanneur passif", padx=10, pady=10)
        self.scanner.pack(fill="both", expand="yes")
        self.button = tk.Button(self.scanner, text="Scan IP", command=self.Icmp2echo)
        self.button.pack( side = tk.LEFT)
        self.button01 = tk.Button(self.scanner, text="Scan Plage", command=self.Arping2tex)
        self.button01.pack( side = tk.LEFT)

        # Label Affichage des resultats de recherche spécifique
        self.special_result = tk.LabelFrame(self.master, text="Statut", padx=10, pady=10)
        self.special_result.pack(fill="both", expand="yes")
        self.cadre_03 = tk.PanedWindow(self.special_result, orient=tk.VERTICAL)
        self.cadre_03.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)
        self.text_result_01 = tk.Text(self.cadre_03, height='1', font=('Segoe UI', '9'), foreground='green', background='black', wrap=tk.WORD)
        self.text_result_01.config(state=tk.NORMAL)
        self.text_result_01.insert('1.0', 'Utiliser le champ \"Adresse IP\" avec le bouton \"Scan IP\" et \"IP/CIDR\" avec \"Scan Plage\" !')
        self.text_result_01.tag_configure("center", justify='center')
        self.text_result_01.tag_add("center", 1.0, tk.END)
        self.text_result_01.config(state=tk.DISABLED)
        self.cadre_03.add(self.text_result_01)
        self.s1 = tk.Scrollbar(self.text_result_01, width=15, cursor='left_ptr') # Test preparation de scrollbar
        self.text_result_02 = tk.Text(self.cadre_03, height='1', font=('Segoe UI', '9'), foreground='green', background='black', wrap=tk.WORD)
        self.text_result_02.config(state=tk.NORMAL)
        self.text_result_02.insert('1.0', 'Waiting for action...')
        self.text_result_02.tag_configure("center", justify='center')
        self.text_result_02.tag_add("center", 1.0, tk.END)
        self.text_result_02.config(state=tk.DISABLED)
        self.cadre_03.add(self.text_result_02)
        self.cadre_03.pack()

        # Label Actions 1
        labelAct1 = tk.LabelFrame(self.master, text="Actions", padx=15, pady=15)
        labelAct1.pack(fill="both", expand="yes")
        tk.Button(labelAct1, text="  Quitter  ", command=self.cleanDestroy).grid(row=1, column=4)

        self.mainloop


    def scanToggle(self):
        self.scan_valide.toggle()
    
    def helpNotice(self):
        import webbrowser
        fichier = 'doc\\Notice_IP_Scanner.mht'
        webbrowser.open(fichier)

    def contactMe(self):
        message = "                        Pour vos retours  \n \n   (dysfonctionnements, suggestions ou autres) \n \n                n'hésitez pas à me contacter: \n \n                cryptodox@cryptodox.net   "
        self.WarnNotice3(message)

    def aboutUs(self):
        message = "  Développé par: \n \n      CodeKiller \n                         \n           \n      CryptoDox.  \n \n           \nIP-Scanner v1.0.0 (Beta)."
        self.WarnNotice3(message)
    
    def WarnNotice3(self, warn_notice3):
        self.myWarn = tkMessageBox.showinfo('Résultat', message=warn_notice3)
    
    # Affichage Status 1
    def afficheStatus1(self, texte):
        self.text_result_01.config(state=tk.NORMAL)
        self.text_result_01.delete('1.0', tk.END)
        self.text_result_01.insert('1.0', texte)
        self.text_result_01.tag_add("center", 1.0, tk.END)
        self.text_result_01.config(state=tk.DISABLED)
    
    # Affichage Status 2
    def afficheStatus2(self, texte):
        self.text_result_02.config(state=tk.NORMAL)
        self.text_result_02.delete('1.0', tk.END)
        self.text_result_02.insert('1.0', texte)
        self.text_result_02.tag_add("center", 1.0, tk.END)
        self.text_result_02.config(state=tk.DISABLED)
    
    def SuivieExec(self, back_log, select):
        # On prépare l'affichage
        self.infoSequence_01 = tk.Toplevel(height=150, width=300)
        self.infoSequence_01.title("Console / Log.")
        self.infoSequence_01.transient(self.cadre_03)
        self.text_result_03 = tk.Text(self.infoSequence_01, height='35', width='300', font=('Segoe UI', '9'), foreground='green', background='black', wrap=tk.WORD)
        self.s2 = tk.Scrollbar(self.text_result_03, width=15, cursor='left_ptr', orient = 'vertical') # Test preparation de scrollbar
        self.s2.pack(side = RIGHT, fill = Y, expand=False)
        self.text_result_03.config(yscrollcommand=self.s2.set) # il faut le préciser!!!
        
        # si Arping2tex
        if (select == 1):
            self.text_result_03.insert('1.0', '              MAC            &              IP \n')
            self.Data2text.texteLog('++        MAC        &       IP     ++ \n', 'mac_ip.txt')
            for snd,rcv in back_log:
                # print (rcv.sprintf(r"%Ether.src% & %ARP.psrc%\\"))
                data = (rcv.sprintf(r"\\ %Ether.src% ==> %ARP.psrc% \\"))
                self.text_result_03.insert('end', data + '\n')
                self.Data2text.texteLog(data + '\n', 'mac_ip.txt')
            self.text_result_03.insert('end', '**************** END-SCAN ***************')
            self.Data2text.texteLog('**************** END-SCAN *************** \n', 'mac_ip.txt')
            if self.check_textScan.get() == 1:
                self.threadOperation_01 = self.Thr(name='mac_ipThread', target=self.Data2text.textLog, args=('mac_ip.txt',), daemon=True)
                self.threadOperation_01.start()
                
        # si Icmp2echo
        elif (select == 0):
            self.text_result_03.insert('1.0', back_log)

        # On affiche le résultat
        self.text_result_03.tag_configure("marge", rmargin='20')
        self.text_result_03.pack( expand=True, fill=BOTH, pady=2, padx=2 )
        self.text_result_03.configure(height=55, width=500)
        self.infoSequence_01.geometry("300x200+300+0") # Taille de la fenetre pour affichage des resultats
        self.s2.config(command=self.text_result_03.yview) # Justement la voilà
    
    # Méthode qui verifie que la fenetre est fermée
    def isActive(self):
        try:
            self.infoSequence_01.grab_set()
            self.infoSequence_01.destroy()
        except:
            pass
    
    # Méthode Icmp2echo
    def Icmp2echo(self):
        self.isActive()
        try:
            adresse = self.value1.get() # adresse IP
            sys.argv = ["./icmp2echo.py", adresse]
            retour = icmp2echo()
            self.SuivieExec( retour, 0 )
        except:
            message = "Timeout dépassé. le réseaux est peut-etre indisponible. \n Veuillez re-essayer plus tard."
            self.WarnNotice3(message)

    # Méthode Arping2tex
    def Arping2tex(self):
        self.isActive()
        try:
            adresse = self.value2.get() # adresse du réseaux/CIDR
            sys.argv = ["./arping2tex.py", adresse]
            retour = arping2tex()
            self.SuivieExec( retour, 1 )
        except:
            message = "Timeout dépassé! \n Le réseaux, ou l'interface réseau, est peut-etre indisponible. \n Veuillez re-essayer plus tard."
            self.WarnNotice3(message)
    
    # Methode de fermeture du programme
    def cleanDestroy(self):
        self.aurevoir = "Fermeture des process. Veillez patienter..."
        try:
            # On suprime ce fichier qui contient des données confidentiel
            self.Data2text.textFile2Del(fileText = 'mac_ip.txt')
        except:
            pass
        try:
            # On suprime ce fichier qui contient des données confidentiel
            self.Data2text.textFile2Del()
        except:
            pass
        try:
            self.isActive()
        except:
            pass

        self.threadOperation_04 = self.Thr(name='AppExit', target=self.Quit, daemon=True)
        self.threadOperation_05 = self.Thr(name='AppQuit', target=self.WarnNotice3, args=(self.aurevoir,), daemon=True)
        self.threadOperation_04.start()
        self.threadOperation_05.start()

    def Quit(self):
        # Clean-up any left-over debugging files.
        try:
            os.remove(DEBUG_FILENAME)  # Delete previous file, if any.
        except Exception:
            pass
        try:
            os.remove(EXC_INFO_FILENAME)  # Delete previous file, if any.
        except Exception:
            pass

        sl.sleeper(7)
        # Finalement on ferme l'application proprement
        self.master.destroy()

if __name__=="__main__":
    #Tk
    master = tk.Tk()
    master.wm_iconbitmap('media/Blockchain_Logo_001.ico')
    f = IpScannerFenetre(master)
    master.mainloop()