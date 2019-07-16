# Keynder
Keynder is a Python program for matching private keys with public keys (RSA, ECC) and certificates (ASN.1, PEM, X509) in a given folder (example : '~/Documents/').
Your folder can contains any type of files (.bin, .zip, .txt, ...). These keys and Certificates will be stored in a local database (created by default) or in an existing one (See Usage).

This project was created for the French National Gendarmerie.


## Installation
`Keynder` needs two external libraries :
* pyOpenSSl : https://github.com/pyca/pyopenssl
* pyCryptro : https://github.com/dlitz/pycrypto


## Usage
-h or --help:
	This options prints the help file.

-d or --directory:
	This option takes the root path of the top directory to be scanned.
	
-i or --inject:
	This option takes no argument and it indicates wether or not we neeed to inject the data into the database.

-b or --database:
	This option handles the argument containing the database name (or the complete path to it). If not provided, it would take the default name ('certs.db'). If it doesn't exist it will be created.
	
-m or --match:
	This option is to be executed with or without the injection option. In case it is executed without injection, it matches the data already existing in the database.


## Examples
```python
python3 main.py -d '/home/project/directory/' -i -b 'mydatabase.db' -m # (for the whole procedure, grabbing, injecting and matching)
python3 main.py -d '/home/project/directory/' -i -b 'mydatabase.db' # (for grabbing and injecting without matching into existing database or a database with a custom name)
python3 main.py -d '/home/project/directory/' -b 'mydatabase.db' -m # (matches data into the already existing database)
python3 main.py -d '/home/project/directory/' -i -m # (injects into the defaults database 'certs.db' and matches data. If the database does not exists it will create it)
```


## TODO
* Translates some french commentaries in english.


## Authors
* Aly Abdellatif
* Michel Estaben
* Aladdin Chettouh
* Koceila Chikdene
* Lounis Berrabah
* Semi Dhouib


## License
[GNU GENERAL PUBLIC LICENSE V3](https://www.gnu.org/licenses/gpl-3.0.en.html)
