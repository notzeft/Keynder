from src.data import Data
from src.key import Key
from src.certificate import Certificate
from src.stringgrabber import StringGrabber as Grabber
from src.exceptions import *


class Classifier:
    def __init__(self, grabber):
        self.data_list = grabber.get_data()
        self.objects_list = []
        self.keys_list = None
        self.certs_list = None

    def detect_type(self):
        for data in self.data_list:
            d = Data(data)
            if(d.my_type == 'ENC'):
                continue
            elif('KEY' in d.my_type):
                d = Key(data)  # creation de la class Key
            elif('CRT' in d.my_type):
                try:
                    # creation de la class Certificat avec PEM
                    d = Certificate(data, 'PEM')
                except:
                    continue

            elif('DER' in d.my_type):
                try:
                    # creation de la class Certificat avec DER
                    d = Certificate(data, 'DER')
                except:
                    continue
            self.objects_list.append(d)
        return len(self.objects_list)

    def remove_duplicate(self):
        liste_keys = []
        liste_certifs = []
        # Tri du tableau de base pour créer une liste de cetificats et une
        # liste de clés
        for objet in self.objects_list:
            if type(objet) is Key:
                liste_keys.append(objet)
            elif type(objet) is Certificate:
                liste_certifs.append(objet)
            else:
                continue

        # On supprime les doublons de clés
        for k1 in liste_keys:
            index = liste_keys.index(k1)
            for k2 in liste_keys[index + 1:]:
                if k1.data == k2.data:
                    index2 = liste_keys.index(k2)
                    del liste_keys[index2]

        # On supprime les doublons dans les certificats
        for c1 in liste_certifs:
            index = liste_certifs.index(c1)
            for c2 in liste_certifs[index + 1:]:
                if c1.pub_key == c2.pub_key:
                    index2 = liste_certifs.index(c2)
                    del liste_certifs[index2]

        # On supprime les clés publiques des certificats
        for k in liste_keys:
            index = liste_keys.index(k)
            for c in liste_certifs:
                if str(k.data).rstrip("\n\r") == str(c.pub_key.rstrip("\n\r")):
                    del liste_keys[index]

        # return liste_keys,liste_certifs
        self.keys_list = liste_keys
        self.certs_list = liste_certifs

    def classify(self):
        self.detect_type()
        self.remove_duplicate()

    def get_data(self):
        return self.certs_list, self.keys_list


if __name__ == '__main__':
    directory = '/mnt/hgfs/Home/Google\ Drive/M2/projet-GN/data/'
    grabber = Grabber(directory)
    classifier = Classifier(grabber)
    classifier.classify()
    print(classifier.objects_list)
