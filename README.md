# SSG - Dicom StoreSCU with GUI in Python
Script in Python which allows Dicom StoreSCU with a GUI.
## Pre-requisites
- [DCMTK](https://dicom.offis.de/dcmtk.php.en) (Dicom Toolkit):
    - For Windows (requires [Chocolatey](https://chocolatey.org/ "Chocolatey")): choco install dcmtk
    - For Linux: sudo apt install dcmtk
    - For Mac OS X (with [Fink](http://www.finkproject.org/download/index.php "Fink")): fink install dcmtk
    - For Mac OS X (with [MacPorts](https://www.macports.org/install.php "MacPorts")): port install dcmtk
- [Python](https://www.python.org/downloads/), an interpreted, high-level, general-purpose programming language:
    - For [Windows](https://www.python.org/ftp/python/3.8.4/python-3.8.4.exe)
    - For [Linux](https://www.python.org/downloads/source/)
    - For [Mac OS X](https://www.python.org/downloads/mac-osx/)
    - For [Other](https://www.python.org/download/other/)
## Installation
### Clone the repository
```sh
$ git clone https://github.com/baronsss/SSG
```
### Install the requirements
- #### With pip (Python 2)
    ```sh
    $ pip install -r requirements.txt
    ```
- #### With pip3 (Python 3)
    ```sh
    $ pip3 install -r requirements.txt
    ```
- #### With poetry
    ```sh
    $ poetry install
    ```
### Execute
- #### With Python 2
    ```sh
    $ python main.py
    ```
- #### With Python 3
    ```sh
    $ python3 main.py
    ```

License
----

GPL-3.0

**More features coming soon!**