class unknownTypeException(Exception):
    def __init__(self):
        message = "Unkown data type! This program only accepts certificates and crypto keys."
        super(unknownTypeException, self).__init__(message)


if __name__ == '__main__':
    pass
