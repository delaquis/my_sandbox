from random import randint

class alphabet():

    note = "this is the standard lower case alphabet"
    __alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                         "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
                         "6", "7", "8", "9", "0", ".", ",", ":", ";", " ", "!", "?", "\n", "(", ")", "_",
                         "-", "[", "]", "'", "@"]  # specifies the alphabet used
    n = len(__alphabet)

    def __init__(self):
        print("I am an alphabet. Why are you creating me?")

    def getAlphabet(self):
        return alphabet.__alphabet

    def setAlphabet(self, _list):
        alphabet.__alphabet = _list
        alphabet.n = len(alphabet.__alphabet)
        print ("Warning: alphabet has been changed! DON'T FUCK IT UP!!")

    def toList(self, _string):
        # does some checks
        if type(_string) != type('str'):
            raise Exception("input is not a string: aborted!")
        elif _string == "":
            raise Exception("no string defined: aborted!")

        # starts process
        _list = []
        _dictionary = dict(zip(alphabet.__alphabet, range(0, alphabet.n)))
        for x in list(_string):
            if x in alphabet.__alphabet:
                _list.append(_dictionary[x])
            else:
                print("'" + x + "' is not in alphabet: droped character!")
        return _list

    def toString(self, _list):
        # does some checks
        if type(_list) != type([0, 1]):
            raise Exception("input is not a list: aborted!")
        if _list == []:
            raise Exception("no list defined: aborted!")

        # starts process
        _string = ""
        _dictionary = dict(zip(range(0, alphabet.n), alphabet.__alphabet))
        _temp = []
        for x in _list:
            if x >= 0 and x < alphabet.n:
                _temp.append(_dictionary[x])
            else:
                print(str(x) + ": is out of range.")
        _string = "".join(_temp)
        return _string
    # improvements:
    # handle alphabet change for completed strings

class cryString(alphabet):
    """cryString (class): this class is a container for a string. it inherits from alphabet."""

    def __init__(self, arg=None):
        self.string = ""    # contains the message in a string
        self.list = []      # contains the message in a numeric list
        self.tag = "empty"  # defines the type. e.g. klartext, geheimtext, dechiffrat, metatext, or empty
        self.log = []       # keeps track of the applied encryptions
        if arg is not None:
            if type(arg) == type(" "):
                self.string = arg
                self.complete()
            elif type(arg) == type([0, 1]):
                self.list = arg
                self.complete()
            else:
                print("cry.String.__init__: invalide argument for string generation! Generated empty string.")

    def complete(self):
        # is cryptostring empty?
        if self.string == "" and self.list == []:
            print("cryString.complete(): cryptostring is empty!")
            return 0

        # is cryptostring list missing?
        elif self.string != "" and self.list == []:
            self.list = self.toList(self.string)
            # print("cryString.complete(): done")
            return 0

        # is cryptostring string missing?
        elif self.list != [] and self.string == "":
            self.string = self.toString(self.list)
            # print("cryString.complete(): done")
            return 0

        # is cryptostring already completet?
        elif self.string == self.toString(self.list):
            # print("cryString.complete(): cryptostring was already completed")
            return 0

        # else it is not good!
        else:
            print("cryString.complete(): cryptostring is corrupted!")
            return 1

class cipher():
    """This class is a superclass for the ciphers! It must be specified in a sub class to contain the cryptographic algorithm and provides some function (e.g. encrypt and decrypt)."""

    def __init__(self):
        self.name = "none"
        self.version = "0.0"
        self.key = []
        self.input = cryString()
        self.output = cryString()
        self.n = self.input.n # alphabet length
        self.direction = 0 # encrypting or decrypting

    def setInput(self,_input):
        if type(_input) == type(self.input):
            if _input.list == []:
                _input.complete()
            print ("cipher: valid input string")
            self.input = _input
            self.n = self.input.n
        else: print ("cipher: not a valide input")

    def getOutput(self):
        return self.output

    def setKey(self,_list):
        self.key = _list
        raise NotImplementedError  # you want to override this on the child classes

    def getKey(self):
        raise NotImplementedError  # you want to override this on the child classes

    def generateRandomKey(self):
        raise NotImplementedError  # you want to override this on the child classes

    def encrypt(self):
        raise NotImplementedError  # you want to override this on the child classes

    def decrypt(self):
        raise NotImplementedError  # you want to override this on the child classes

    def execute(self):
        raise NotImplementedError  # you want to override this on the child classes

    def printOutput(self):
        self.output.complete()
        print(self.name + " output:")
        print(self.output.string)


# an example
class nullCipher(cipher):
    """This cipher does nothing - it allows to test the basic operations."""

    def __init__(self):
        cipher.__init__(self)
        self.name = "null cipher"
        self.version = "1.0"

    def setInput(self,_input):
        if type(_input) == type(self.input):
            if _input.list == []:
                _input.complete()
            print ("null cipher: valid input string")
            self.input = _input
            self.n = self.input.n
        else: print ("null cipher: not a valide input")

    def getOutput(self):
        if self.output.list == []:
            print ("null cipher: output is empty")
        print ("null cipher: returned output string")
        return self.output

    def setKey(self, _key):
        self.key = _key
        self.name = _key[0]
        self.version = _key[1]
        self.direction = _key[2]

    def getKey(self):
        return self.key

    def generateRandomKey(self):
        self.direction = 1
        self.key = [self.name,self.version,self.direction]

    def encrypt(self):
        print ("null cipher: 'encrypting'...")
        self.output.type = "encrypted"
        self.direction = 1
        self.output = self.input
        self.key = [self.name, self.version, self.direction]

    def decrypt(self):
        print ("null cipher: 'decrypting'...")
        self.output.type = "dechiffrat"
        self.direction = -1
        self.output = self.input
        self.key = [self.name, self.version, self.direction]

    def execute(self):
        if self.direction == 1:
            self.decrypt()
        elif self.direction == -1:
            self.encrypt()
        else: print ("execute(): direction is unclear.")

# the caesar cipher! (monoalphabetic substitution cipher)
class caesarCipher(cipher):
    """This the caesar cipher - it shifts all letters by 3 in the alphabet."""

    def __init__(self):
        cipher.__init__(self)
        self.name = "caesar cipher"
        self.version = "1.0"
        self.b = 3

    def setInput(self,_input):
        if type(_input) == type(self.input):
            if _input.list == []:
                _input.complete()
            # print ("caesar cipher: valid input string")
            self.input = _input
            self.n = self.input.n
        else: print ("caesar cipher: not a valide input")

    def getOutput(self):
        if self.output.list == []:
            print ("caesar cipher: output is empty")
        # print ("caesar cipher: returned output string")
        return self.output

    def setKey(self, _key):
        self.key = _key
        self.name = _key[0]
        self.version = _key[1]
        self.direction = _key[2]
        self.b = _key[3]

    def getKey(self):
        return self.key

    def generateRandomKey(self):
        self.direction = 1
        self.key = [self.name,self.version,self.direction,self.b]

    def encrypt(self):
        # print ("caesar cipher: 'encrypting'...")
        self.output.tag = "encrypted"
        self.direction = 1
        self.output.list = [(x + self.b) % self.n for x in self.input.list]
        self.key = [self.name, self.version, self.direction, self.b]

    def decrypt(self):
        # print ("caesar cipher: 'decrypting'...")
        self.output.tag = "dechiffrat"
        self.direction = -1
        self.output.list = [(x - self.b) % self.n for x in self.input.list]
        self.key = [self.name, self.version, self.direction, self.b]

    def execute(self):
        if self.direction == 1:
            self.decrypt()
        elif self.direction == -1:
            self.encrypt()
        else: print ("execute(): direction is unclear.")

# the affine cipher! (monoalphabetic substitution cipher)
class affineCipher(cipher):
    """This the vigenere cipher - it shifts all letters by a*x + b in the alphabet."""

    def __init__(self):
        cipher.__init__(self)
        self.name = "affine cipher"
        self.version = "1.0"
        self.a = 1
        self.b = 0

    def setInput(self,_input):
        if type(_input) == type(self.input):
            if _input.list == []:
                _input.complete()
            # print ("affine cipher: valid input string")
            self.input = _input
            self.n = self.input.n
        else: print ("affine cipher: not a valide input")

    def getOutput(self):
        if self.output.list == []:
            print ("affine cipher: output is empty")
        # print ("affine cipher: returned output string")
        return self.output

    def setKey(self, _key):
        self.key = _key
        self.name = _key[0]
        self.version = _key[1]
        self.direction = _key[2]
        self.a = _key[3]
        self.b = _key[4]

    def getKey(self):
        return self.key

    def generateRandomKey(self):
        self.direction = 1
        self.a = randint(1,self.n-1)
        self.b = randint(1,self.n)
        self.key = [self.name,self.version,self.direction,self.a,self.b]
        # print(self.a, self.b)

    def encrypt(self):
        # print ("affine cipher: 'encrypting'...")
        self.output.tag = "encrypted"
        self.direction = 1
        self.output.list = [(x*self.a + self.b) % self.n for x in self.input.list]
        self.key = [self.name, self.version, self.direction, self.a, self.b]

    def decrypt(self):
        # print ("affine cipher: 'decrypting'...")
        self.output.tag = "dechiffrat"
        self.direction = -1
        self.output.list = [(x - self.b) * self.a**(self.n-2)% self.n for x in self.input.list]
        self.key = [self.name, self.version, self.direction, self.a, self.b]

    def execute(self):
        if self.direction == 1:
            self.decrypt()
        elif self.direction == -1:
            self.encrypt()
        else: print ("execute(): direction is unclear.")

# the vigenere cipher!
class vigenereCipher(cipher):
    """This the vigenere cipher - it shifts all letters by a*x + b in the alphabet."""

    def __init__(self):
        cipher.__init__(self)
        self.name = "vigenere cipher"
        self.version = "1.0"
        self.password = cryString()

    def setInput(self,_input):
        if type(_input) == type(self.input):
            if _input.list == []:
                _input.complete()
            # print ("vigenere cipher: valid input string")
            self.input = _input
            self.n = self.input.n
        else: print ("vigenere cipher: not a valide input")

    def getOutput(self):
        if self.output.list == []:
            print ("vigenere cipher: output is empty")
        # print ("vigenere cipher: returned output string")
        return self.output

    def setKey(self, _key):
        self.key = _key
        self.name = _key[0]
        self.version = _key[1]
        self.direction = _key[2]
        self.password.string = _key[3]
        self.password.list = []
        self.password.complete()

    def getKey(self):
        return self.key

    def generateRandomKey(self):
        self.direction = 1
        self.password.string = "random"
        self.password.list = []
        self.password.complete()
        self.key = [self.name,self.version,self.direction,self.password.string]

    def encrypt(self):
        # print ("vigenere cipher: 'encrypting'...")
        self.output.tag = "encrypted"
        self.direction = 1
        self.output.list = [(self.input.list[i] + self.password.list[(i) % len(self.password.list)]) % self.n for i in range(len(self.input.list))]
        self.key = [self.name, self.version, self.direction, self.password.string]

    def decrypt(self):
        # print ("vigenere cipher: 'decrypting'...")
        self.output.tag = "dechiffrat"
        self.direction = -1
        self.output.list = [(self.input.list[i] - self.password.list[(i) % len(self.password.list)]) % self.n for i in range(len(self.input.list))]
        self.key = [self.name, self.version, self.direction, self.password.string]

    def execute(self):
        if self.direction == 1:
            self.decrypt()
        elif self.direction == -1:
            self.encrypt()
        else: print ("execute(): direction is unclear.")

    def setPassword(self,_string):
        if type(_string) != type(" "):
            print("set Password(): wrong statement")
        else:
            self.password.string = _string
            self.password.list = []
            self.password.complete()
            self.key[3] = _string


# atbash cipher! (monoalphabetic substitution cipher) reverse alphabet