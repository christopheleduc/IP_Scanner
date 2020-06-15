#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

__all__ = ['sleeper']

"""
    Ce module propose un simple timer
"""

__version__ = "1.0.0"

#######################################
# Une petite fonction pour un timer.  #
#######################################

def sleeper(num):
    while True:
        # Try to convert it to a float
        try:
            num = float(num)
        except ValueError:
            continue
 
        # lance la commande time.sleep() et affiche le timestamp de début et de fin.
        print('Programme en pause à: %s' % time.ctime() + ' Please wait... \r\n')
        time.sleep(num)
        print('Reprise du programme à: %s\n' % time.ctime() + ' \r\n')
        return False
