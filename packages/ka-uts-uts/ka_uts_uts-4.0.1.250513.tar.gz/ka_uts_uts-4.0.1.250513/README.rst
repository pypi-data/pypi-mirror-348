##########
ka_uts_uts
##########

Overview
********

.. start short_desc

**Utilities for Application Setup and Package Management**

.. end short_desc

Installation
************

.. start installation

The package ``ka_uts_uts`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: shell

	$ python -m pip install ka_uts_uts

To install with ``conda``:

.. code-block:: shell

	$ conda install -c conda-forge ka_uts_uts

.. end installation

Package logging 
***************

(c.f.: **Appendix**: `Package Logging`)

Package files
*************

Classification
==============

The Package ``ka_uts_uts`` consist of the following file types (c.f.: **Appendix**):

#. **Special files:** (c.f.: **Appendix:** *Special python package files*)

#. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

#. **Modules**

   #. **Control *Modules**

      a. *do.py*
      #. *parms.py*
      #. *task.py*

   #. **Application Modules**

      #. *setup.py*

#. **Sub-packages**

   a. **ioc:** *(I/O Control)*

      #. **Special files:** (c.f.: **Appendix:** *Special python package files*)

      #. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

      #. **Modules**

          #. *jinja2.py*
          #. *yaml.py*

   #. **utils:** *(Utilities)*

      #. **Special files:** (c.f.: **Appendix:** *Special python package files*)

      #. **Dunder modules:** (c.f.: **Appendix:** *Special python package modules*)

      #. **Modules**

         #. *pacmod.py*
         #. *pac.py*

Control Modules
***************

The Package ``ka_uts_uts`` contains the following Control modules.

  .. ka_uts_uts-Control-Modules-label:
  .. table:: *ka_uts_uts Control Modules*

   +--------+----------------------------------------+
   |Name    |Decription                              |
   +========+========================================+
   |do.py   |Main control with Do class and do method|
   +--------+----------------------------------------+
   |parms.py|Parameter control                       |
   +--------+----------------------------------------+
   |task.py |Mail Task management                    |
   +--------+----------------------------------------+

Application Modules
*******************

The Package ``ka_uts_uts`` contains the following Application modules.

  .. ka_uts_uts-Application-Modules-label:
  .. table:: *ka_uts_uts Application Modules*

   +----------+-----------------------+
   |Name      |Decription             |
   +==========+=======================+
   |setup.py  |Application Setup      |
   +----------+-----------------------+

Sub-package: `ioc (I/O Control)`
********************************

Modules
=======

The Sub-package ``ioc`` contains the following modules.

  .. ioc-Modules-label:
  .. table:: *ioc Modules*

   +----------+-------------------------------------+
   |Name      |Decription                           |
   +==========+=====================================+
   |jinja\_.py|I/O Control methods for jinja2 files.|
   +----------+-------------------------------------+
   |yaml\_.py |I/O Control methods for yaml files.  |
   +----------+-------------------------------------+

Module: jinja2\_.py
-------------------

The Module ``jinja2_.py`` contains the static class ``Jinja2``

jinja2\_.py Class: Jinja2
^^^^^^^^^^^^^^^^^^^^^^^^^

The static Class ``Jinja2`` provides I/O Control methods for Jinja2 files;
it contains the subsequent methods.

Jinja2 Methods
""""""""""""""

  .. Jinja2-Methods-label:
  .. table:: *Jinja2 Methods*

   +-------------+------------------------------+
   |Name         |Description                   |
   +=============+==============================+
   |read         |Read log file path with jinja |
   +-------------+------------------------------+
   |read_template|Read log file path with jinja2|       
   +-------------+------------------------------+

Jinja2 Method: read
"""""""""""""""""""

Parameter
.........

  .. Jinja2-Method-read-Parameter-label:
  .. table:: *Jinja2 Method read: Parameter*

   +--------+-----+---------------+
   |Name    |Type |Description    |
   +========+=====+===============+
   |pacmod  |TnDic|               |
   +--------+-----+---------------+
   |filename|str  |               |
   +--------+-----+---------------+

Jinja2 Method: read_template
""""""""""""""""""""""""""""

Parameter
.........

  .. Jinja2-Method-read_template-Parameter-label:
  .. table:: *Jinja2 Method read_template: Parameter*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path string|
   +----+------+-----------+

Return Value
............

  .. Jinja2-Method-read_template-Return-Value-label:
  .. table:: *Jinja2 Method read_template: Return Value*

   +----+----------------+---------------+
   |Name|Type            |Description    |
   +====+================+===============+
   |    |TyJinja2Template|Jinja2 Template|
   +----+----------------+---------------+

Module: yaml\_.py
-----------------

The Module ``yaml_.py`` contains the static class ``Yaml``.

yamml\_.py Class: Yaml
^^^^^^^^^^^^^^^^^^^^^^

The static Class ``Yaml`` provides I/O Control functions for Yaml files;
it contains the subsequent methods

Yaml Methods
""""""""""""

  .. Yaml-Methods-label:
  .. table:: *Yaml Methods*

   +----+----------------------------------------------+
   |Name|Description                                   |
   +====+==============================================+
   |load|Load yaml string into any object using yaml   |
   |    |loader; default loader is yaml.safeloader     |
   +----+----------------------------------------------+
   |read|Read yaml file path into any object using yaml|
   |    |loder; default loader is yaml.safeloader      |
   +----+----------------------------------------------+

Yaml Method: read_with_safeloader
"""""""""""""""""""""""""""""""""

Parameter
.........

  .. Yaml-Method-read_with_safeloader-Parameter-label:
  .. table:: *Yaml Method read_with_safeloader: Parameter*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path string|
   +----+------+-----------+

Yaml Method: write
""""""""""""""""""

Parameter
.........

  .. Yaml-Method-write-Parameter:
  .. table:: *Yaml Method write: Parameter*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path string|
   +----+------+-----------+
   |obj |TyAny |Object     |
   +----+------+-----------+

Sub package: utils
******************

utils Modules
=============

The Sub-package ``utils`` contains the following modules.

  .. utils-Modules-label:
  .. table:: *utils Modules*

   +---------+---------------------------+
   |Name     |Functionality              |
   +=========+===========================+
   |pacmod.py|Manage Packages and Modules|
   +---------+---------------------------+
   |pac.py   |Manage Packages            |
   +---------+---------------------------+

utils Module: pacmod.py
-----------------------

The Module ``pacmod.py`` contains the static class ``PacMod``.

pacmod.py Class: PacMod
^^^^^^^^^^^^^^^^^^^^^^^

The static Class ``PacMod`` is used to get the Package- and Module-name.
it contains the subsequent methods

PacMod Methods
""""""""""""""

  .. PacMod Methods-label:
  .. table:: *PacMod Methods*

   +-------------------+-----------------------------------+
   |Name               |Description                        |
   +===================+===================================+
   |sh_d_pacmod        |Show (Get) package module          |
   |                   |dictionary for class.              |
   +-------------------+-----------------------------------+
   |sh_path_module_yaml|show package module yaml file path.|
   +-------------------+-----------------------------------+
   |sh_path_keys_yml   |show keys.yaml file path.          |
   +-------------------+-----------------------------------+
   |sh_path_cfg_yml    |show cfg.yaml file path.           |
   +-------------------+-----------------------------------+
   |sh_dir_type        |show type specific file directory. |
   +-------------------+-----------------------------------+
   |sh_path_pattern    |show pattern file path.            |
   +-------------------+-----------------------------------+

PacMod Method: sh_d_pacmod
""""""""""""""""""""""""""

Parameter
.........

  .. PacMod-Method-sh_d_pacmod-label:
  .. table:: *PacMode Method sh_d_pacmod: Parameter*

   +----+------+-----------+
   |Name|Type  |Description|
   +====+======+===========+
   |path|TyPath|Path string|
   +----+------+-----------+

Appendix
********

Package Logging
===============

Description
-----------

The Standard or user specifig logging is carried out by the log.py module of the logging
package ka_uts_log using the configuration files **ka_std_log.yml** or **ka_usr_log.yml**
in the configuration directory **cfg** of the logging package **ka_uts_log**.
The Logging configuration of the logging package could be overriden by yaml files with
the same names in the configuration directory **cfg** of the application packages.

Log message types
-----------------

Logging defines log file path names for the following log message types: .

#. *debug*
#. *info*
#. *warning*
#. *error*
#. *critical*

Application parameter for logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Application-parameter-used-in-log-naming-label:
  .. table:: *Application parameter used in log naming*

   +-----------------+---------------------------+----------+------------+
   |Name             |Decription                 |Values    |Example     |
   +=================+===========================+==========+============+
   |dir_dat          |Application data directory |          |/otev/data  |
   +-----------------+---------------------------+----------+------------+
   |tenant           |Application tenant name    |          |UMH         |
   +-----------------+---------------------------+----------+------------+
   |package          |Application package name   |          |otev_xls_srr|
   +-----------------+---------------------------+----------+------------+
   |cmd              |Application command        |          |evupreg     |
   +-----------------+---------------------------+----------+------------+
   |pid              |Process ID                 |          |æevupreg    |
   +-----------------+---------------------------+----------+------------+
   |log_ts_type      |Timestamp type used in     |ts,       |ts          |
   |                 |logging files|ts, dt       |dt        |            |
   +-----------------+---------------------------+----------+------------+
   |log_sw_single_dir|Enable single log directory|True,     |True        |
   |                 |or multiple log directories|False     |            |
   +-----------------+---------------------------+----------+------------+

Log type and Log directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Single or multiple Application log directories can be used for each message type:

  .. Log-types-and-Log-directories-label:
  .. table:: *Log types and directoriesg*

   +--------------+---------------+
   |Log type      |Log directory  |
   +--------+-----+--------+------+
   |long    |short|multiple|single|
   +========+=====+========+======+
   |debug   |dbqs |dbqs    |logs  |
   +--------+-----+--------+------+
   |info    |infs |infs    |logs  |
   +--------+-----+--------+------+
   |warning |wrns |wrns    |logs  |
   +--------+-----+--------+------+
   |error   |errs |errs    |logs  |
   +--------+-----+--------+------+
   |critical|crts |crts    |logs  |
   +--------+-----+--------+------+

Log files naming
^^^^^^^^^^^^^^^^

Naming Conventions
""""""""""""""""""

  .. Naming-conventions-for-logging-file-paths-label:
  .. table:: *Naming conventions for logging file paths*

   +--------+-------------------------------------------------------+-------------------------+
   |Type    |Directory                                              |File                     |
   +========+=======================================================+=========================+
   |debug   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |info    |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |warning |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |error   |/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+
   |critical|/<dir_dat>/<tenant>/RUN/<package>/<cmd>/<Log directory>|<Log type>_<ts>_<pid>.log|
   +--------+-------------------------------------------------------+-------------------------+

Naming Examples
"""""""""""""""

  .. Naming-examples-for-logging-file-paths-label:
  .. table:: *Naming examples for logging file paths*

   +--------+--------------------------------------------+------------------------+
   |Type    |Directory                                   |File                    |
   +========+============================================+========================+
   |debug   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|debs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |info    |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|infs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |warning |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|wrns_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |error   |/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|errs_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+
   |critical|/data/otev/umh/RUN/otev_xls_srr/evupreg/logs|crts_1737118199_9470.log|
   +--------+--------------------------------------------+------------------------+

Python Terminology
==================

Python packages
---------------

  .. Python packages-label:
  .. table:: *Python packages*

   +-----------+-----------------------------------------------------------------+
   |Name       |Definition                                                       |
   +===========+==========+======================================================+
   |Python     |Python packages are directories that contains the special module |
   |package    |``__init__.py`` and other modules, packages files or directories.|
   +-----------+-----------------------------------------------------------------+
   |Python     |Python sub-packages are python packages which are contained in   |
   |sub-package|another pyhon package.                                           |
   +-----------+-----------------------------------------------------------------+

Python package Sub-directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  .. Python package-Sub-directories-label:
  .. table:: *Python packages Sub-directories*

   +----------------------+-------------------------------+
   |Name                  |Definition                     |
   +======================+==========+====================+
   |Python package        |Sub-directories are directories|
   |sub-directory         |contained in python packages.  |
   +----------------------+-------------------------------+
   |Special Python package|Python package sub-directories |
   |sub-directory         |with a special meaning.        |
   +----------------------+-------------------------------+

Special python package Sub-directories
""""""""""""""""""""""""""""""""""""""

  .. Special-python-package-Sub-directories-label:
  .. table:: *Special python Sub-directories*

   +-------+------------------------------------------+
   |Name   |Description                               |
   +=======+==========================================+
   |bin    |Directory for package scripts.            |
   +-------+------------------------------------------+
   |cfg    |Directory for package configuration files.|
   +-------+------------------------------------------+
   |data   |Directory for package data files.         |
   +-------+------------------------------------------+
   |service|Directory for systemd service scripts.    |
   +-------+------------------------------------------+

Python package files
^^^^^^^^^^^^^^^^^^^^

  .. Python-package-files-label:
  .. table:: *Python package files*

   +--------------+---------------------------------------------------------+
   |Name          |Definition                                               |
   +==============+==========+==============================================+
   |Python        |Files within a python package.                           |
   |package files |                                                         |
   +--------------+---------------------------------------------------------+
   |Special python|Package files which are not modules and used as python   |
   |package files |and used as python marker files like ``__init__.py``.    |
   +--------------+---------------------------------------------------------+
   |Python package|Files with suffix ``.py``; they could be empty or contain|
   |module        |python code; other modules can be imported into a module.|
   +--------------+---------------------------------------------------------+
   |Special python|Modules like ``__init__.py`` or ``main.py`` with special |
   |package module|names and functionality.                                 |
   +--------------+---------------------------------------------------------+

Special python package files
""""""""""""""""""""""""""""

  .. Special-python-package-files-label:
  .. table:: *Special python package files*

   +--------+--------+---------------------------------------------------------------+
   |Name    |Type    |Description                                                    |
   +========+========+===============================================================+
   |py.typed|Type    |The ``py.typed`` file is a marker file used in Python packages |
   |        |checking|to indicate that the package supports type checking. This is a |
   |        |marker  |part of the PEP 561 standard, which provides a standardized way|
   |        |file    |to package and distribute type information in Python.          |
   +--------+--------+---------------------------------------------------------------+

Special python package modules
""""""""""""""""""""""""""""""

  .. Special-Python-package-modules-label:
  .. table:: *Special Python package modules*

   +--------------+-----------+-----------------------------------------------------------------+
   |Name          |Type       |Description                                                      |
   +==============+===========+=================================================================+
   |__init__.py   |Package    |The dunder (double underscore) module ``__init__.py`` is used to |
   |              |directory  |execute initialisation code or mark the directory it contains as |
   |              |marker     |a package. The Module enforces explicit imports and thus clear   |
   |              |file       |namespace use and call them with the dot notation.               |
   +--------------+-----------+-----------------------------------------------------------------+
   |__main__.py   |entry point|The dunder module ``__main__.py`` serves as an entry point for   |
   |              |for the    |the package. The module is executed when the package is called by|
   |              |package    |the interpreter with the command **python -m <package name>**.   |
   +--------------+-----------+-----------------------------------------------------------------+
   |__version__.py|Version    |The dunder module ``__version__.py`` consist of assignment       |
   |              |file       |statements used in Versioning.                                   |
   +--------------+-----------+-----------------------------------------------------------------+

Python elements
---------------

  .. Python elements-label:
  .. table:: *Python elements*

   +---------------------+--------------------------------------------------------+
   |Name                 |Description                                             |
   +=====================+========================================================+
   |Python method        |Python functions defined in python modules.             |
   +---------------------+--------------------------------------------------------+
   |Special python method|Python functions with special names and functionalities.|
   +---------------------+--------------------------------------------------------+
   |Python class         |Classes defined in python modules.                      |
   +---------------------+--------------------------------------------------------+
   |Python class method  |Python methods defined in python classes                |
   +---------------------+--------------------------------------------------------+

Special python methods
^^^^^^^^^^^^^^^^^^^^^^

  .. Special-python-methods-label:
  .. table:: *Special python methods*

   +--------+------------+----------------------------------------------------------+
   |Name    |Type        |Description                                               |
   +========+============+==========================================================+
   |__init__|class object|The special method ``__init__`` is called when an instance|
   |        |constructor |(object) of a class is created; instance attributes can be|
   |        |method      |defined and initalized in the method.                     |
   +--------+------------+----------------------------------------------------------+

Table of Contents
=================

.. contents:: **Table of Content**
