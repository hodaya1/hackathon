from socket import *
import struct
import time
import getch
import threading


while 1:
    try:
        print("Client started, listening for offer requests...")
        client = socket(AF_INET, SOCK_DGRAM) # UDP
        client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        client.bind(("", 13117))
        data, addr = client.recvfrom(2048)
        server_port = struct.unpack('I B H', data)[2]
        print( "Received offer from " +  addr[0] + " attempting to connect...")


        #host = addr[0] 
        #port = server_port
        BUFFER_SIZE = 2000 

        host = "172.1.0.89"       #TODO check
        port = 12000

        team_name = "the_best_group"
        tcpClient = socket(AF_INET, SOCK_STREAM) 
        tcpClient.connect((host, port))
        tcpClient.send(team_name.encode())

        global run_
        run_ = True
        def press_keys(socket_tcp):
            try:
                while 1: 
                    ch = getch.getch().encode()
                    if run_:
                        socket_tcp.send(ch)
            except:
                pass

        data = tcpClient.recv(1024)
        print(data)

        game_th = threading.Thread(target=press_keys, args=(tcpClient,))

        game_th.start()
        
        try:
            game_over = tcpClient.recv(1024)
            run_ = False
            game_th.join()
            print(game_over)
        except:
            run_ = False
            game_th.join()

        print("server disconnected, listening for offer request...")
    except:
        pass





