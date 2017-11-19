
import socket
import threading
import select
import time
import datetime

def main():

    completedClients = list()

    class Chat_Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None

            def run(self):
                HOST = ''
                PORT = 5000
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(10)
                self.conn, self.addr = s.accept()

                
                while self.running == True:
                    f = open(inputFile, 'rb')
                    if self.addr not in completedClients:
                        toSend = f.read(1024)
                        while toSend:
                            self.conn.send(toSend)
                            toSend = f.read(1024)

                        f.close()
                        completedClients.append(self.conn)
                        print('Upload Successful to ', self.addr)
                        break

            def kill(self):
                self.running = 0

    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1

            def run(self):
                PORT = 5001
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                
                while self.running == True:
                    f=open("recvFile","wb")
                    recvFile=self.sock.recv(1024)
                    while(recvFile):
                        f.write(recvFile)
                        recvFile=self.sock.recv(1024)

                    f.close()
                    break

            def kill(self):
                self.running = 0


    

    ip_addr = raw_input('Type IP address or type upload: ')

    if ip_addr == 'upload':
        inputFile = raw_input('Enter path of the file to upload: ')
        chat_server = Chat_Server()
       # chat_client = Chat_Client()
        chat_server.start()

    else:
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_client.host = ip_addr
        chat_client.start()

if __name__ == "__main__":
    main()


