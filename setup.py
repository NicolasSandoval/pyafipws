
"Creador de instalador para PyAfipWs"

__author__ = "Mariano Reingart (reingart@gmail.com)"
__copyright__ = "Copyright (C) 2008-2019 Mariano Reingart"


import glob
import os
import subprocess
import sys
import warnings

from setuptools import setup

try:
    rev = subprocess.check_output(['hg', 'tip', '--template', '{rev}'],
                                  stderr=subprocess.PIPE).strip()
except BaseException:
    rev = 0

__version__ = "%s.%s.%s" % (sys.version_info[0:2] + (rev, ))

HOMO = True


kwargs = {}
desc = ("Interfases, tools and apps for Argentina's gov't. webservices "
        "(soap, com/dll, pdf, dbf, xml, etc.)")
kwargs['package_dir'] = {'pyafipws': '.'}
kwargs['packages'] = ['pyafipws', ]
opts = {}
data_files = [("pyafipws/plantillas", glob.glob("plantillas/*"))]
data_files += [("conf", glob.glob("conf/*"))]


long_desc = ("Interfases, herramientas y aplicativos para Servicios Web"
             "AFIP (Factura Electrónica, Granos, Aduana, etc.), "
             "ANMAT (Trazabilidad de Medicamentos), "
             "RENPRE (Trazabilidad de Precursores Químicos), "
             "ARBA (Remito Electrónico)")

# convert the README and format in restructured text (only when registering)
if "sdist" in sys.argv and os.path.exists("README.md") and sys.platform == "linux2":
    try:
        cmd = ['pandoc', '--from=markdown', '--to=rst', 'README.md']
        long_desc = subprocess.check_output(cmd).decode("utf8")
        open("README.rst", "w").write(long_desc.encode("utf8"))
    except Exception as e:
        warnings.warn("Exception when converting the README format: %s" % e)

# dependencias

requires_path = 'requirements.txt'
requires = []

if os.path.isfile(requires_path):
    with open(requires_path) as f:
        requires = f.read().splitlines()

dependency_links = ['https://github.com/pysimplesoap/pysimplesoap/tarball/stable_py3k#egg=pysimplesoap', ]


setup(name="PyAfipWs",
      version=__version__,
      description=desc,
      long_description=long_desc,
      author="Mariano Reingart",
      author_email="reingart@gmail.com",
      url="https://github.com/reingart/pyafipws",
      license="GNU GPL v3+",
      options=opts,
      data_files=data_files,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: Financial and Insurance Industry",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Operating System :: OS Independent",
          "Operating System :: Microsoft :: Windows",
          "Natural Language :: Spanish",
          "Topic :: Office/Business :: Financial :: Point-Of-Sale",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Software Development :: Object Brokering",
      ],
      keywords="webservice electronic invoice pdf traceability",
      **kwargs,
      install_requires=requires,
      dependency_links=dependency_links,
      zip_safe=False,
      )
