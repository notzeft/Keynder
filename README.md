# Authors

* Aly Abdellatif
* Michel Estaben
* Aladdin Chettouh
* Koceila Chikhdene
* Lounis Berrabah
* Semi Dhouib


# Keynder

Keynder is a Python Program for matching Public and Private keys(Certificates,ASN.1,PEM,X509) in a given Folder(example : '~/Documents/'). Your Folder can contain any type of files(.bin,.zip,.txt,etc...). These keys and Certificates will be stocked in a database(created by default).



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

	python3 main.py -d '/home/project/directory/' -i -b 'mydatabase.db' -m #(for the whole procedure, grabbing, injecting and matching);

	python3 main.py -d '/home/project/directory/' -i -b 'mydatabase.db' #(for grabbing and injecting without matching into exisiting database or database with custom name);
	python3 main.py -d '/home/project/directory/' -b 'mydatabase.db' -m #(matches data into the already existing database);

	python3 main.py -d '/home/project/directory/' -i -m #(injects into the defaults database 'certs.db' and matches data. If the database does not exist it will create it).

```
## License
[GNU GENERAL PUBLIC LICENSE V3] (https://www.gnu.org/licenses/gpl-3.0.en.html)
