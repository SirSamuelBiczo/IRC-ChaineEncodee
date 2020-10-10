#coding: utf-8

import socket
import time 
import re
import base64

HOST = "irc.root-me.org"
PORT = 6667

def regex_find_pattern(regex, string):
    return re.findall(regex, string)

def irc_initialize_connection(socket, nickname):
    data = "USER guest 0 * :guest\r\n"
    data = data.encode("utf-8")
    socket.sendall(data)

    data = "NICK {}\r\n".format(nickname)
    data = data.encode("utf-8")
    socket.sendall(data)

def irc_join_channel(socket, channel):
    data = "JOIN {}\r\n".format(channel)
    data = data.encode("utf-8")
    socket.sendall(data)
    time.sleep(1)
def irc_send_message_channel(socket, channel, msg):
    data = "PRIVMSG {} :{}...\r\n".format(channel, msg)
    data = data.encode("utf-8")
    socket.sendall(data)
    time.sleep(1)
def irc_send_private_message(socket, name, msg):
    data = "PRIVMSG {} {}...\r\n".format(name, msg)
    data = data.encode("utf-8")
    socket.sendall(data)

    time.sleep(1)

def irc_disconnect(socket):
    time.sleep(4)
    data = "QUIT\r\n"
    data = data.encode("utf-8")
    socket.sendall(data)

def irc_read_buffer(socket, buffsize):
    data = socket.recv(buffsize)
    data = data.decode("utf-8")
    return data 

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((HOST, PORT))
except ConnectionRefusedError:
    print("Connexion refusé !")
except:
    print("Impossible de se connecter")
else:
    print("Vous êtes connecter...")
    
    irc_initialize_connection(socket, "BOT_SamuelBiczoPy")
    irc_join_channel(socket, "#root-me_challenge")

    print(irc_read_buffer(socket, 2**13))
    irc_send_private_message(socket, "candy", "!ep2\r\n")

    data = irc_read_buffer(socket, 2**8)
    print(data)

    #####################CHALLENGE####################### 
    encode = regex_find_pattern("BOT_SamuelBiczoPy :(.+)", data)[0]
    
    decode = base64.b64decode(encode).decode("utf-8")
    print("Encoded : {} Decode {} : ".format(encode, decode))
 
    ###################################################### 

    irc_send_private_message(socket, "candy", "!ep2 -rep {}\r\n".format(decode))
    
    print(irc_read_buffer(socket, 2**8))
    irc_disconnect(socket)
     
finally:
    print("Fermeture de la connexion...")
    socket.close()