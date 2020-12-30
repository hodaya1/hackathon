from socket import *
import struct
import time
import getch
import threading


while 1:

    print("Client started, listening for offer requests...")
    while 1:
        try:     
            client = socket(AF_INET, SOCK_DGRAM) # UDP
            client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            client.bind(("", 13117))
            data, addr = client.recvfrom(2048)
            client.close()
            (cookie, mytype, port) = struct.unpack('!IBH', data)
            if cookie!=0xfeedbeef or mytype!=2:
                raise Exception
            break
        except:
            pass    
    print( "Received offer from " +  addr[0] + " attempting to connect...")

    try:
        host = addr[0]
        #BUFFER_SIZE = 2000 

        #host = "172.1.0.41"       #TODO check
        #port = 12000

        team_name = "shem_mekori"
        tcpClient = socket(AF_INET, SOCK_STREAM) 
        tcpClient.connect((host, port))
        tcpClient.send(team_name.encode())

        global run_
        run_ = True
        def press_keys(socket_tcp):
            try:
                ten_seconds = time.time() + 10
                while time.time()<ten_seconds: 
                    ch = getch.getch().encode()
                    if run_:
                        socket_tcp.send(ch)
            except:
                pass

        data = tcpClient.recv(1024)
        print(data.decode())

        game_th = threading.Thread(target=press_keys, args=(tcpClient,))

        game_th.start()
        
        try:
            game_over = tcpClient.recv(1024)
            run_ = False
            game_th.join()
            print(game_over.decode())
        except:
            run_ = False
            game_th.join()

        print("server disconnected, listening for offer request...")
    except:
        pass
