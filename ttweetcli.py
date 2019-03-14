"""	
Authors: Geetika Kapoor, Ruiyang Qin 
Code Referrences: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/, 
				  https://pymotw.com/2/socket/tcp.html
"""

import socket
import sys

ServerIP = '0.0.0.0'
ServerPort = '8080'
message = ''
BUFFER_SIZE = 4096



def client():

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	ServerIP = str(sys.argv[1])
	ServerPort = int(sys.argv[2])
	server_address = (ServerIP, ServerPort)
	username = str(sys.argv[3])
	sock.connect(server_address)

	# check if username alphanumeric
	if (username.isalnum() == 0):
		print "Error: Username should be alphanumeric."
		exit(0)

	else: 
		# send username to server to check if valid
		message = "username " + username
		sock.sendall(message.encode())
		amount_received = 0
		messageLength = 0
		# get the length of the message
		while messageLength == 0:
			messageLength = sock.recv(150)
			if messageLength == 0:
				break
		amount_expected = int(messageLength)

		# send ack to server for message length
		received = 'received'
		sock.sendall(received.encode())
		if amount_received == amount_expected and amount_received == 0:
			print 'EMPTY MESSSAGE'
			exit(0)
		else:
			# receive actual data from server
			msg_from_server = ""
			while amount_received < amount_expected:
				data = sock.recv(150)
				amount_received += len(data)
				msg_from_server += data	
			print msg_from_server
			# check if username valid
			if msg_from_server != (username + ", connection established."):
				print username + ", connection failed since username occupied"
				exit(0)
			else:
				while True: # break using exit
					# valid username, can continue with standard I/O
				    inp = input()
					# split to get the command
	                command = inp.split()[0]
	                if command == "exit":
	                	##### EXIT #####
	                    print "bye bye"
	                    exit(0)
	                elif command == "tweet":
	                	##### TWEET #####

	                	# find message
						start_tweet = inp.find("\"")
						end_tweet = inp.find("\"", start_tweet + 1)
						tweet = inp[(start_tweet + 1) : end_tweet]
						# check if message length <= 150
						if len(tweet) > 150:
							print "message format illegal"			    	
		    			else:
		    				# find hashtag
		    				start_hash = inp.find("#")
		    				hastags = inp[start_hash + 1:]
		    				hashtags_list = hashtags.split("#")
		    				# Question: DO WE NEED TO CHECK IF EACH HASHTAG IS ALPHANUMERIC?
				    		# send tweet to server
				    		sock.sendall(inp.encode())

							# I don't think the server needs to resend the message to the client
							# so I am commenting this functionality from both server and client - Geetika
							# For the "tweet" command, server doesn't reply with anything (from the google drive)
							# amount_received = 0
							# amount_expected = len(message)
							# while amount_received < amount_expected:
							# 	data = sock.recv(150)
							# 	amount_received += len(data)
							# if data == message:
							# 	print 'Upload Successful'
							# else:
							# 	print 'Socket received wrong message, please Upload again'
			        elif command == "subscribe":
			        	print ""
		        	elif command == "unsubscribe":
		        		print ""
	        		elif command == "timeline":
	        			print ""
	        		else:
	        			break


if __name__ == '__main__': 
    client()
