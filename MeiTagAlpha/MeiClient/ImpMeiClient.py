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

import MeiClient
from MeiClient import MeiClient

tom = MeiClient('ServerID-MAC-001.txt', 'ClientName.txt') #opens secure connection with credential details
tom.convo() #pings the server specified in the credential files

msg ='damn'
tom.convo(msg) #sends a message to a server specifed in the credential files