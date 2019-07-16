#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 19:26:41 2019

@author: lounis
"""
from OpenSSL.crypto import *
from Crypto.PublicKey import *
from Exceptions import *

class Key:
    def __init__(self, data):
        self.data_brut = data
        self.algo = None
        self.tipe = None
        self.taille = 0
        self.form = 'PEM'
        self.data = None
        self.pubkey = None
        self.set_key()
             
    def recherche_mot(self,mot):
        return self.data_brut.find(mot)

    def set_public_key(self):
        if self.tipe == 'Pri':
            self.pubkey = dump_publickey(FILETYPE_PEM, self.pkey)
        elif self.tipe == 'Pub':
            self.pubkey = self.data
        
    def set_key(self):
        pri = self.recherche_mot('PRIVATE')
        pub = self.recherche_mot('PUBLIC')
        if(pri!=-1):
            self.tipe = 'Pri'
            try: #try PEM
                self.pkey = load_privatekey(FILETYPE_PEM, self.data_brut)
                self.data = dump_privatekey(FILETYPE_PEM, self.pkey)

            except: #try DER
                try:
                    self.pkey = load_privatekey(FILETYPE_ASN1, self.data_brut)
                except:
                    self.pkey = None
                    raise unknownTypeException()
        elif(pub!=-1):
            self.tipe = 'Pub'
            try: #try PEM
                self.pkey = load_publickey(FILETYPE_PEM, self.data_brut)
                self.data = dump_publickey(FILETYPE_PEM, self.pkey)
            except: #try DER
                try:
                    self.pkey = load_publickey(FILETYPE_ASN1, self.data_brut)
                except:
                    self.pkey = None
                    raise unknownTypeException()
        self.set_algo()
        self.taille = self.pkey.bits()
        self.set_public_key()
            
    def set_algo(self):
        if self.pkey.type() == 408:
            self.algo = 'ECC'
        elif self.pkey.type() == 6:
            self.algo = 'RSA'

    def get_pkey(self):
        return self.pkey

    # Checks if the key format is PEM and converts it otherwise.
    def check_format(self):
        return True
        
    def print_key(self):
        print(self.cle)
        print(self.algo+'.'+self.tipe)
        print(self.taille)
        
        

