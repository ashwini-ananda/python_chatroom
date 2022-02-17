from concurrent import futures

import grpc
import time
import sys
import argparse

import proto.chat_pb2 as chat
import proto.chat_pb2_grpc as rpc

from concurrent.futures import ThreadPoolExecutor
# from chat_protobufs.chatroom_pb2_grpc import add_ChatServicer_to_server
# from chat_protobufs.grpc_servicer import InfoService

cservice = None

class ChatServer(rpc.ChatServerServicer):

    def __init__(self):
        self.chats = []
        # self._grpc_service = InfoService()

    # send new messages to clients
    def ChatStream(self, request_iterator, context):
        lastindex = 0
        # join_user = 0
        # left_user =0
        # while True:
        #     while len(self._grpc_service.connected_users) > join_user:
        #         print(f"[CHAT SERVER]: Connected user {self._grpc_service.connected_users[join_user]}")
        #         join_user += 1
        
        # while True:
        #     while len(self._grpc_service.disconnected_users) > last_user:
        #         logging.info(f"[CHAT SERVER]: Disconnected user: {self._grpc_service.disconnected_users[last_user]}")
        #         last_user += 1
        
        # infinite loop for every client
        while True:
            # if len(self._grpc_service.connected_users) > join_user:
            #     print(f"[CHAT SERVER]: Connected user {self._grpc_service.connected_users[join_user]}")
            #     join_user += 1
            
            # if len(self._grpc_service.disconnected_users) > left_user:
            #     print(f"[CHAT SERVER]: Disconnected user: {self._grpc_service.disconnected_users[left_user]}")
            #     left_user += 1
            # check for new msgs
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                yield n

    def SendNote(self, request: chat.Note, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        return chat.Empty()

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('clients')
    parser.add_argument('port')
    parser.add_argument('testing',nargs='?', default='0')
    args = parser.parse_args(argv)
    if args.clients == '' or args.port == '':
        print("Expecting: server.py [client IDs] [port]")
        exit()
    # read client IDs, convert list to array of int
    l = []
    for part in args.clients.split(","):
        if part.strip():
            l.append(int(part.strip()))
    
    print(f'{l}')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=len(l)))  # create gRPC server
    cservice = ChatServer()
    rpc.add_ChatServerServicer_to_server(cservice, server)  # register server to gRPC
    print('...STARTING SERVER...')
    server.add_insecure_port('[::]:' + str(args.port))
    server.start()
    print('...SERVER RUNNING...')
    while True:
        time.sleep(64 * 64 * 100)

if __name__ == '__main__':
    # port = 50001
    main()    
