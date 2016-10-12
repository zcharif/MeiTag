import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

import socket
import TCP
from TCP import send, receive

import PKCSEncryptDecrypt
from PKCSEncryptDecrypt import keyGen, RSAencrypt, RSAdecrypt

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import SymmetricCryptoTest
from SymmetricCryptoTest import encryptF, decryptF

import time

class MeiClient:
    def saltGen(self, byteSize=16):
        return os.urandom(byteSize)

    def setup(self):
        keySet = keyGen() #has a tuple of the key, and the public key
        privKey=keySet[0]
        pubKey=keySet[1]
        
        print('Sending Public Key')
        send(pubKey.exportKey(),self.IP)
        
        serverKey = RSA.importKey(receive(self.IP))
        
        print('Sending ID')
        send(RSAencrypt(self.MYNAME, serverKey),self.IP)

        print('Waiting on server response')
        response = receive(self.IP)

        if response != self.LOGINMESSAGE:
            print('Failed to login')
            return False

        print('Sending salt') #In future implementations, may want to figure out how to encrypt this.
        keySalt=self.saltGen()

        send(keySalt, self.IP, 9000) #HUGE
        print('Receiving ServerName')
        ServerName = receive(self.IP)
        ServerName = decryptF(self.PASSWORD, keySalt, ServerName)

        if ServerName == self.SERVERNAME:
            print('Server Id confirmed')
            print('Sending confirmation') ######
            send(self.IDCONFIRM, self.IP)
        else:
            print('ID cross fail')
            send(self.FAILLOGIN, self.IP)
            return False #DIFFERENT RETURN FOR SERVERNAMECHECK????

        print('Receiving Salt')
        salt = receive(self.IP, 9000) #HUGE
        
        print('Sending CheckID')
        garbleID = encryptF(self.PASSWORD, salt, self.MYNAME)
        send(garbleID, self.IP)

        print('Waiting for confirm')
        response = receive(self.IP)

        if response != self.IDCONFIRM:
            print('Failed to login') #####
            return False
        
        send(b'', self.IP)

        self.CURRENTSALT = RSAdecrypt(receive(self.IP), privKey)
            
        print('Logged in')
        return True

    def initConn(self):
        wait = True
        while wait:
            wait = not self.setup()
            time.sleep(.3)
        return self.SERVERNAME, self.IP

    def setupIPTargets(self):  #INPUT FROM FILE
        self.IP = False
        with open(self.FILENAME, 'r') as f: #FOR TESTS USING SAME FILE, SIMILAR BETWEEN SIDES
            for x in range(0, 1):
                self.IP = f.readline().rstrip()
        return (self.IP)

    def GetMyName(self): #INPUT FROM FILE
        name = False
        with open(self.MYFILENAME, 'r') as f:
            name = f.readline().rstrip().encode('utf-8')
        return name

    def IPTargetName(self): #INPUT FROM FILE
        Name = False
        with open(self.FILENAME, 'r') as f:
            for x in range(0, 2):
                Name = f.readline().rstrip().encode('utf-8') #limited name length at 17
        return (Name) 

    def IPTargetLogin(self): #INPUT FROM FILE
        Pass = False
        with open(self.FILENAME, 'r') as f:
            for x in range(0, 3):
                Pass = f.readline().rstrip().encode('utf-8') #unlimited pass length
        return (Pass)   

    def convo(self, message='ping'):
        message = message.encode('utf-8')
        msg = encryptF(self.PASSWORD, self.CURRENTSALT, message)
        send(msg, self.IP)
        saltK = receive(self.IP)
        self.CURRENTSALT = decryptF(self.PASSWORD, self.CURRENTSALT, saltK)
        return 0


    #####BEGIN ##NEEDS A SERVERID FILE AND MYNAME FILE



    def __init__(self, FILENAME, MYFILENAME):
        self.LOGINMESSAGE = b'Id accepted'
        self.IDCONFIRM = b'Id confirmed'
        self.FAILLOGIN = b'Id rejected'
        self.FILENAME = FILENAME #FROM EXTERNAL INPUT'
        self.MYFILENAME = MYFILENAME #FROM EXTERNAL INPUT
        self.CURRENTSALT = b'salty'
        self.IP = self.setupIPTargets() #INDEX is the line from the login file to read from
        self.MYNAME = self.GetMyName()
        self.SERVERNAME = self.IPTargetName()
        self.PASSWORD = self.IPTargetLogin()

        server, ip = self.initConn() 
        print(server, ip) #Write to file? WRITE THIS NAH

        time.sleep(1)
        print('pinging')
        ping = self.convo()
        print(ping)


