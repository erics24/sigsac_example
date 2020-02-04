#!/usr/bin/env python3

from socket import *
from datetime import datetime
import time, argparse

MAX_BYTES = 65535

### server function

def server(port):
    sock = socket(AF_INET, SOCK_DGRAM) #Create the datagram socket
    
    sock.bind(('127.0.0.1', port)) #bind the socket to the local loopback address and the respective port passed in from the command line
    print('Listening at {}'.format(sock.getsockname()))  ## Verifying the IP/port binding
    
    while True: ## why do we need this while loop?  Try removing it...
        #Cntl-break will exit from recvfrom
        data, address = sock.recvfrom(MAX_BYTES) # this function 'blocks', or prevents the code from continuing its execution until a datagram is received
        received_text = data.decode('ascii') #encode the string to ascii, utf-8 is default 
        print('The client at {} says {}'.format(address, received_text))
        
        sending_text = 'Your data was {} bytes long'.format(len(data)) #create message to return to client
        print("Sending to client:", sending_text)
        data = sending_text.encode('ascii')        
        sent = sock.sendto(data, address) ##sends response to same address on line 15
        print("Sent {} bytes back to the client, waiting for next datagram.".format(sent))

### client function

def client(port):
    sock = socket(AF_INET, SOCK_DGRAM)  ##create the client socket
    print('The OS assigned me the address {}'.format(sock.getsockname())) ## get the IP/port for the socket
    
    text = 'The time is {}'.format(datetime.now()) ##get the current time
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.0.1', port)) #send initiall message to server
    
    data, address = sock.recvfrom(MAX_BYTES)  # Danger! We will secure this later... Could someone sniff my local port number?
    text = data.decode('ascii')
    print('The server {} replied:\n {}'.format(address, text)) ## Got our response!
    

if __name__ == '__main__':
    choices = {'client': client, 'server': server} ##point each key to the function names above
    parser = argparse.ArgumentParser(description='Send and receive UDP locally') #generate the argument parser object
    parser.add_argument('role', choices=choices, help='which role to play') #add the role argument, requiring a choice of client or server
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)') #require the port role (keyword arg has default value)
    args = parser.parse_args() #parse the args upon execution
    function = choices[args.role] #assign the reference client or server to the variable function
    function(args.p) ##run the function given by the 'role' argument (client or server) with the port as the keyword argument


    ## >>> python3 udp_client_server.py server
    ## >>> python3 udp_client_server.py client
