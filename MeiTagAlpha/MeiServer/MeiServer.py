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

import time
from time import sleep

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import SymmetricCryptoTest
from SymmetricCryptoTest import encryptF, decryptF

#CHECK FOR MAC FIRST!
class MeiServer:
    def checkID(self, ClientID):
        with open(self.CLIENTFILENAME) as f:
            ClientIdMySide = 'sioht89e4jrfioeoihse984hf8iheap9w8fh98'
            read = '4598fjwjt98'
            toaster = ''
            while read != '':
                read = f.readline().rstrip()
                if self.IP == read:
                    if f.readline().rstrip() == str(self.BAN_IP_CODE):
                        print('Reset the IP codes, passwords, etc. for this device. Potentially hacked or password incorrect')
                        return False
                    toaster = f.readline().rstrip()
                    ClientIdMySide = toaster.encode('utf-8')
                pass
        if ClientID == ClientIdMySide:
            return True
        return False

    def CheckIP(self):
        with open(self.CLIENTFILENAME, 'r') as f:
            data = f.readlines()
            oData = data
            read = '98747+_)+)'
            i = 0
            while read != '':
                read = f.readline().rstrip()
                i = i + 1
                if read == self.IP:
                    read = f.readline().rstrip()
                    break
        if read == str(self.BAN_IP_CODE):
            return False
        return True

    def saltGen(self, byteSize=16):
        return os.urandom(byteSize)
        
    def setup(self): #returns a connection value
        keySet = keyGen() #has a tuple of the key, and the public key
        privKey=keySet[0]
        pubKey=keySet[1]
        
        print('Receiving ClientKey')
        clientKey = RSA.importKey(receive(self.IP))
        
        print('Sending PublicKey')
        send(pubKey.exportKey(), self.IP)
        
        print('Receiving ID')
        ClientID = RSAdecrypt(receive(self.IP), privKey)
        
        print('User', ClientID.decode('utf-8'), 'connected')

        if self.checkID(ClientID):
            print('Id accepted')
            print('Sending confirmation')
            send(self.LOGINMESSAGE, self.IP) 
            
        else:
            send(self.FAILLOGIN, self.IP)
            print('Id rejected')
            return False

        print('Receiving Salt')
        salt = receive(self.IP, 9000) #HUGE
        
        print('Sending server name')
        garbleID = encryptF(self.PASSWORD, salt, self.MYNAME)
        send(garbleID, self.IP)

        print('Waiting for confirm')
        response = receive(self.IP)
        ##print('response', response)
        ##print('ID CONFIRM FOR SERVER SENT?', IDCONFIRM)

        if response != self.IDCONFIRM:
            print('Failed to login')
            return False
            

        print('Sending salt')
        keySalt=self.saltGen()
        send(keySalt, self.IP, 9000) #HUGE
        print('Receiving CrossData')
        ClientCross = receive(self.IP)
        ClientCross = decryptF(self.PASSWORD, keySalt, ClientCross)

        if ClientID == ClientCross:
            print('Id confirmed')
            print('Sending confirmation')
            send(self.IDCONFIRM, self.IP)
            receive(self.IP)
        else:
            print('ID cross fail')
            send(self.FAILLOGIN, self.IP)
            receive(self.IP)
            return False

        self.CURRENTSALT = self.saltGen()
        send(RSAencrypt(self.CURRENTSALT, clientKey), self.IP)
        
        return True
            
    def initConn(self):
        failCount = 0
        wait = True
        while wait:
            print('Login Attempt:',failCount +1)
            wait = not self.setup()
            failCount = failCount + 1
            if failCount > self.MAXFAIL:
                return self.BAN_IP_CODE, self.IP
        return self.LOGIN_IP_CODE, self.IP

    def setupIPTargets(self):  #INPUT FROM FILE
        ip = False
        with open(self.FILENAME, 'r') as f: #FOR TESTS USING SAME FILE, SIMILAR BETWEEN SIDES
            for x in range(0, 1 + self.INDEX * 2):
                ip = f.readline().rstrip()
        return (ip)

    def GetMyName(self): #INPUT FROM FILE
        name = False
        with open(self.FILENAME, 'r') as f:
            name = f.readline().rstrip().encode('utf-8')
            name = f.readline().rstrip().encode('utf-8')
        return name

    def IPTargetLogin(self): #INPUT FROM FILE
        Pass = False
        with open(self.FILENAME, 'r') as f:
            for x in range(0, 3 + self.INDEX * 2):
                Pass = f.readline().rstrip().encode('utf-8') #unlimited pass length
        return (Pass)   

    def convo(self):
        msg = b''
        msg = receive(self.IP)
        msg = decryptF(self.PASSWORD, self.CURRENTSALT, msg)
        saltK = self.saltGen()
        send(encryptF(self.PASSWORD, self.CURRENTSALT, saltK), self.IP)
        self.CURRENTSALT = saltK
        return msg.decode('utf-8')


    #######BEGIN  ###NEEDS A SERVERID FILE, A CLIENTLIST, AND A MYNAME FILE
    #SUDO PIP3 INSTALL PYCRYPTO

    def __init__(self, FILENAME, CLIENTFILENAME):
        self.INDEX = 0
        self.LOGINMESSAGE = b'Id accepted'
        self.IDCONFIRM = b'Id confirmed'
        self.FAILLOGIN = b'Id rejected'
        self.MAXFAIL = 10
        self.BAN_IP_CODE = 8976
        self.LOGIN_IP_CODE = 9999
        self.LOGOUT_IP_CODE = 5978
        self.CRITSENDERROR = b'9th4589ugvjhwpu8g8gser78hfguhefgo8rehsuger8ougheo84uih'
        self.FILENAME = FILENAME #INPUT FROM OUTSIDE PROGRAM!
        self.CLIENTFILENAME = CLIENTFILENAME #INPUT FROM OUTSIDE PROGRAM!
        self.CURRENTSALT = b'salty'

        self.IP = False
        self.MYNAME = False
        self.PASSWORD = False

        print('Retrieving credentials')

        while self.IP == False or self.MYNAME == False or self.PASSWORD == False:
            try:
                self.IP = self.setupIPTargets()
                self.MYNAME = self.GetMyName()
                self.PASSWORD = self.IPTargetLogin()
               # print(self.IP, self.MYNAME, self.PASSWORD)
            except:
                print('Cannot access credentials. Are they properly installed?')
                sleep(2)
            pass

        status, ip = self.initConn()
        #print(status, ip) #Write to master login file WRRIIITEE

        try:
            with open(self.CLIENTFILENAME, 'r') as f:
                data = f.readlines()
                oData = data
                read = '98747+_)+)'
                i = 0
                while read != '':
                    read = f.readline().rstrip()
                    i = i + 1
                    if read == self.IP:
                        break
            data[i] = str(status) + '\n'
            with open(self.CLIENTFILENAME, 'w') as f:
                f.writelines(data)
            print('Saved login data')
        except:
           print("Failed to save login data")
           try:
                with open(self.CLIENTFILENAME, 'w') as f:
                    f.writelines(oData)
           except:
              print('Backup deleted')

        print('Receiving ping from', self.IP)

        convoRET = self.convo()
        print(convoRET)
