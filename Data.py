#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 20:00:13 2019

@author: root
"""

class Data:    
    def __init__(self, d):
        self.data = d
        self.set_type()
        
    def recherche_mot(self, mot, data):
        return data.find(mot)
        
    def is_it_this(self,mot):
        if self.recherche_mot(mot, self.data) != -1:
            return True
        else:
            return False
        
    def set_type(self): #type de clé
        # PEM
        if(type(self.data) == bytes):
            self.my_type = 'DER'
        else:
            if(self.is_it_this('KEY')):
                if self.is_it_this('ENCRYPTED') == False:
                    self.my_type = 'KEY'
                else:
                    self.my_type ='ENC'
            elif(self.is_it_this('CERTIFICATE')):
                 self.my_type = 'CRT'
            else:
                self.my_type = 'N/A'
