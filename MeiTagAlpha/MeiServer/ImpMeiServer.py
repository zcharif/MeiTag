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

import threading

##OK SOME FILE EDITOR HERE THAT BASICALLY WILL DO THE CRUDE WORK....?
##NAH LET'S GO FOR SUPER GHETTO

import MeiServer
from MeiServer import MeiServer

tom = MeiServer('SERVERID-MAC-001.txt', 'ClientID.txt') #opens a secure connection with credential details
tom.convo() #listens to the client specified in credential file

msg = tom.convo() #records the next message received from client specified
print(msg)


def worker(): #code for the thread created
    pass

threads = []
t = threading.Thread(target=worker) #creates a thread
threads.append(t) #adds to queue
t.start() #starts unstarted threads, must code every time a new thread is created

#Code below will run regardless of the threads above AWESOME!