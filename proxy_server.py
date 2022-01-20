#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing  import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def handle_echo(addr, conn, client_socket):
    print(f'connected by {addr}')

    #send data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f'sending received data {send_full_data} to google')
    client_socket.sendall(send_full_data)

    #shutdown socket
    client_socket.shutdown(socket.SHUT_WR)

    data = client_socket.recv(BUFFER_SIZE)
    print(f'sending received data {data} to client')

    #send data back
    conn.send(data)


def main():
    host = 'www.google.com'
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #reuse address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        print('Starting proxy server')
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket: 
                print("connecting to google...")
                remote_ip = get_remote_ip(host)

                #connect client_socket
                client_socket.connect((remote_ip, port))

                #TODO Question 6
                p = Process(target=handle_echo, args=(addr, conn, client_socket))
                p.daemon = True
                p.start()
                print(f'started process {p}')



            conn.close()

if __name__ == "__main__":
    main()
