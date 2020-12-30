from socket import *
import struct
import time
import getch
import threading


while 1:
    print("Client started, listening for offer requests...")
    client = socket(AF_INET, SOCK_DGRAM) # UDP
    client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    client.bind(("", 13117))
    data, addr = client.recvfrom(2048)
    server_port = struct.unpack('I B H', data)[2]
    print( "Received offer from " +  addr[0] + " attempting to connect...")


    #host = addr[0] 
    port = server_port
    BUFFER_SIZE = 2000 

    host = "127.0.1.1"       #TODO check

    team_name = "the_best_group"
    tcpClient = socket(AF_INET, SOCK_STREAM) 
    tcpClient.connect((host, port))
    tcpClient.send(team_name.encode())

    def press_keys(socket_tcp):
        try:
            while 1: 
                socket_tcp.send(getch.getch().encode())
        except:
            pass

    data = tcpClient.recv(1024)
    print(data)

    game_th = threading.Thread(target=press_keys, args=(tcpClient,))

    game_th.start()
    game_th.join()

    print("server disconnected, listening for offer request...")

    # time.sleep(10)
    # if game_th.is_alive():
    #     game_th._tstate_lock()  
    #     game_th._stop()


    # def run(): 
    #     while True: 
    #         # print('thread running') 
    #         global stop_threads 
    #         if stop_threads: 
    #             break
    
    # stop_threads = False
    # t1 = threading.Thread(target = run) 
    # t1.start() 
    # time.sleep(1) 
    # stop_threads = True
    # t1.join() 
    # print('thread killed') 


