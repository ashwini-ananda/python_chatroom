# python_chatroom
GRPC Chatroom with python using async RPC


I have implemented the group chat using Python and gRPC library. The system implements a bidirectional gRPC streaming where the type of calls is response-stream type. 

gRPC uses the CompletionQueue API for asynchronous operations. The completion queue is bound to an RPC call. To use an asynchronous client to call a remote method, we first create a channel and stub. Once we have a stub running, initiate the RPC. The server implementation requests an RPC call with a tag and then waits for the completion queue to return the tag.

There is a gRPC specific service that will provide a service to use that has the given RPC calls implemented. Each client opens a new connection and waits for the server to send messages. The server is open and can keep sending messages. The server can handle incoming messages from clients so as to broadcast this message to all the other people in the chatroom. Multiple clients/users can communicate with each other in the chatroom via multi-threading. Each user is runs on a separate thread as the main/UI thread.

I have used Tkinter, a standard Python interface to the Tk GUI toolkit. This gives out the chat UI. First the user enters their name. Then the Tkinter chat UI pops up. Thereafter, all “unread” messages are downloaded, and the user can join the conversation as well. 

To run the project, in the app’s directory, first install all necessary packages in the requirements document.

`pip install reqs.txt`


Once all the dependencies are successfully installed, one can run the server and client(s).

`python chat_server.py 1,2,3 50001`

`python client.py 1 localhost 50001` 


This equips the chatroom up to a maximum of 3 clients who can successfully communicate with each other.
