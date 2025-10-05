#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Socket lets program talk over the network
Can send and receive mesages between computers
This virtual switch program uses sockets to send and receive UDP packets

sys can read command line arguments, stop the program, print errors etc.
Used to read port numbers from command line arguments. 
Ports: number that tells a computer which program a message is meant for. 
So, IP address tells which computer, port number tells which program on that computer.
"""
import socket 
import sys

"""
sys.argv: is a list of words after typing "python3". For example, if i type "python3 vswitch.py 8080" then sys.argv = ["vswitch.py", "8080"]. 
So, the following if statement checks if i typed exactly 2 words after "python3". And stops the program with sys.exit(1).
The print statement tells the user how to use the program correctly.
"""

# parse parameters
server_port = None
if len(sys.argv) != 2:
    print(f"Usage: python3 vswitch.py {VSWITCH_PORT}")
    sys.exit(1)
else:
    server_port = int(sys.argv[1]) # sets server_port to the port number in the command line argument

"""
server_address is a tuple and can't be altered. 
0.0.0.0 means listen on all IP on your machine. 
It tells the program to accept messages sent to any of the computer's IP addresses. "I'm the VSwitch. I will listen for UDP messages on port 8080, no matter which IP they come through."
""" 
server_address = ("0.0.0.0", server_port) 




# 0. create a UDP socket, bind to service port
"""
Creating a socket for the program to use for sending and receiving data. ".socket()" constructor method creates a new socket object (from socket class in socket module).
".socket(family, type)" takes two arguments:
- family: what kind of address (e.g., IPv4 or IPv6)
- type: what kind of connection (e.g., TCP or UDP)

both are constants:
socket.AF_INET: means "use IPv4 addresses" (like 127.0.0.1 or 10.1.1.101)
socket.SOCK_DGRAM: means "use UDP (User Datagram Protocol),” which sends small packets fast without checking if they arrived.
"""
vserver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # vserver_socket is now a UDP socket object.
vserver_socket.bind(server_address)
print(f"VSwitch Started at {server_address[0]}:{server_address[1]}")


