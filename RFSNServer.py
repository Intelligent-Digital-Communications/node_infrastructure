import sys, os, subprocess
from socket import *

serverPort = 5035
EXITCODE = '-1'

def help():
    print("\n--------------------------RFSNServer.py--------------------------\n"
          "         - This application connects to the RFSN Client,         \n"
          "            updates gains and schedules data captures.           \n"
          "-----------------------------------------------------------------\n")

def setup_socket():
    try:
        # Create a TCP socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # Assign IP address and port number to socket
        serverSocket.bind(('', serverPort))
        # Server begins listening for incoming TCP requests
        serverSocket.listen(1)
        # Reuse the socket in TIME_WAIT state without waiting for it to timeout
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return serverSocket
    except:
        print "Error setting up the socket\n"
        exit(1)

def process_message(connectionSocket):
    try:
        message = connectionSocket.recv(4096) # limited to 4096 bytes
        if not message or message == 'END':
            return EXITCODE
        if message[0] == '3':
            parsedMessage = message.split(',', 2)
        else:
            parsedMessage = message.split(',')
        # If no data is received or an 'END' message is received the while loop
        # breaks and the connection socket is colsed
        return parsedMessage
    except:
        return "Error receiving or processing message on the server side.\n"

def send_message(connectionSocket, message):
    try:
        connectionSocket.send(message) # Server response
    except:
        print "Send message failed.\n"

def update_gains(gainInfo):
    try:
        if not gainInfo[2].endswith("/"):
            path = gainInfo[2] + "/"
        else:
            path = gainInfo[2]
        if not os.path.exists(path):
            return "Invalid path to generate epochs."
    except:
        return "Invalid path to generate epochs."

    try:
        err = os.system("python update_gains.py " + "--gain=" + gainInfo[1] + " --path=" + path)
        if err == 0:
            message = "\nGain for " + str(gethostname()) + " updated!"
        else:
            message = "There was an error updating the gains. Please try again."

        return message
    except:
        return "Error updating gains on the server. Please try again."

def generate_epochs(epochsInfo):
    # inser / just in case the path is not in correct format
    try:
        if not epochsInfo[2].endswith("/"):
            path = epochsInfo[2] + "/"
        else:
            path = epochsInfo[2]
        if not os.path.exists(path):
            return "Invalid path to generate epochs."
    except:
        return "Invalid path to generate epochs."

    try:
        currentDirectory = os.getcwd()
        if not currentDirectory.endswith("/"):
            currentDirectory = currentDirectory + "/"
        currentDirectory = currentDirectory + "csv_files/"
        err = os.system("python generate_epochs.py " + currentDirectory + epochsInfo[1] + " " + path + epochsInfo[3])
        if err == 0:
            message = "\nEpochs generated for " + str(gethostname())
        else:
            message = "There was an error generating the epochs. Please try again."
        return message
    except:
        return "Error generating epochs. Please try again."

def close_serverSocket(serverSocket):
    try:
        serverSocket.close()
    except:
        pass

def close_connectionSocket(connectionSocket):
    try:
        connectionSocket.close()
    except:
        pass

def receive_file(fileStream):
    try:
        currentDirectory = os.getcwd()
        if not currentDirectory.endswith("/"):
            currentDirectory = currentDirectory + "/"
        if not os.path.exists(currentDirectory + "csv_files/"):
            os.makedirs(currentDirectory + "csv_files/")
        currentDirectory = currentDirectory + "csv_files/" + fileStream[1].strip()
        out_file = open(currentDirectory, 'w')
        out_file.write(fileStream[2])
        out_file.close()
        return "CSV file transfer complete."
    except:
        return 'Error writing CSV file to server.'

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help'
            help()
            exit(0)
    try:
        serverSocket = setup_socket()
        while 1:
            # server waits for incoming requests; new socket created on return
            connectionSocket, addr = serverSocket.accept()
            while 1:
                parsedMessage = process_message(connectionSocket)
                if parsedMessage == '-1':
                    break
                if parsedMessage[0] == '1':
                    message = update_gains(parsedMessage)
                elif parsedMessage[0] == '2':
                    message = generate_epochs(parsedMessage)
                elif parsedMessage[0] == '3':
                    message = receive_file(parsedMessage)

                send_message(connectionSocket, message)
                # close the TCP connection; the welcoming socket continues
            connectionSocket.close()
        # Close the welcoming socket connection
        serverSocket.close()

    except KeyboardInterrupt:   # If the user interrupts the program, print to indicate
        print("\nExited by user.\n")
        try:
            close_serverSocket(serverSocket)
            close_connectionSocket(connectionSocket)
        except:
            pass
        exit(0)

if __name__ == "__main__":
    main()
