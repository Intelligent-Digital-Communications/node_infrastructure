import os, time
from socket import *

serverPort = 5035
EXITCODE = '-1'

def help():
    print("--------------------------RFSNClient.py--------------------------\n"
          "         - This application connects to the RFSN Client,         \n"
          "            updates gains and schedules data captures.           \n"
          "-----------------------------------------------------------------\n")

def setup_socket():
    try:
        # Create a TCP socket
        serverSocket = socket(AF_INET, SOCK_STREAM)
        # Assign IP address and port number to socket
        serverSocket.bind(('', serverPort))
        # server begins listening for incoming TCP requests
        serverSocket.listen(1)
        # Reuse the socket in TIME_WAIT state without waiting for it to timeout
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return serverSocket
    except:
        print "Error setting up the socket\n"
        exit(1)

def process_message(connectionSocket):
    try:
        message = connectionSocket.recv(1024) # limited to 1024 bytes
        if not message or message == 'END':
            return EXITCODE
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
        os.chdir(gainInfo[2])
    except:
        return "Invalid directory.\n"

    try:
        err = os.system("python update_gains.py " + "--gain=" + gainInfo[1])
        if err == 0:
            message = "\nGain for " + str(gethostname()) + " updated!\n"
        else:
            message = "There was an error updating the gains. Please try again.\n"

        return message
    except:
        return "Error updating gains on the server. Please try again.\n"

def generate_epochs(epochsInfo):
    # inser / just in case the path is not in correct format
    try:
        if not epochsInfo[2].endswith("/"):
            path = epochsInfo[2] + "/"
        else:
            path = epochsInfo[2]

        os.chdir(path)
    except:
        return "Invalid path to generate epochs.\n"

    try:
        err = os.system("python generate_epochs.py " + epochsInfo[1] + ".csv " + path + epochsInfo[3])
        if err == 0:
            message = "\nEpochs generated for " + str(gethostname()) + "\n"
        else:
            message = "There was an error generating the epochs. Please try again.\n"
        os.system("cp /opt/IDC_scripts/update_gains.py " + path + epochsInfo[3] + "/update_gains.py")

        return message
    except:
        return "Error generating epochs. Please try again.\n"

def keyboardInterrupt_exit(connectionSocket, serverSocket):
    try:
        connectionSocket.close()
    except:
        pass
    try:
        serverSocket.close()
    except:
        pass
    exit(0)

def main():
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

                send_message(connectionSocket, message)
                # close the TCP connection; the welcoming socket continues
            connectionSocket.close()
        # Close the welcoming socket connection
        serverSocket.close()

    except KeyboardInterrupt:   # If the user interrupts the program, print to indicate
        print("Exited by user.\n")
        keyboardInterrupt_exit(connectionSocket, serverSocket)


if __name__ == "__main__":
    main()