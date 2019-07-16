import getopt
import sys
from src.db import Database
from src.Classifier import Classifier
from src.Key import Key
from src.Certificate import Certificate
from src.StringGrabber import StringGrabber as Grabber

# The help function prints the usage file (used in case of an error)
def help(): 
    helpfile = open('read.me','r')
    helptext = helpfile.read()
    print(helptext)
    
def main():
    directory = ''
    match = False
    inject = False
    db_name = 'certs.db'
    output = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hd:midb:-o',['help','directory=','match','inject','database=','--output'])
    except:
        help()
    for opt,arg in opts:
        if opt in ('-h','--help'):
            print('printing hep')
            help()
        elif opt in ('-d','--directory'):
            directory = arg
            if(not directory.endswith('/')):
                directory += '/'
        elif opt in ('-m','--match'):
            match = True
        elif opt in ('-i','--inject'):
            inject = True
        elif opt in ('-b','--database'):
            db = arg
        elif opt in ('-o','--output'):
            output = True
            outputfile = arg
            if(outputfile==''):
                outputfile = 'matches.txt'
    if(directory):       
        print("Grabbing data...")
        grabber = Grabber(directory)
        classifier = Classifier(grabber)
        print("Classifying...")
        classifier.classify()
        certs, keys = classifier.get_data()
    db = Database(db_name)
    if(inject):
        try:
            print("Creating the database")
            db.create_db()
        except:
            print("Database already exists.")
        print("Injecting data into the database...")
        db.insert_keys(keys)
        db.insert_certs(certs)
    if(match):
        print("Matching data...")
        db.match_cert_key()
    if(output):
        db.export_matches(outputfile)
    
    
main()
                   
# directory = '/mnt/hgfs/Home/Google\ Drive/M2/projet-GN/data/keypairs'
# grabber = Grabber(directory)
# classifier = Classifier(grabber)
# classifier.classify()
# print(classifier.objects_list)
       
# db = Database('certs.db')
#db = Database('testpy.db')
# rsa_pub = '''-----BEGIN PUBLIC KEY-----
# MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAtEwZm19PD1amHL7ezahR
# FQhTesQKDtSiK2TYcQSoyOLTBlvCSBGS5bteL+6RW1De59ZPv+s7pG/GK/h7Ms5T
# ivdj9ATsnwmxqXjtNvZf9Z0itRWPKBboebW/cv4i9syFOn5cvxsN2YVbzEpQ5dHc
# SZyUru1hgPEepO3X75v9eZFy207QZeIVrKixCCaLQbxFdhpSX7hp2IE+ZcudtcTx
# mmLKdmH8NmFwjApSL5NJ6+IIzdMxxRe2PZeWb43o3LY8du8cMMouL0cbqjvV28Tx
# f6zMUfhf1jILLcZs147O4V9BvwTc6kLkfp46YMQ1WxTSznMVfugimi1jQw7c4+I/
# 6QBqkEDgN6xmGHz8nsjm5IEzAhAgP/gyBxKEH2TRPehYhjQ3kAYioWaj7X/ymUEh
# SAoPlN0bFmBgNuM5aoujgQ9VMlBbgAeN0QxTCg+l8NHhlMuV1zQuDMb0bnOG0+eM
# 7Ihk+MGfmvWkp2ilvSdRzngu39VK8ExPaGKZHidJ+13yYxaka6O0ydxfG0T5ZwD1
# gLbs83y/wlKCEJQLKVMjmzlJvqOlKF10nSN87XynlKvK1qarxm46YGiGl/ezRBKG
# WoWQVIoeedJVk+kTmfshbg4KoSVtnYxso1w+KPUZkNoGCNyouMfxuRBUqCa/4uJu
# aDZVi2LZXsttZCB4TGDPUI0CAwEAAQ==
# -----END PUBLIC KEY-----
# '''
#db.create_db()
# db.match_cert_key()
# key = Key(rsa_pub)
# db.insert_key(key)
# keys_tab = [key]
# db.insert_keys(keys_tab)
# db.test()
