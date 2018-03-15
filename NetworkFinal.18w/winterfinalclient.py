''' This is a simple client that will send a timestamp to the server over tcp.

'''
import socket
import sys
import datetime
import time
import threading



def sendTime():

		# Create a TCP/IP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the socket to the port where the server is listening
		server_address = ('localhost', 10000)
		print >>sys.stderr, 'connecting to %s port %s' % server_address
		sock.connect(server_address)

		try:
		    
		    #make a timestamp

		    timestamp = time.time()

		    #Now make it pretty 

		    message = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
		    print >>sys.stderr, 'sending "%s"' % message
		    sock.sendall(message)

		    # Look for the response
		    amount_received = 0
		    amount_expected = len(message)
		    
		    while amount_received < amount_expected:
		        data = sock.recv(1024)
		        amount_received += len(data)
		        print >>sys.stderr, 'received "%s"' % data

		finally:
		    print >>sys.stderr, 'closing socket'
		    sock.close()

		'''
		When the entire message is sent and a copy received, 
		the socket is closed to free up the port.
		'''

sendTime()


