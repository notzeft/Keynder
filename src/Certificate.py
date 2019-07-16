#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:24:08 2019

@author: lounis
"""
from OpenSSL.crypto import *

class Certificate:
    def __init__(self, data, forma):
        self.data = data
        self.signature = ''
        self.issuer = ''
        self.validity_b = ''
        self.validity_f = ''
        self.forma = forma
        self.algo_pk = ''
        self.taille = 0
        self.publickey = None
        self.certificate = 'BINARY_SHIT'
        
        try:
            self.format_certificate()
        except certificateFormatingException:
            print("An error occured while converting certificate to the right format!")
            # Get certificate meta-data
        self.create_certificate()
        
    # This function uses openssl to write the certificate in the right format and gathers meta-data
    def format_certificate(self):
        pass
    
    def recherche_mot(self, mot):
        return self.data.find(mot)
    
    def get_champ_certif(self,champ_deb, champ_fin):
        debut = self.recherche_mot(champ_deb)
        debut = debut + len(champ_deb) +1
        if debut != -1 :
            fin = self.recherche_mot(champ_fin)
            get = self.data[debut:fin]
            # get = get.replace(" ","")
            get = get.strip("\n")
            return get
        else:
            return False


    def get_format_certif(self,champ_deb, champ_fin):
        debut = self.recherche_mot(champ_deb)
        debut = debut 
        if debut != -1 :
            fin = self.recherche_mot(champ_fin) + len(champ_fin) +1
            get = self.data[debut:fin]
            # get = get.replace(" ","")
            get = get.strip("\n")
            return get
        else:
            return False

            
    
    def set_signature(self):
        self.signature = self.x509.get_signature_algorithm()     

    def set_issuer(self):
        issuer = self.x509.get_issuer()
        for component in issuer.get_components():
            self.issuer = component[0].decode('utf-8')+':'+component[1].decode('utf-8')+'/'
        
    def set_validity_b(self):
        self.validity_b = self.x509.get_notBefore()
        
    def set_validity_f(self):
        self.validity_f = self.x509.get_notAfter()
        
    def set_algo_pk(self):
        if self.x509.get_pubkey().type() == 6:
            self.algo_pk = "RSA"

        if self.x509.get_pubkey().type() == 408:
            self.algo_pk = "ECC"
            
    def set_taille(self):
        self.taille = self.x509.get_pubkey().bits()

	#OBJET PKEY
    def set_public_key(self):
        self.public_key = self.x509.get_pubkey() 
        
	
    def set_certificate(self):
        debut_cert = "-----BEGIN CERTIFICATE-----"
        fin_cert = "-----END CERTIFICATE-----"
        self.certificate = self.get_format_certif(debut_cert, fin_cert)
        
    #DATA KEY -----BEGIN PUBLIC KEY-----
    def get_pub_key(self):
        self.pub_key = dump_publickey(FILETYPE_PEM, self.public_key).decode('utf-8')

    def create_certificate(self):
        
        if(self.forma == 'DER'):
            self.x509 = load_certificate(FILETYPE_ASN1, self.data)
        else:
            self.set_certificate()
            self.x509 = load_certificate(FILETYPE_PEM, self.certificate)

        ##############SIGNATURE  
        self.set_signature()

        ###############ISSUER
        self.set_issuer()
        
        ###############Validity debut
        self.set_validity_b()
        
        ###############Validity fin
        self.set_validity_f()
        
        ################ PUB_ALGO
        self.set_algo_pk()
        
        ################ Taille de la clé
        self.set_taille()
        
        ################ PUBLIC KEY 
        self.set_public_key()

        self.get_pub_key()
        
        




  
