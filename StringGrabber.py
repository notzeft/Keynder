#!/usr/bin/env python
# coding: utf-8

import os, sys,zipfile,subprocess,tempfile,string

class StringGrabber():

    def __init__(self,directory):
        self.directory = directory

    def ini_listFiles(self,list_files,directory): #Initialise la liste_filesavec les noms des fichiers(directory et subdirectory recursivement)
        # r=root, d=directories, f = files
        for r, d, f in os.walk(directory):
            for file in f:
                list_files.append(os.path.join(r, file))



    def unzip(self,file,extract_location): #unizp un file zip et mets les extract dans extract_location
        zip_ref = zipfile.ZipFile(file, 'r')
        zip_ref.extractall(extract_location)
        zip_ref.close()
        os.system("rm -rf " + file)

    def extract_lines(self,file,directory,list_data): #traite les fichiers binaires: elle copie le contenu du fichier binaire dans temp.txt pui dans temp.txt elle met chaque cle ou certificat dans la liste finale
        all = os.popen('strings ' + file+' 2>/dev/null').read()
    
        with open(directory + "temp.txt","a",encoding='utf-8',errors='ignore') as file_bin:
            file_bin.write(str(all).rstrip("\n"))
        with open(directory + "temp.txt","r",encoding='utf-8', errors='ignore') as file_bin1:
            data = file_bin1.readlines()
            string=""
            begin_data = ["-----BEGIN PUBLIC KEY-----","-----BEGIN EC PRIVATE KEY-----","-----BEGIN RSA PRIVATE KEY-----","-----BEGIN CERTIFICATE-----"]
            end_data = ["-----END PUBLIC KEY-----","-----END EC PRIVATE KEY-----","-----END RSA PRIVATE KEY-----","-----END CERTIFICATE-----"]
            for line in data:
                string=string + line
                if any(begin in line for begin in begin_data):
                    string=""
                    pos = line.find("-----BEGIN")
                    string= string + line[pos:]
                if any(end in line for end in end_data):
                    list_data.append(string)
                
        os.system("rm -rf " + directory + "temp.txt")
        os.system("rm -rf " + file)

    def der_file(self,list_files,list_data): #Pour chaque ficher , on mets son contenu dans la liste finale
        files = {}
        for filename in list_files:
            if os.path.isfile(filename):
                if filename.endswith(".der"):
                    with open(filename, "rb") as file:
                        if filename in files:
                            continue
                        files[filename] = file.read()

        for filename, text in files.items():
            list_data.append(text)



    def DataFiles_to_DataList(self,fullpath):
        tmp = tempfile.TemporaryDirectory()
        temporary_path = tmp.name+'/'
        DataList = []
        filenames =[]
    
        dir = fullpath #dossier dans lequel il y'a tout les fichier de cles:bin,zip,txt,der,sous-repertoires ,etc..
        temp_dir = temporary_path #repertoire  pour travailler dessus
        to_create = "CreatedRep" # repertoire qui sera cree temporairement
        dir_create = temp_dir + to_create
        if os.path.exists(dir_create):
            os.system("rm -rf " + dir_create)

        os.system("mkdir " + dir_create)
        os.system("cp -R " + dir + "* " + dir_create )

        filenames = []
        self.ini_listFiles(filenames,dir_create)
        for filename in filenames:
            if filename.endswith(".zip"):
                self.unzip(filename,dir_create)
            
        self.ini_listFiles(filenames,dir_create) #filenames est reinitialise avec les nouveaux fichiers
        self.der_file(filenames,DataList)
        
        self.ini_listFiles(filenames,dir_create) 
        for filename in filenames:
            self.extract_lines(filename,dir_create,DataList)
            self.ini_listFiles(filenames,dir_create)

        os.system("rm -rf " + dir_create)
        #DataList = [data.replace('\n', ' ') for data in DataList]

        return DataList
    
    def get_data(self):
        return self.DataFiles_to_DataList(self.directory)
    
######################## Execution de la fonction principale
# directory = '/mnt/hgfs/Home/Google\ Drive/M2/projet-GN/data/working'
# # # Full Path de notre dossier a traiter


#directory = '/root/Documents/projet_GN/projet-GN-fin/projet-GN/data'
#sg = StringGrabber(directory)
#data = sg.get_data()
#print(data)



