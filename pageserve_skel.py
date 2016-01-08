"""
Socket programming in Python
  as an illustration of the basic mechanisms of a web server.

  Based largely on https://docs.python.org/3.4/howto/sockets.html
  This trivial implementation is not robust:  We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible. 
"""


import socket    # Basic TCP/IP communication on the internet
import random    # To pick a port at random, giving us some chance to pick a port not in use
import _thread   # Response computation runs concurrently with main program 


def listen(portnum):
    """
    Create and listen to a server socket.
    Args:
       portnum: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """
    # Internet, streaming socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to port and make accessible from anywhere that has our IP address
    serversocket.bind(('', portnum))
    serversocket.listen(1)    # A real server would have multiple listeners
    return serversocket

def serve(sock, func):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        print("Attempting to accept a connection on {}".format(sock))
        (clientsocket, address) = sock.accept() #listening for request to come in. creates a socket and creates an address (of client) 
        _thread.start_new_thread(func, (clientsocket,)) #web page of cat


CAT = """
     ^ ^
   =(   )=
   """


def respond(sock):
    """
    Respond (only) to GET

    """
    sent = 0
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    print("\nRequest was {}\n".format(request))#debugging code. run this code to see what the request looked like. like foo.html, look for this and send the file. 

    parts = request.split()
    if len(parts) > 1 and parts[0] == "GET":
        address_unedit = parts[1]
        if "~" in address_unedit or "//" in address_unedit or ".." in address_unedit: #checks for illegal characters in  url for security
            transmit("HTTP/1.0 403 Forbidden\n\n", sock) #tells computer there is a error
            transmit("403 Forbidden\n\n",sock) #forbidden error
        elif address_unedit.endswith(".html") or address_unedit.endswith(".css"): #makes sure html or css files
            try:
                htmlcss_file = address_unedit[1:]
                file = open(htmlcss_file,'r')
                line_list =[] #list of strings to be complied into something sendable
                for line in file:
                    line_list.append(line)
                final_string = " ".join(line_list)#create one big string to send over transmit
                transmit("HTTP/1.0 200 OK\n\n", sock)
                transmit(final_string,sock)
            except IOError:
                transmit("HTTP/1.0 404 Not Found\n\n", sock)#tells computer there is a error
                transmit("404 Not Found\n\n",sock)
    
        else:
            transmit("HTTP/1.0 403 Forbidden\n\n", sock) #forbidden error
            transmit("403 Forbidden\n\n",sock)
            
        
    else:
        transmit("HTTP/1.0 400 Bad Request\n\n", sock)#tells computer there is a error
        transmit("404 Not Found\n\n",sock)
    sock.close()

    return

def transmit(msg, sock):
    """It might take several sends to get the whole buffer out"""
    sent = 0
    while sent < len(msg):
        buff = bytes( msg[sent: ], encoding="utf-8")
        sent += sock.send( buff )
    

def main():
    port = random.randint(5000,8000)
    sock = listen(port)
    print("Listening on port {}".format(port))
    print("Socket is {}".format(sock))
    serve(sock, respond)
    
main()
    
