import sys, time, subprocess, pickle
from socket import *

EXITCODE = 1
# IP addresses that the Ping server can be bound to
serverIP = "143.215.249.9", "143.215.249.7", "143.215.249.14"
serverPort = 5035         # Port number that the Ping server is bound to

def help():
    print("--------------------------RFSNClient.py--------------------------\n"
          "   - This application connects to the selected RFSN nodes,       \n"
          "         updates gains and schedules data captures.              \n"
          "-----------------------------------------------------------------\n")

def get_input():
    try:
        print ("\nEnter a number to select a node: \n\n"
               "0. All                               ")

        # Display node options depending on how many IP addresses there are
        for x in range(1, len(serverIP)+1):
            print( repr(x) + ". RFSN" + repr(x) )
        node = raw_input("")[:1]

        option = raw_input("Enter a number to select an option\n "
                           "\n1. Update gain                     "
                           "\n2. Generate epochs               \n")[:1]
        if option == '1':
            message = '1,' + raw_input("Enter the new gain:    \n")[:3]
            message = message + "," + raw_input("Enter full path to modify gain for:\n")

        if option == '2':
            fileName = raw_input("Enter the CSV file name:  \n")
            message = '2,' + fileName
            path = raw_input("Enter full path to generate epochs:\n")
            message = message + "," + path
            message = message + "," + raw_input("Enter the name of the game:\n")
            print "\n"

        return path, node, option, message, fileName
    except EOFError:
        exit(1)

def setup_socket(serverName):
    try:
        # Create TCP client socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Open the TCP connection
        clientSocket.connect((serverName,serverPort))
        # Set socket timeout as 1 second
        clientSocket.settimeout(1)
        return clientSocket
    except:
        return "Request timed out.\n"

def send_message(messageIn, socketIn):
    try:
        # Send the TCP packet with the message
        socketIn.send(messageIn)
        # Receive the server response
        # Limited to 4096 bytes because that is the maximum set on the server side
        message = socketIn.recv(4096)
        return message
    except:
        return "Error sending message, please try again.\n"


def main():
    while True:
        try:
            path, node, option, message, fileName = get_input()
            #if node == '0'
            #    server = serverIP
            #else
            #    server = serverIP[int(node)-1]

            if node == '0':
                for x in serverIP:
                    socket = setup_socket(x)
                    if option == '2':
                        if not fileName.endswith(".csv"):
                            fileName = fileName + ".csv"
                        outFile = open(fileName)
                        fileString = outFile.read()
                        received = send_message('3,' + fileName + ',' + fileString, socket)
                        outFile.close()
                        print received
                    received = send_message(message, socket)
                    print received
                    socket.close()
            else:
                socket = setup_socket(serverIP[int(node)-1])
                if option == '2':
                        if not fileName.endswith(".csv"):
                            fileName = fileName + ".csv"
                        outFile = open(fileName)
                        fileString = outFile.read()
                        received = send_message('3,' + fileName + ',' + fileString, socket)
                        outFile.close()
                        print received
                received = send_message(message, socket)
                print received
                socket.close()
        except KeyboardInterrupt:
            try:
                socket.close()
                exit(0)
            except:
                exit(0)

if __name__ == "__main__":
    main()
