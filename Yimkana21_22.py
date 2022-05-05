#!/usr/bin/python3
#Andrés González Varela, DNI 45144778X

import socket
import hashlib
import sys
import struct
import array
import base64
import requests
import threading
import queue

def obtenerIdentificador(msg): 
    identificador = msg.split(':')
    identificador = identificador[1].split('\n')
    identificador = identificador[0]
    return identificador

def reto0():
    sock = socket.socket()
    sock.connect(("rick", 2000))
    msg = sock.recv(1024)
    print(msg.decode())
    sock.sendall("unruffled_meitner".encode())
    msg, server = sock.recvfrom(1024)
    print(msg.decode())
    return msg.decode()

def UDP(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 40000))
    identificador = obtenerIdentificador(msg)
    respuesta = "40000 " + identificador
    sock.sendto(respuesta.encode(), ("rick", 4000))
    msg, server = sock.recvfrom(1024)
    sock.sendto(identificador.upper().encode(), server)
    
    msg, server = sock.recvfrom(1024)
    print(msg.decode())
    return msg.decode()

def WordCounter(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('rick', 3002))
    identificador = obtenerIdentificador(msg)
    cadena = ''
    received = False
    
    while received == False:
        numberOfWords = 0
        cadena += sock.recv(2048).decode()
        cadenaSpliteada = cadena.split()
        
        for i in range(len(cadenaSpliteada)):
            numberOfWords = numberOfWords + 1
            if len(cadenaSpliteada) - i >= 2:
                if (cadenaSpliteada[i+1]=="that's" and cadenaSpliteada[i+2]=="the" and cadenaSpliteada[i+3]=="end"):
                    received = True
                    break
            
    resultado = identificador + " " + str(numberOfWords)
    sock.send(resultado.encode())
    
    msg = b''
    while(True):
        aux = sock.recv(2048)
        if len(aux) <= 0:
            break
        msg += aux
    print(msg.decode())
    return msg.decode()
    
def reverseWords(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('rick', 6500))
    identificador = obtenerIdentificador(msg)
    received = False
    received2 = False
    cadena = ''
    cadenafinal=''
    listaInversa = ''
    palindrome=''
    
    
    while received == False:
        cadena = sock.recv(2048).decode()
        cadenafinal = cadenafinal+cadena
        cadenaSpliteada = cadenafinal.split(" ")
        for i in range(len(cadenaSpliteada)):
            if cadenaSpliteada[i] == "".join(reversed(cadenaSpliteada[i])) and len(cadenaSpliteada[i]) >=3:
                palindrome = cadenaSpliteada[i]
                received = True
                break
    
    cadenafinalSpliteada = cadenafinal.split(" ")

    while received2 == False:
        for i in range(len(cadenafinalSpliteada)):
            if cadenafinalSpliteada[i] == palindrome:
                received2=True
                break
            else:
                if cadenafinalSpliteada[i].isdigit():
                    listaInversa = listaInversa + " " + str(cadenafinalSpliteada[i])
                else:
                    listaInversa = listaInversa + " " + str("".join(reversed(cadenafinalSpliteada[i]))) 
                
    resultado = identificador + " " + listaInversa + " " + "--"
    sock.send(resultado.encode())
    
    msg = b'' 
    while(True):
        aux = sock.recv(2048)
        if len(aux) <= 0:
            break
        msg += aux
    print(msg.decode())
    return msg.decode()
        
def md5(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('rick', 9000))
    identificador = obtenerIdentificador(msg)
    sock.send(identificador.encode())
    
    read = False
    cMsg = b''
    msg = b''
    quantityBytes=b''
    toReceive = 1000
    
    while read==False: 
        msg = sock.recv(1)
        if (msg == b':'):
            read = True
            break
        quantityBytes=b''.join([quantityBytes,msg])
    
    print(quantityBytes)
    quantityBytes = quantityBytes.decode('ascii')
    count = int(quantityBytes)
   
    read = False
    while read == False: 
        msg = sock.recv(toReceive)
        count -= len(msg)
        cMsg = b''.join([cMsg, msg])
        if (count <= len(msg)):
            msg=sock.recv(count)
            cMsg = b''.join([cMsg, msg])
            read = True
            break
        
    md5 = hashlib.md5(cMsg)
    md5 = md5.digest()
    sock.send(md5)
    
    msg = b''
    while(True):
        aux = sock.recv(2048)
        if len(aux) <= 0:
            break
        msg += aux
    print(msg.decode())
    return msg.decode()        

def YAP(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',6691))
    identificador = obtenerIdentificador(msg)
    payload = base64.b64encode(identificador.encode())
    YAP = b'YAP'
    tipo = 0
    codigo = 0
    checksum = 0
    header =struct.pack(f'!3shBHh',YAP,tipo,codigo,checksum,1)
    msg = header + payload
    checksum= cksum(msg)
    header = struct.pack(f'!3shBHh', YAP, tipo, codigo, checksum, 1)
    msg = header + payload
    sock.sendto(msg,('rick',6001))
    info = sock.recv(4096)[10:]
    info = base64.b64decode(info)
    print(info.decode())
    sock.close()


        
# David Villa Alises: Author
def cksum(pkt):
    # type: (bytes) -> int
    if len(pkt) % 2 == 1:
        pkt += b'\0'
    s = sum(array.array('H', pkt))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    s = ~s
    if sys.byteorder == 'little':
        s = ((s >> 8) & 0xff) | s << 8
    return s & 0xffff
  
msg = reto0()
msg = UDP(msg)
msg = WordCounter(msg)
msg = reverseWords(msg)
msg = md5(msg)
msg = YAP(msg)
#msg = WebServer(msg)