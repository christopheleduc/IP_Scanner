# CodeKiller_Present
<p align="center">
<img src="media/Ip_Scanner.png" width=200>
</p>


&nbsp;
# IP-SCANNER

IP-SCANNER :


&nbsp;
Utlisation de la librairie Scapy & Npcap avec Python 3 & Tkinter .


&nbsp;
IP-SCANNER :


&nbsp;
Il s'agit d'une application Python 3. Cette version est configuré pour produire un Package avec la librairie cx_Freeze. Les fonctionnalités sont les suivantes:

&nbsp;

* Scan une adresse IP sur le réseau.
* Scan une plage d'adresses IP/CIDR et retourne les couples IP/MAC.
* Affiche les couples IP/MAC dans un fichier texte.
* Le fichier texte est effacé à la fermeture du programme.

---

# NOTICE

* Vous avez besoin de la librairie Scapy :

$ pip install scapy

* Scapy sources :
* &#160;&#160;[Git development version.](https://github.com/secdev/scapy)
* &#160;&#160;[Documentation.](https://scapy.readthedocs.io/en/latest/index.html)


&nbsp;
* Npcap:
* &#160;&#160;[Sous Windows vous aurez aussi besoin de Npcap disponible ici.](https://nmap.org/npcap/)


&nbsp;
* Aide:
* &#160;&#160;[L'aide est disponible ici !](/doc/Notice_IP_Scanner.mht)


&nbsp;
* Packaging:
* &#160;&#160;Pour créer le Package MSI ou la version Stand Alone, vous avez besoin de la librairie "cx_Freeze".
* &#160;&#160;ATTENTION le setup est configuré pour Windows! A adapter selon les besoins...

$ python -m pip install cx_Freeze

* &#160;&#160;Pour générer la version Stand Alone:

$ python setup.py build

* &#160;&#160;Pour générer le binaire MSI:

$ python setup.py bdist_msi

---

# CHANGELOG
All notable changes to this project will be documented in this file.


&nbsp;
## [Unreleased]
