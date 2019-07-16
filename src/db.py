import sqlite3
import os
import sys


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.con = sqlite3.connect(filename)
        self.db = self.con.cursor()

    def test(self):
        keys = self.db.execute("""SELECT * FROM keys;""")
        for key in keys:
            print(key)
        self.con.commit()

    def create_db(self):
        certs_table = """
        CREATE TABLE certs(
            pub_key TEXT PRIMARY KEY NOT NULL,
            signature TEXT,
            issuer TEXT,
            validity TEXT,
            pub_key_size INTEGER,
            pub_key_id INTEGER,
            format TEXT CHECK(format in ('PEM','DER')),
            certificate TEXT NOT NULL UNIQUE,
            pri_key TEXT UNIQUE,

            FOREIGN KEY(pri_key) REFERENCES keys(pub_key)
            FOREIGN KEY(pub_key_id) REFERENCES keys(id)
        );
        """

        keys_table = """
        CREATE TABLE keys(
            id INTEGER PRIMARY KEY NOT NULL,
            pub_key TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type in ('Pri','Pub')),
            algo TEXT NOT NULL CHECK(algo in ('ECC','RSA')),
            size INTEGER NOT NULL,
            format TEXT NOT NULL CHECK(format in ('DER','PEM')),
            key TEXT NOT NULL UNIQUE,
            cert_id TEXT,
            FOREIGN KEY(cert_id) REFERENCES certs(pub_key)
        );
        """

        query = certs_table + keys_table
        self.db.executescript(query)
        self.con.commit()

    def insert_many(self, keys):
        keys_list = []
        for key in keys:
            data = key.key
            tipe = key.tipe
            algo = key.algo
            size = key.taille
            form = key.form
            keys_list.append((data, tipe, algo, size, form))
        query = """
        INSERT INTO keys(data,type,algo,size,format) VALUES (?,?,?,?,?);
        """
        self.db.executemany(query, keys_list)
        self.con.commit()

    def insert_keys(self, keys):
        for key in keys:
            self.insert_key(key)

    def insert_certs(self, certs):
        for cert in certs:
            self.insert_cert(cert)

    def insert_key(self, key):
        query = """
        INSERT INTO keys(pub_key,key,type,algo,size,format)
        VALUES ({pub_key},{data},{tipe},{algo},{size},{form});
        """.format(
            pub_key="'" + key.pubkey.decode('utf-8') + "'",
            data="'" + key.data.decode('utf-8') + "'",
            tipe="'" + key.tipe + "'",
            algo="'" + key.algo + "'",
            size="'" + key.taille + "'",
            form="'" + key.form + "'",
        )
        print(query)
        try:
            self.db.executescript(query)
        except Exception as e:
            print("Duplicates problem :", e, file=sys.stdout)
        self.con.commit()

    def insert_cert(self, cert):
        query = """
        INSERT INTO certs(pub_key,signature,issuer,validity,format,certificate)
        VALUES ({pub_key},{signature},{issuer},{validity},{form},{certificate});
        """.format(
            pub_key="'" + cert.pub_key + "'",
            signature="'" + cert.signature.decode('utf-8') + "'",
            issuer="'" + cert.issuer + "'",
            validity="'" + cert.validity_f.decode('utf-8') + "'",
            form="'" + cert.forma + "'",
            certificate="'" + cert.certificate + "'"
        )
        try:
            self.db.executescript(query)
        except Exception as e:
            print(e)
        self.con.commit()

    def match_cert_key(self):
        query_select = """
        SELECT keys.id,keys.key,certs.pub_key
        FROM keys,certs
        WHERE keys.type=\'Pri\' AND
              certs.pub_key=keys.pub_key;
        """
        query_update = """
        UPDATE certs
        SET pub_key_id={}
        WHERE certs.pub_key={};
        """

        results = self.db.execute(query_select)
        for res in results:
            update_query = query_update.format(res[0], '\'' + res[2] + '\'')
            for r in res:
                print(r)
        self.db.executescript(update_query)
        self.con.commit()

    def export_matches(self, output_file):
        query = """
        SELECT keys.id,keys.pub_key,certs.pub_key
        FROM keys,certs
        WHERE keys.type=\'Pri\' AND
              certs.pub_key=keys.pub_key;
        """
        command = """sqlite3 -header -csv {} {} > {}""".format(
            self.filename, '"' + query + '"', output_file)
        print(command)
        os.system(command)


if __name__ == '__main__':
    pass
