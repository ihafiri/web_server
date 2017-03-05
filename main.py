import ConfigParser
import sys
import socket
import utils
import threading


if __name__ =="__main__":
    config = ConfigParser.ConfigParser()
    config.read(sys.argv[1])

    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (config.get('SRVCONF' , 'ListenIP') ,
    int(config.get('SRVCONF' , 'ListenPORT')))
    sock.bind(server_address)
    sock.listen(5)
    while True:
        connection , cAddr = sock.accept()
        data = connection.recv(2048)
        #utils.RequestHandler(connection , data , config).serve()
        #connection.close()
        client_thread=threading.Thread(target=utils.multi_threading_wrapper,
        args=(connection,data,config,))
        client_thread.start()
