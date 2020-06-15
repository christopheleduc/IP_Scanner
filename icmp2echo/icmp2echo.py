#!/usr/bin/env python
# icmp2echo : take IP or name to send ICMP echo request packet and displays the return packet
#coding:utf-8

# This file is part of a simple Scapy experience with Python3: https://github.com/christopheleduc/Scapy_Experience_001
# 
# See http://www.secdev.org/projects/scapy for more information
# Copyright (C) CryptoDox <cryptodox@cryptodox.net>
# This program is published under a GPLv2 license

__author__ = "Christophe LEDUC"
__date__ =  "03 novembre 2019"

"""
    Implémentation de l'envoi d'un paquet ICMP echo

    Usage:

    >>> from icmp2echo import icmp2echo
    >>> icmp2echo()
"""

__version__ = "1.0.0"

import sys

__all__ = ['icmp2echo']

def icmp2echo():

    if len(sys.argv) != 2:
        print ("Usage: icmp2echo <IP or hostname>\n  eg: icmp2echo 192.168.1.1")
        sys.exit(1)

    # from io import StringIO# Another way 1
    from scapy.layers import inet
    from scapy.all import sr1, IP, ICMP

    #packet = sr1(IP(dst=sys.argv[1])/ICMP())
    packet = sr1((IP(dst=sys.argv[1])/ICMP()), timeout=10)
    if packet:
        #Redirect output of print to variable 'capture'
        # capture = StringIO()# Another way 1
        # save_stdout = sys.stdout# Another way 1
        # sys.stdout = capture# Another way 1
        retour = packet.show(dump=True)
        # sys.stdout = save_stdout# Another way 1
        # capture.getvalue() is a string with the output of 'pack.show()'# Another way 1
        # print (capture.getvalue())# Another way 1 
        # retour = (capture.getvalue())# Another way 1
        # Verify that capture.getvalue() is a string# Another way 1
        # print (isinstance(capture.getvalue(), str))# Another way 1
        return retour

if __name__ == '__main__':
    icmp2echo()