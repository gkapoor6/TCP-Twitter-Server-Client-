""" 
Authors: Geetika Kapoor, Ruiyang Qin 
Code Referrences: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/, 
                  https://pymotw.com/2/socket/tcp.html,
                  https://www.geeksforgeeks.org/python-check-two-lists-least-one-element-common/
"""

import socket
import sys
import thread


# IDEA: Server stores a dictionary of (username, LIST OF hashtags the user has subscribed to) - dict1
# When a user tweets, server uses dict1 to find all usernames subscribed to the used hastag.
# Then it sends the tweet to all users - maybe the tweet message begins with a keyword so the client knows that it is 
# receiving a tweet rather than a response to another query.
# Timeline = the client will output all tweets that have been sent to it by the server since the 
#               last time the user has run the ‘timeline’ command. 
# timeline feature mus tbe handled by the client. The server would have already sent it messages.

## Dictionary will be shared between threads and will acquire locks to write.
dict1 =  {}
dict1_lock = threading.Lock()

# thread fuction to handle multiple clients
def threaded(connection): 
    try:
        while True:
            
            data = connection.recv(300)
            if data:
                # split to get the command
                command = data.split()[0]
                username = data.split()[1]

                # initial username command
                if command == "username":
                    # acquire lock for dictionary
                    dict1_lock.acquire()
                    dict1[username] = []
                    dict1_lock.release()

                # for tweet
                elif command == "tweet":
                    # find tweet
                    start_tweet = data.find("\"")
                    end_tweet = data.find("\"", start_tweet + 1)
                    tweet = data[(start_tweet + 1) : end_tweet]
                    # find hashtags
                    start_hash = data.find("#")
                    hashtags = data[start_hash + 1:]
                    hashtags_list = hashtags.split("#")
                    hashtags_set = set(hashtags_list)
                    # find users that have subscribed to each of the hastags in the hashtags_list
                    # send a message to each user
                    dict1_lock.acquire() # for reading shared object

                    # When a user tweets, server uses dict1 to find all usernames subscribed to the used hastag.
                    # Then it sends the tweet to all users - maybe the tweet message begins with a keyword so the client knows that it is 
                    # receiving a tweet rather than a response to another query.
                    for u in dict1:
                        # check if two lists (list of subscribed hastags and list of hashtags in tweet) have common hashtag
                        if (set(dict1[u]) & hashtags_set) or ("ALL" in dict1[u]):
                            # <client_username> <sender_username>: <tweet_message> <origin_hashtag>
                            connection.sendall(username + " " + u + ": " + tweet + data[start_hash:])
                            
                    dict1_lock.release()    

                    # connection.sendall(messageHolder) # I don't think the server needs to resend the message to the client
                                                        # so I am commenting this functionality from both server and client.
                                                        # for the "tweet" command, server doesn't reply with anything (from the google drive)
                                                        # - Geetika
                elif command == "timeline":
                    # NEED TO CHANGE CODE BELOW
                    print
                    # messageLength = len(messageHolder)
                    # connection.sendall(str(messageLength))
                    # ack = connection.recv(150)
                    # if ack == 'received':
                    #     connection.sendall(messageHolder)

            else:
                # if data = null
                break
    finally:
        connection.close()


  
def server():   
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_addr = ("127.0.0.1", int(sys.argv[1]))
    sock.bind(server_addr)
    print("Socket binded to port: ", port)

    # Listen for upto 5 incoming connections
    sock.listen(5)
    print("Socket is listening\n") 

    while True:
        print 'waiting for a connection...'

        connection, client_address = sock.accept()
        print('Connected to: ', client_address)

        # Start a new thread and return its identifier
        start_new_thread(threaded, (connection,))


if __name__ == '__main__': 
    server()