import sys
import random
import socket
import math
from math import *
import re
def is_server_up(s,server, port):
    try:
        s.connect((server, port))
        return 'UP'
    except Exception as e:
        return 'DOWN'


def get_list_of_servers(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    list_of_keys=[]
    for line in Lines:
        list_of_keys.append((line.split()))
    
    return list_of_keys

def get_list_of_data(filename):
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    list_of_strings=[]
    for line in Lines:
        list_of_strings.append((line))
    
    return list_of_strings

def Read_argument():

    print('Start reading arguments')
    if len(sys.argv)!=7:
        print('ERROR: Something from arguments is missing!')
        return -1
    
    list_arg=sys.argv

    server_file=''
    data=''
    number_servers=-1

    for index,value in enumerate(list_arg):
        #print(index,value)
        if value=='-s':
            server_file=list_arg[index+1]
        elif value=='-i':
            data=list_arg[index+1]
        elif value=='-k':
            number_servers=list_arg[index+1]

    
    print('End reading arguments')
    return server_file, data, int(number_servers)

# python3 kvClient.py -s serverFile.txt -i dataToIndex.txt -k 2

if __name__ == "__main__":

    #read argument
    server_file, data_filename, number_servers_to_index=Read_argument() 

    #get list with server info
    list_of_servers=get_list_of_servers(server_file) 

    #get data to list of strings
    data_to_index=get_list_of_data(data_filename)

    # list of sockets for every server
    sockets = []  

    is_ok_server=True
    # for loop to check connect with all servers
    for ip,port in list_of_servers:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((ip, int(port)))
            print(port)
            sockets.append(s)
            print('Server: ',ip,':',port,' IS UP!')
        except:
            print('Server: ',ip,':',port,' IS DOWN!')
            is_ok_server=False

    # check if all servers is UP
    if is_ok_server==True:
        print('All Servers is UP')
    else:
        print('ERROR: One or more Servers is down!')
        exit (-1)


    #PART 1 - send data to index in servers ###################### 
    print("Start send data to index in Servers")
    for line in data_to_index:

        # get random k servers to send the record line
        index_socket=[]
        for i in range(len(sockets)):
            index_socket.append(i)
        random_socket = random.sample(index_socket, number_servers_to_index)

        for i in range(len(sockets)):

            # get random k servers to send the record line
            if i not in random_socket: continue
            
            sockets[i].send(("PUT "+line).encode())
            data = sockets[i].recv(1024).decode()
            #print(f"Received data from: {data}")

    print("End send data to index in Servers")
    for i in range(len(sockets)):

        sockets[i].send(("CHECKPUT").encode())
        data = sockets[i].recv(1024).decode()
        print('Index Data: ',data)

    
    #PART 2 - Start questions to servers ######################
    while True:
        user_input = input("Enter Question: ")
        part_user_input = user_input.split(" ", 1)
        #Check how many server is UP
        number_server_up=0
        socketsup=[]
        index=0
        for ip,port in list_of_servers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                s.connect((ip, int(port)))
                socketsup.append(index)
                number_server_up+=1
            except:
                number_server_up+=0
            index+=1
        
        if number_server_up==0:
                print('All server are down')
                break
        elif number_server_up<number_servers_to_index:
            print('WARNING: All server are=',len(sockets)-number_servers_to_index+1,' or more servers are down and therefore it cannot guarantee the correct output')
        
        if part_user_input[0]=='GET':
            result=[]
            for i in range(len(sockets)):
                if i not in socketsup: continue
                sockets[i].send((user_input).encode())
                data = sockets[i].recv(1024).decode()
                result.append(data)

            result = list(set(result))
            if len(result)>1: result.remove('NOT FOUND')
            print(f"Received Answer: {part_user_input[1]} -> {result[0]}")
        
        elif part_user_input[0]=='DELETE':
            result=[]
            for i in range(len(sockets)):
                if i not in socketsup: continue
                try:
                    sockets[i].send((user_input).encode())
                    data = sockets[i].recv(1024).decode()
                    result.append(data)
                except:
                    result.append('NOT FOUND')

            result = list(set(result))
            if len(result)>1: result.remove('NOT FOUND')
            print(f"Received Answer: {part_user_input[1]} -> {result[0]}")

        elif part_user_input[0]=='QUERY':
            result=[]
            for i in range(len(sockets)):
                if i not in socketsup: continue

                sockets[i].send((user_input).encode())
                data = sockets[i].recv(1024).decode()
                result.append(data)

            result = list(set(result))
            if len(result)>1: result.remove('NOT FOUND')
            print(f"Received Answer: {part_user_input[1]} -> {result[0]}")
        
        elif part_user_input[0]=='COMPUTE':

            part_user_input2 = user_input.split(" ")
            expression=part_user_input2[1] 
            modified_expression = re.sub(r"log\(([^)]+)\)", r"log(\1,10)", expression)
            #print('FUNCTION: ',modified_expression)

            if part_user_input2[2]!='WHERE': 
                print('COMPUTE format is wrong. Try again!')
                continue

            queries=' '.join(part_user_input2[3:]).split(' AND ')
            
            queries = [q.split(' = ') for q in queries]
            #print(queries)

            flag=0
            for var,que in queries:
                result=[]
                for i in range(len(sockets)):
                    if i not in socketsup: continue

                    sockets[i].send((que).encode())
                    data = sockets[i].recv(1024).decode()
                    result.append(data)

                result = list(set(result))
                #print('--',result)
                if 'NOT FOUND' in result: 
                    result.remove('NOT FOUND')

                if result==[]:
                    flag=1
                    print ('ERROR: ',var,' = ',que,' NOT FOUND')
                    break
                elif result[0].isnumeric()==False:
                    flag=2
                    print ('ERROR: ',var,' = ',que,' is STRING, can not compute')
                    break
                modified_expression=modified_expression.replace(var,result[0])
            
            if flag!=0:
                continue


            eval_res=eval(modified_expression)
            print(f"Received Answer: {eval_res}")
        else:
            print('Wrong format of question! Try again')
           




        