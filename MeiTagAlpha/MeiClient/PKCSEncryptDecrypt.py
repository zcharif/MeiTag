import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

def keyGen(byteSize=1024): #must match size of message, computational time exponentially tied to bytesize
    random_generator = Random.new().read
    key = RSA.generate(byteSize, random_generator) #generate pub and priv key
    publicKey = key.publickey() # pub key export for exchange. Only is able to encrypt
    return (key,publicKey) #key is the private key, with decryption capacity
    
def RSAencrypt(message, publicKey): #must be byte code and an RSA object
    cipher = PKCS1_OAEP.new(publicKey)
    ciphertext = cipher.encrypt(message)
    #message to encrypt is in the above line 'encrypt this message'
    return (ciphertext)

def RSAdecrypt(message, privateKey): #must be bytecode and an RSA object
    cipher = PKCS1_OAEP.new(privateKey)
    decrypted = cipher.decrypt(message)
    return decrypted
