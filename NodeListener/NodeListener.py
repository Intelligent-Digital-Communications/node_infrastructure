import sys, os, subprocess, time, datetime, logging, pickle, hug
from socket import *
from schedule_recordings import schedule_recordings, Recording
serverPort = 5035
EXITCODE = '-1'
RECVTIMEOUT = 1           # Receive timeout time for TCP socket
LOG_FILENAME = "nodelistener.log"

def help():
    print("\n--------------------------NodeListener.py--------------------------\n"
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
        logging.info("Error setting up the socket\n")
        exit(1)

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

def process_message(connectionSocket):
    try:
        message = recv_timeout(connectionSocket, RECVTIMEOUT)
        print('proc_mes mess: ' + message)
        if not message or message == 'END':
            return EXITCODE
        if message.startswith('99'):
            parsedMessage = message.split(',', 2)
            print('parsed: ' + str(parsedMessage))
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
        logging.info("Send message failed.\n")

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

@hug.post('/generate_epochs')
def generate_epochs(body):
    recs = []
    for x in body:
        y = Recording()
        y.__dict__ = x
        recs.append(y)
    schedule_recordings(recs)

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
    logging.info('Filestream: ' + str(fileStream))
    #logging.info('CSV? ' + str(fileStream[2:]))
    try:
        csvdir = os.getcwd() + '/csv_files/'
        if not os.path.exists(csvdir):
            os.makedirs(csvdir)
        csvpath = csvdir + fileStream[1].strip()
        logging.info('csvpath: ' + csvpath)
        out_file = open(csvpath, 'w')
        out_file.write(fileStream[2])
        out_file.close()
        return "CSV file transfer complete."
    except:
        return 'Error writing CSV file to listener.'

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'help':
            help()
            exit(0)
    try:
        serverSocket = setup_socket()
    except:
        logging.info("Error setting up socket with server.")
    try:
        while 1:
            # server waits for incoming requests; new socket created on return
            connectionSocket, addr = serverSocket.accept()
            while 1:
                parsedMessage = process_message(connectionSocket)
                print('parsed in main: ' + str(parsedMessage))
                if parsedMessage == '-1':
                    break
                if parsedMessage[0] == '1':
                    message = update_gains(parsedMessage)
                elif parsedMessage[0] == '2':
                    message = generate_epochs(parsedMessage)
                elif parsedMessage[0] == '3':
                    logging.info("DEPRECATED!")
                    message = schedule_epochs(parsedMessage[1])
                elif parsedMessage[0] == '99':
                    message = receive_file(parsedMessage)

                send_message(connectionSocket, message)
                # close the TCP connection; the welcoming socket continues
            connectionSocket.close()
        # Close the welcoming socket connection
        serverSocket.close()

    except KeyboardInterrupt:   # If the user interrupts the program, log to indicate
        serverSocket.close()
        logging.info("\nExited by user.\n")
        try:
            close_serverSocket(serverSocket)
            close_connectionSocket(connectionSocket)
        except:
            pass
        exit(0)

def setup_logger():
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    logging.info(datetime.datetime.now())

if __name__ == "__main__":
    setup_logger()
    main()
