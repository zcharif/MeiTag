import socket

def send(message, IP, BUFFER_SIZE=1024, PORT = 8676 output=False): #bytecode and string!
    TCP_IP = IP
    TCP_PORT = PORT #Apple code requires port number higher than 1000
    BUFFER_SIZE = BUFFER_SIZE
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Windows compliance
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1) #required for Apple compliance
        s.connect((TCP_IP,TCP_PORT))
        s.send(message)
        if output == True:
            print('Sent')
    except: #will only fail if socket wasn't made. WILL NOT FAIL IF MESSAGE IS NOT RECEIVED BY OTHER END
        if output == True:
            print('Failed to send')
        return False
    finally:
        s.close
    return True

def receive(IP="", BUFFER_SIZE=1024, PORT=8676 output = False):
    TCP_IP = IP
    TCP_PORT = PORT #Apple code requires port number higher than 1000
    BUFFER_SIZE = BUFFER_SIZE
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s = s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Windows compliance
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) #Apple compliance
    s.bind((TCP_IP,TCP_PORT))
    s.listen(1)
    try:
        if output == True:
            print('Waiting')
        c, addr = s.accept()
        data = c.recv(BUFFER_SIZE)
        if output != 0:
            print('Received')
        return data
    except: #will only fail if socket wasn't made. WILL NOT FAIL IF MESSAGE IS NOT RECEIVED BY OTHER END
        if output == True:
            print('Failed to receive')
        return 0
    finally:
        s.close()
