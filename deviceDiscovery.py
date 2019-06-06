import socket       #for socket programming
import re           #for regular expressions
import requests     #for  getting data from webpages
import lxml         #for operating on xml data

# message to be sent over http to request data from devices
msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'

# Set up UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

#set time for which we wait for device replies
s.settimeout(10)

# set broadcast ip address for upnp
ip = "239.255.255.250"

# set broadcast port for upnp
port = 1900

# broadcast the message as utf-8 format
s.sendto(msg.encode('utf-8'), (ip, port) )
f = open("address.txt", 'w')
i = 1
try:
    while True:
        #store received data in variables
        data, addr = s.recvfrom(65507)

        # isolate xml url from data received
        link = str(re.search("(?P<url>http?://[^\sr]+)", str(data)).group("url"))

        # remove backslash from url
        link = link[:-1]
        print(link)
        
        # get all data in xml file and store in variable
        x = requests.get(link)

        # write data to file
        with open("device" + str(i) + ".xml", 'wb') as k:
            k.write(x.content)
        f.write(str(link))
        f.write("\n\n")
        i += 1
except socket.timeout:
    # if timeout is reached, close the loop
    pass
f.close()




