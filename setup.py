#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3

"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""
 
import sys, os.path
# import distutils
import opcode

from cx_Freeze import setup, Executable
 
#############################################################################
# preparation des options
 
# chemins de recherche des modules
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')

# copier les fichiers non-Python et/ou repertoires et leur contenu:
includefiles = [(distutils_path, 'lib/distutils'),os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),('media/'),('doc/'),('IP_Scanner.exe.manifest'),('Package.appxmanifest')]

# ajouter d'autres chemins (absolus) si necessaire: sys.path + ["chemin1", "chemin2"]
path = sys.path
 
# options d'inclusion/exclusion des modules
includes = []  # nommer les modules non trouves par cx_freeze
excludes = ['distutils']
packages = []  # nommer les packages utilises
 
if sys.platform == "win32":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Windows
elif sys.platform == "linux2":
    pass
    # includefiles += [...] : ajouter les recopies specifiques à Linux
else:
    pass
    # includefiles += [...] : cas du Mac OSX non traite ici
 
# pour que les bibliotheques binaires de /usr/lib soient recopiees aussi sous Linux
binpathincludes = []
if sys.platform == "linux2":
    binpathincludes += ["/usr/lib"]
 
# niveau d'optimisation pour la compilation en bytecodes
optimize = 0
 
# si True, n'affiche que les warning et les erreurs pendant le traitement cx_freeze
silent = True
 
# construction du dictionnaire des options
options = {"path": path,
           "includes": includes,
           "excludes": excludes,
           "packages": packages,
           "include_files": includefiles,
           "bin_path_includes": binpathincludes,
           #"create_shared_zip": False,  # <= ne pas generer de fichier zip
           #"include_in_shared_zip": False,  # <= ne pas generer de fichier zip
           #"compressed": False,  # <= ne pas generer de fichier zip
           "optimize": optimize,
           "silent": silent
           }
 
# pour inclure sous Windows les dll system de Windows necessaires
if sys.platform == "win32":
    options["include_msvcr"] = True

# if 'bdist_msi' in sys.argv:
#     prgm_path = os.environ.get("PROGRAMFILES")
#     destination = os.path.join(prgm_path,'Ip_compliance')
#     sys.argv += ['--initial-target-dir', destination]

#############################################################################
# MSI Bluid
# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    (
        "DesktopShortcut",        # Shortcut
        "DesktopFolder",          # Directory_
        "CryptoDox IP Scanner",           # Name
        "TARGETDIR",              # Component_
        "[TARGETDIR]IP_Scanner.exe",# Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
     ),

     (
        "StartupShortcut",        # Shortcut
        "ProgramMenuFolder",          # Directory_
        "CryptoDox IP Scanner",     # Name
        "TARGETDIR",              # Component_
        "[TARGETDIR]IP_Scanner.exe",   # Target
        None,                     # Arguments
        None,                     # Description
        None,                     # Hotkey
        None,                     # Icon
        None,                     # IconIndex
        None,                     # ShowCmd
        'TARGETDIR'               # WkDir
     ),
    ]

directory_table = [
    (
        "ProgramMenuFolder",
        "TARGETDIR",
        ".",
    ),

    (
        "MyProgramMenu",
        "ProgramMenuFolder",
        "MYPROG~1|My Program",
    ),
]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
#msi_data.append = {"Shortcut": directory_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}
 
#############################################################################
# preparation des cibles
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # pour application graphique sous Windows
    # base = "Console" # pour application en console sous Windows
 
icone = None
if sys.platform == "win32":
    icone = "media/Blockchain_Logo_001.ico"

shortcutN = None
if sys.platform == "win32":
    shortcutN = "CryptoDox IP Scanner"

shortcutD = None
if sys.platform == "win32":
    shortcutD = "DesktopFolder"
 
cible_1 = Executable(
    "main.py",
    targetName="IP_Scanner.exe",
    base=base,
    #compress=False,  # <= ne pas generer de fichier zip
    #copyDependentFiles=True,
    #appendScriptToExe=True,
    #appendScriptToLibrary=False,  # <= ne pas generer de fichier zip
    icon=icone, # Only for "MSI"; Remove for "EXE"
    shortcutName = shortcutN,
    shortcutDir = shortcutD,
    )
 
#cible_2 = Executable(
    #script="monprogramme2.pyw",
    #base=base,
    #compress=False,
    #copyDependentFiles=True,
    #appendScriptToExe=True,
    #appendScriptToLibrary=False,
    #icon=icone
    #)
 
bdist_msi_options = {'add_to_path': False,
                     'data': msi_data,
                     'product_code': '{4147c223-0043-405f-9629-c3fe5e2f735e}',
                     'upgrade_code': '{e24c3a51-ae07-4509-b5e2-2b300bc63304}'}



#############################################################################
# creation du setup
setup(
    name="IP_Scanner",
    version="1.0.0",
    description="Scan une IP ou une plage d'adresses IP/CIDR et retourne les couples IP/MAC",
    maintainer="CodeKiller",
    maintainer_email="cryptodox@cryptodox.net",
    long_description="En cours de rédaction...",
    options={"build_exe": options, "bdist_msi": bdist_msi_options},
    executables=[cible_1]
    )