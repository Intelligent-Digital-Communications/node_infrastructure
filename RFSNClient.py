import sys, time
from socket import *

EXITCODE = '-1'
# IP addresses that the Ping server can be bound to
# DO NOT DELETE THE "0" AT THE END OF THE serverIP LIST!!!!!!!!!!!!!!!!!!!!!!!!!
serverIP = ("rfsn-demo1.vip.gatech.edu", "rfsn-demo2.vip.gatech.edu",
            "rfsn-demo3.vip.gatech.edu", "0")
serverPort = 5035         # Port number that the Ping server is bound to
RECVTIMEOUT = 1           # Receive timeout time for TCP socket

def help():
    print("--------------------------RFSNClient.py--------------------------\n"
          "   - This application connects to the selected RFSN nodes,       \n"
          "         updates gains and schedules data captures.              \n"
          "-----------------------------------------------------------------\n")

def getservers():
    return serverIP

def updategains(iplist, gain, path):
    message = '1,' + gain + ',' + path
    return sendmessages(iplist, message)

def generateepochs(iplist, filename, path):
    message = '2,' + filename + ',' + path + ',headless'
    return sendmessages(iplist, message)

def get_input():
    try:
        if len(serverIP) <= 1:
            print ("\n-----------------------------------------------------------------\n"
                   "                 No IP addresses have been added.                  \n"
                   "          Please add IP addresses and restart the program.         \n"
                   "-----------------------------------------------------------------  \n")
        print ("\nEnter a number to select a node: \n\n"
               "0. All                               ")

        # Display node options depending on how many IP addresses there are
        for x in range(1, len(serverIP)):
            print( repr(x) + ". RFSN" + repr(x) )
        node = raw_input("")[:1]

        option = raw_input("Enter a number to select an option\n "
                           "\n1. Update gain                     "
                           "\n2. Generate epochs               \n")[:1]
        if option == '1':
            gain = -1
            gain = raw_input("Enter the new gain:    \n")[:3]
            while not gain.isdigit() or int(gain) < 0 or int(gain)  > 100:
                print "\nInvalid gain, please enter a number between 0 and 100.\n"
                gain = raw_input("Enter the new gain:    \n")[:3]
            message = '1,' + gain
            path = raw_input("Enter full path to modify gain for:\n")
            message = message + "," + path
            fileName = "NA"

        if option == '2':
            fileName = raw_input("Enter the CSV file name:  \n")
            if not fileName.endswith(".csv"):
                fileName = fileName + ".csv"
            message = '2,' + fileName
            path = raw_input("Enter path to generate epochs to:\n")
            message = message + "," + path
            #message = message + "," + raw_input("Enter the name of the game (unused):\n")
            message = message + ",old_feature"
            print "\n"

        return path, node, option, message, fileName
    except EOFError:
        exit(1)

def setup_socket(serverName):
    try:
        # Get ip address of target from
        serverName = gethostbyname(serverName)
        # Create TCP client socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Open the TCP connection
        clientSocket.connect((serverName,serverPort))
        # Set socket timeout as 1 second
        clientSocket.settimeout(1)
        return clientSocket
    except:
        return "Request timed out.\n"

def recv_timeout(socketIn,timeout=2):
    # Make socket non blocking
    socketIn.setblocking(0)

    # Total data partwise in an array
    final_data = [];
    data = '';

    # Beginning time
    begin = time.time()
    while True:
        # If you got some data, then break after timeout
        if final_data and time.time() - begin > timeout:
            break
        # If you got no data at all, wait a little longer, twice the timeout
        elif time.time() - begin > timeout*2:
            break
        # Receive something
        try:
            data = socketIn.recv(4096)
            if data:
                final_data.append(data)
                # Change the beginning time for measurement
                begin = time.time()
            else:
                # Sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    # Join all parts to make final string
    return ''.join(final_data)

def send_message(messageIn, socketIn):
    try:
        # Send the TCP packet with the message
        socketIn.sendall(messageIn)
        # Receive the server response
        message = recv_timeout(socketIn, RECVTIMEOUT)
        return message
    except:
        return "Error sending message, please try again.\n"

def send_messages(iplist, message):
    returning = ''
    for x in iplist:
        socket = setup_socket(x)
        returning += send_message(message, socket)
        socket.close()
    return returning

def send_csv_file(fileNameIn, socketIn):
    try:
        if not fileNameIn.endswith(".csv"):
            fileNameIn = fileNameIn + ".csv"
        outFile = open(fileNameIn)
        fileString = outFile.read()
        received = send_message('3,' + fileNameIn + ',' + fileString, socketIn)
        outFile.close()
        print received
    except:
        print "Failed to send CSV file, please try again.\n"

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            help()
            exit(0)
    while True:
        try:
            path, node, option, message, fileName = get_input()
            if node == '0':
                server = serverIP[:(len(serverIP)-1)] 
            else:
                server = serverIP[int(node)-1], '0'

            for x in server:
                if x == '0': break
                socket = setup_socket(x)
                if option == '2':
                    send_csv_file(fileName, socket)
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
