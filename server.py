import threading
from socket import *
import time
import struct
import random

while 1: #so the program will run forever
    time.sleep(1)
    def UDP_thread():
        my_ip= gethostbyname(gethostname())
        print("Server started, listening on IP address " + my_ip)
        while 1:
            try:
                serverPort = 12000
                serverSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
                serverSocket.bind(('', serverPort))
                broadcast = struct.pack('!IBH',0xfeedbeef,0x2,serverPort) #broadcast with ip over udp 
                serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                for i in range (0, 10):
                    serverSocket.sendto(broadcast, ('172.1.0', 13117))
                    time.sleep(1)
                break
            except:  
                time.sleep(1) 
                pass
    try:
        global counter_group1 
        global counter_group2 
        global lock_1
        global lock_2

        counter_group1 = 0
        counter_group2 = 0
        lock_1 = threading.Lock()
        lock_2 = threading.Lock()

        def print_list(lst,d): #this func create string with all the groups name
            output=""
            for i in range(0,len(lst)):
                output+=(d[lst[i]]+"\n")
            return output

        def counter_for_group(conn,group_1,group_2):  #this func count the chars of every groups
            try:
                while 1:
                    time.sleep(0.0001)
                    if conn in group_1:
                        lock_1.acquire()
                        global counter_group1
                        counter_group1 += 1
                        lock_1.release()
                    elif conn in group_2:
                        lock_2.acquire()
                        global counter_group2
                        counter_group2 += 1
                        lock_2.release()  
            except:
                time.sleep(1) 
                pass

        def TCP_thread():
            my_ip= gethostbyname(gethostname())
            serverPort = 12000
            tcpServer = socket(AF_INET, SOCK_STREAM) 
            tcpServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
            tcpServer.bind((my_ip, serverPort)) 
            threads = [] 
            groups = {}
            list_conn = []
            ten_second = time.time() + 10
            tcpServer.settimeout(1)
            while(time.time() < ten_second):
                time.sleep(0.0001)
                tcpServer.listen(15) 
                try:
                    (conn, (ip,port)) = tcpServer.accept()
                    groups[conn] = conn.recv(1024).decode() #create dictionary that the key is the connection and the value is the group name
                    list_conn.append(conn)
                except:
                    time.sleep(1) 
                    pass
            
            if len(list_conn) == 0:
                massege_game_over = "No groups signed up"
                
            else:
                random.shuffle(list_conn) #random the division of the groups
                count_conn = len(list_conn)
                if count_conn > 1 : #split all the groups into 2 groups
                    group_2 = list_conn[0:int(count_conn/2)]
                    group_1 = list_conn[int(count_conn/2):count_conn]
                else:  # if there is just one group 
                    group_1 = list_conn
                    group_2 = []

                messege = "\nWelcome to Keyboard Spamming Battle Royale.\n\nGroup 1:\n==\n"+print_list(group_1,groups)+"\nGroup 2:\n==\n"+print_list(group_2,groups)+"\nStart pressing keys on your keyboard as fast as you can!!\n"
                for i in range(0,count_conn): #create thread for every connection and start the thread
                    list_conn[i].send(messege.encode())
                    thread_for_client = threading.Thread(target=counter_for_group, args=(list_conn[i], group_1, group_2))
                    threads.append(thread_for_client)
                    thread_for_client.start()
                
                time.sleep(10)
                #result of the game - winner / loser / tie
                ret = ""
                list_win = ""
                if counter_group1 == counter_group2:
                    ret = "Tie!"
                    list_win = print_list(group_1, groups)+ print_list(group_2,groups)
                elif counter_group1 > counter_group2:
                    ret = "Group 1 wins!"
                    list_win = print_list(group_1,groups)
                else:
                    ret = "Group 2 wins!"
                    list_win = print_list(group_2,groups)

                massege_game_over = "Game over!\nGroup 1 typed in "+str(counter_group1)+" characters. Group 2 typed in "+str(counter_group2)+" characters.\n"+ret+"\n\nCongratulations to the winners:\n==\n"+list_win
                for i in range(0,count_conn): #send message with the result of the game and then end the connection
                    list_conn[i].send(massege_game_over.encode())
                    try:
                        list_conn[i].close()
                    except:
                        pass

            print(massege_game_over)
        #create the threads and run them
        tcp_th = threading.Thread(target=TCP_thread, args=())           
        udp_th = threading.Thread(target=UDP_thread, args=())    
        tcp_th.start()
        udp_th.start()
        tcp_th.join()
        udp_th.join()
    except:
        time.sleep(1) 
        pass
    
