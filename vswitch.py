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



"""
.recvfrom() method waits for a UDP packet (Ethernet frame wrapped in UDP) to arrive. 
input parameters: maximum size of Ethernet frame in bytes. In my case 1518 bytes. The largest chunk of data to expect. 

output: 
data: contains the actual bytes of the UDP packet that was received.
vport or sender address: a tuple (IP, port) of the VPort (client) that sent it. example: ('192.168.1.5', 40000).

UDP: method of sending data. 
Ethernet frame is the actual data in bytes. For example b'\xff\xff\xff\xff\xff\xff\x11\x11\x11\x11\x11\x11\x08\x00HelloWorld...'

ethernet headers are 14 bytes long. 
so, we are grabbing those 14 and extracting the Destination MAC (Bytes 0-5), Source MAC (Bytes 6-11), and EtherType (Bytes 12-13).


Example: ethernet_header[06:12] = b'\x11\x22\x33\x44\x55\x66'. each \x means a byte written in hexadecimal.
So, a loop (x for x in eth_header[6:12]) would return x = 0x11, x = 0x22,x = 0x33, x = 0x44, x = 0x55, x = 0x66.
"{:02x}".format(x)": This converts each byte (x) to a two-digit hexadecimal lowercase string. 
Example: "{:02x}".format(255) = FF.
join() takes this list of strings anf combines them using ":" as a separator.


"""
mac_table = {} # MAC addresses and their port numbers

while True: # keep looping forever, listen for data all the time.
    # 1. read ethernet from VPort
    data, vport_sender_address = vserver_socket.recvfrom(1518)

    # 2. parsing ethernet header
    ethernet_header = data[:14] 
    ethernet_destination = ":".join("{:02x}".format(x) for x in ethernet_header[0:6]) 
    ethernet_source = ":".join("{:02x}".format(x) for x in ethernet_header[6:12])
    print(f"[VSwitch] vport_sender_address<{vport_sender_address}>" f" src<{ethernet_source}> dst<{ethernet_destination}> datasz<{len(data)}>")


    # 3. insert or update MAC table:
    if ethernet_source not in mac_table or mac_table[ethernet_source] != vport_sender_address:
        mac_table[ethernet_source] = vport_sender_address
        print(f"[VSwitch] MAC Table Updated: {mac_table}")

    """
    Switch checks who the frame is for in the if statement.
    If the destination MAC address is in the MAC table, it sends the frame to that address.

    Else if the destination MAC address is the broadcast address (ff:ff:ff:ff:ff:ff), it sends the frame to all ports except the source port.
    broadcast_destination_ports gets all the MAC addresses in the MAC table except the source MAC address
    """
    # 4. forward ethernet frame
    # if destination is in mac table, forward ethernet frame to it
    if ethernet_destination in mac_table:
        vserver_socket.sendto(data, mac_table[ethernet_destination])
    elif ethernet_destination == "ff:ff:ff:ff:ff:ff": # broadcast address
        broadcast_destination_macs = list(mac_table.keys())
        broadcast_destination_macs.remove(ethernet_source)
        broadcast_destination_ports = {mac_table[mac] for mac in broadcast_destination_macs}
        print(f"[VSwitch] Broadcasting {broadcast_destination_ports}")

        for broadcast_destination in broadcast_destination_ports:
            vserver_socket.sendto(data, broadcast_destination) # broadcasts data to each port in the broadcast list except the source port
    else:
        print(f"Ethernet Frame Discarded")


    