# -------------------------------------------#
# SETUP HEADER                         #
# -------------------------------------------#
#  Reusable setup.py file                   #
#-------------------------------------------#
import os
import sys


# AUTHOR
#-------------------------------------------
AUTHOR = "Caio Rodrigues"
AUTHOR_EMAIL = "caiorss.rodrigues@gmail.com"

# PACKAGE
#-------------------------------------------
PACKAGE_NAME = "encfsgtk"
LICENSE = 'BSD'
DESCRIPTION = """Graphical user interface for Encfs encryption tool ( a file level encryption tool """

PLATFORMS = ['Linux', 'Unix']
INSTALL_REQUIRES = ['gtk>=2.0', 'pygtk']
PACKAGE_DATA =   {}
KEYWORDS = ['encryption', 'security', 'data', 'encfs', 'cypher']
#
URL = "https://github.com/wolfprogrammer/encfsgtk"
CLASSIFIERS = [
    'Programming Language :: Python :: 2.7'
]

# DIRECTORY STRUCTURE
#-----------------------------------------------------
README_FILE = "README.md"
LICENSE_FILE = "LISENCE.txt"

# CONTROL VARIABLES
#-----------------------------------------------------
DEBUG = True

#----------------------------------------------------#
#   AUTOMATED SECTION - Don't change this section    #
#----------------------------------------------------#

from setuptools import setup, find_packages
from setuptools.command.install import install as _install
#from distutils.cmd import Command
from setuptools import Command

import re


def debug(*msg):
    if DEBUG:
        print  "DEBUG: ", "".join(msg)


HERE = os.path.abspath(os.path.dirname(__file__))
INIT = open(os.path.join(HERE, PACKAGE_NAME, '__init__.py')).read()
README = open(os.path.join(HERE, README_FILE)).read()
VERSION = re.findall("""__version__\s*=\s*["|'](.*)["|']""", INIT)[0]

PYTHON = sys.executable
PYTHON_PREFIX = sys.prefix
# Python Script/Executables locations - For Windows Only
PYTHON_SCRIPTS = os.path.join(PYTHON_PREFIX, "Scripts")

EPYDOC = os.path.join(PYTHON_SCRIPTS, "epydoc")
# Html File
INDEX_HTML = os.path.join(HERE, "docs", "index.html")

DATAPATH = os.path.join(HERE, PACKAGE_NAME, "data")

debug("HERE = ", HERE)
debug("PYTHON_SCRIPTS ", PYTHON_SCRIPTS)
debug("VERSION = %s" % VERSION)
debug("INDEX_HTML = %s" % INDEX_HTML)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

#test_suite='tests'

#----------------------------------------------------#
#   SETUP COMMANDS - Add setup custom commands here  #
#----------------------------------------------------#





def get_desktop_path():
    import os, re

    D_paths = list()

    try:

        fs = open(os.sep.join((os.path.expanduser("~"), ".config", "user-dirs.dirs")),'r')
        data = fs.read()
        fs.close()
    except:
        data = ""

    D_paths = re.findall(r'XDG_DESKTOP_DIR=\"([^\"]*)', data)

    if len(D_paths) == 1:
        D_path = D_paths[0]
        D_path = re.sub(r'\$HOME', os.path.expanduser("~"), D_path)

    else:
        D_path = os.sep.join((os.path.expanduser("~"), 'Desktop'))

    if os.path.isdir(D_path):
        return D_path
    else:
        return None



class install(_install):
    """
    Post Install Command Goes Here

    """

    def run(self):
        _install.run(self)

        pwd = os.getcwd()

        # Post Install code goes here.

        print "\n\n"
        print \
            """

        --------------------------------
        |   INSTALLATION DONE           |
        --------------------------------
        """


class CreateDocumentation(Command):
    """
    Create Documentation Using Epydoc
    """
    user_options = []
    description = "Create Project Documentation"

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        from subprocess import call
        import webbrowser

        print(" => bootstrapping development environment ...")

        call([PYTHON, EPYDOC, '-v', '--html', '-n', PACKAGE_NAME, '-o', 'docs', PACKAGE_NAME])
        webbrowser.open(INDEX_HTML)


class TestDocumentation(Command):
    """
    Create Documentation Using Epydoc
    """
    user_options = []
    description = "Create Project Documentation"

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        import webbrowser

        print(" => bootstrapping development environment ...")
        webbrowser.open(INDEX_HTML)


DESKTOP = get_desktop_path()

setup(
    cmdclass={'install': install, 'doc': CreateDocumentation, 'test_doc': TestDocumentation},

    name=PACKAGE_NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    long_description=README,
    #packages=['PyXExcel', 'test'],
    test_suite="test",

    py_modules=[PACKAGE_NAME],

    packages=find_packages(),

    #include_package_data=True,
    package_data=PACKAGE_DATA,
    description=DESCRIPTION,
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    data_files = [
        ('/usr/share/encfsgtk',         ['data/icon.png']),
        ('/usr/share/applications/',    ['data/encfsgtk.desktop']),
        (DESKTOP,                       ['data/encfsgtk.desktop']),
    ]
    #data_files=[('data/icon.png', ['/usr/share/encfsgtk']),
    #            ('data/encfsgtk.desktop', ['/usr/share/applications/'])]

)