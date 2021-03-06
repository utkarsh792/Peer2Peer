import socket
import threading
import select
import time
import datetime

def main():

    class Chat_Server(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
                self.conn = None
                self.addr = None
            def run(self):
                HOST = ''
                PORT = 7001
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST,PORT))
                s.listen(4)
                self.conn, self.addr = s.accept()
                
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.conn],[self.conn],[])
                    for input_item in inputready:
                        
                        message = self.conn.recv(1024)
                        if message:
                            print "Utkarsh: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0

    class Chat_Client(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.host = None
                self.sock = None
                self.running = 1
            def run(self):
                PORT = 7000
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, PORT))
                
                while self.running == True:
                    inputready,outputready,exceptready \
                      = select.select ([self.sock],[self.sock],[])
                    for input_item in inputready:
                        
                        message = self.sock.recv(1024)
                        if message:
                            print "Utkarsh: " + message + ' (' + datetime.datetime.now().strftime('%H:%M:%S') + ')'
                        else:
                            break
                    time.sleep(0)
            def kill(self):
                self.running = 0

    class Text_Input(threading.Thread):
            def __init__(self):
                threading.Thread.__init__(self)
                self.running = 1
            def run(self):
                while self.running == True:
                  text = raw_input('')
                  try:
                      chat_client.sock.sendall(text)
                  except:
                      Exception
                  try:
                      chat_server.conn.sendall(text)
                  except:
                      Exception
                  time.sleep(0)
            def kill(self):
                self.running = 0

    

    ip_addr = raw_input('Type IP address or press enter: ')

    if ip_addr == '':
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_server.start()
        text_input = Text_Input()
        text_input.start()

    else:
        chat_server = Chat_Server()
        chat_client = Chat_Client()
        chat_client.host = ip_addr
        text_input = Text_Input()
        chat_client.start()
        text_input.start()

if __name__ == "__main__":
    main()
