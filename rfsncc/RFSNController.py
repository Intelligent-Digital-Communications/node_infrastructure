import sys, time
from socket import *

EXITCODE = '-1'
# IP addresses that the Ping server can be bound to
listeners = ["localhost", "rfsn-demo1.vip.gatech.edu", "rfsn-demo2.vip.gatech.edu",
            "rfsn-demo3.vip.gatech.edu"]
serverPort = 5035         # Port number that the Ping server is bound to
RECVTIMEOUT = 1           # Receive timeout time for TCP socket

def help():
    print("--------------------------RFSNController.py----------------------\n"
          "   - This application connects to the selected RFSN nodes,       \n"
          "         updates gains and schedules data captures.              \n"
          "-----------------------------------------------------------------\n")


def updategains(iplist, gain, path):
    message = '1,' + gain + ',' + path
    return sendmessages(iplist, message)

def generateepochs(iplist, filename, path):
    for x in iplist: # Be sure the file is already on all of the RFSNs
        send_csv_file(filename, x)
    message = '2,' + filename + ',' + path + ',headless'
    return sendmessages(iplist, message)

def get_input():
    try:
        if len(listeners) <= 1:
            print ("\n-----------------------------------------------------------------\n"
                   "                 No IP addresses have been added.                  \n"
                   "          Please add IP addresses and restart the program.         \n"
                   "-----------------------------------------------------------------  \n")
        print ("\nEnter a number to select a node:\n\n0. All")

        # Display node options
        for x in range(0, len(listeners)):
            print(str(x + 1) + ". " + listeners[x])
        node = raw_input("")[:1]

        option = raw_input("Enter a number to select an option\n "
                           "\n1. Update gain                     "
                           "\n2. Generate epochs               \n"
                           "\n3. Schedule epochs               \n")[:1]
        if option == '1':
            gain = -1
            gain = raw_input("Enter the new gain:    \n")[:3]
            while not gain.isdigit() or int(gain) < 0 or int(gain)  > 100:
                print ("\nInvalid gain, please enter a number between 0 and 100.\n")
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

        if option == '3':
            path = raw_input("Enter path of atqCmd.sh file (--path=...)")
            message = '3,' + path
            fileName = "NA"
        return path, node, option, message, fileName
    except EOFError:
        exit(1)

def setup_socket(serverName):
    # Get ip address of target from
    serverName = gethostbyname(serverName)
    try: # Create TCP client socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
    except Exception as e:
        print(e)
        print("Socket failed to be created.")
        return None
    try: # Open the TCP connection
        clientSocket.connect((serverName,serverPort))
    except Exception as e:
        print(e)
        print("Socket failed to connect.")
        return None
    clientSocket.settimeout(1)
    return clientSocket

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

def send_message(messageIn, ip):
    socketIn = setup_socket(ip)
    try:
        # Send the TCP packet with the message
        socketIn.sendall(messageIn)
    except Exception as e:
        print(e)
        print("Failed while sending message!")
    try: # Receive the server response
        message = recv_timeout(socketIn, RECVTIMEOUT)
    except Exception as e:
        print(e)
        print("Probably just timed out. Are you sure clients are running?")
    try:
        socketIn.close()
    except: #If doesn't close, didn't exist
        return "Failed to send message."
    return message

def send_messages(iplist, message):
    returning = ''
    for x in iplist:
        returning += send_message(message, x)
    return returning

def send_csv_file(fileNameIn, ip):
    try:
        socketIn = setup_socket(ip)
        if not fileNameIn.endswith(".csv"):
            fileNameIn = fileNameIn + ".csv"
        outFile = open(fileNameIn)
        fileString = outFile.read()
        received = send_message('99,' + fileNameIn + ',' + fileString, socketIn)
        outFile.close()
        socketIn.close()
        print received
    except:
        socketIn.close()
        print "Failed to send CSV file, please try again.\n"

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            help()
            exit(0)
    while True:
        try:
            path, node, option, message, fileName = get_input()
            if node == '0': # Selected all
                print send_messages(listeners, message)
            else: # Picked just one
                print send_message(message, listeners[int(node)-1])

        except KeyboardInterrupt:
            try:
                exit(0)
            except:
                exit(0)

if __name__ == "__main__":
    main()
