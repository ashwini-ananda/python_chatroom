import sys
import threading
from tkinter import *
from tkinter import simpledialog

import grpc
import argparse

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

class Client:
    def __init__(self, username: str, root=None, window=None, clients=None, outputs=None):
        self.username = username
        self.root=root
        self.window = window
        self.outputs = outputs
        # create gRPC channel and stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatServerStub(channel)
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        clients.append(self)
        self.__init_ui()
        self.window.mainloop()
    
    def __init_ui(self):
        self.chatHistory = Text(padx=10,pady=10,bg="black",fg="white",height=10)
        self.chatHistory.pack(side=TOP)
        # self.chat_list.pack(bg="black",fg="white")
        self.nameLabel = Label(self.window, text=self.username,bg="black",fg="white")
        self.nameLabel.pack(side=LEFT)
        self.chatMsg = Entry(self.window, bd=5,bg="#f6f6f6",fg="black")
        self.chatMsg.bind('<Return>', self.sendMessage)
        self.chatMsg.focus()
        self.chatMsg.pack(side=BOTTOM)

    def __listen_for_messages(self):
        # wait for new messages from the server and add to UI
        for note in self.conn.ChatStream(chat.Empty()):
            self.outputs.append("{}: {}".format(note.name, note.message))
            print("{}: {}".format(note.name, note.message))
            self.chatHistory.insert(END, "[{}] {}\n".format(note.name, note.message))

    def sendMessage(self, event):
        # get message from tkinter UI
        message = self.chatMsg.get()
        if message != '':
            n = chat.Note()
            n.name = self.username
            n.message = message
            print("{}: {}".format(n.name, n.message))
            self.conn.SendNote(n)
            self.chatMsg.delete(0,"end")

    def close():
        sys.exit()


def main(argv=None, clients=[], outputs=[]):
    parser = argparse.ArgumentParser()
    parser.add_argument('client_id')
    parser.add_argument('server_ip')
    parser.add_argument('port')
    parser.add_argument('username',nargs='?', default='')
    args = parser.parse_args(argv)
    
    global address 
    address = args.server_ip
    global port 
    port = args.port
    global clientID
    clientID = int(args.client_id)
    global testing
    testing = False
    root = Tk()
    root.configure(background='black')
    frame = Frame(root, width=200, height=100)
    frame.configure(background='black')
    frame.pack()
    root.withdraw()
    username = None
    if args.username != '':
        username = args.username
        testing = True
    while username is None:
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()
    c = Client(username, root, frame, clients, outputs)
    

def setGlobals(server_ip, port_number, client_id):
    global address 
    address = server_ip
    global port 
    port = port_number
    global clientID
    clientID = client_id

def sendMessage(c, message):
    n = chat.Note()
    n.name = c.username
    n.message = message
    c.conn.SendNote(n)

def destroy(c):
    c.root.destroy()

if __name__ == '__main__':
    main() 
