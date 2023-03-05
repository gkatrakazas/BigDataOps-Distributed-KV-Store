import socket
import sys
import json

def search(string, keys_list):

    print(string,keys_list)
    string=string.replace(' ->',':').replace('[ ','{').replace(' ]','}').replace(' |',',')

    string='{'+string+'}'

    dict_obj = json.loads(string)

    print(dict_obj)

    value=dict_obj.copy()
    for k in keys_list:
        value = value[k]
    
    string=str(value).replace(':',' ->').replace('{','[ ').replace('}',' ]').replace(',',' |').replace("'",'"')
    
    return string

def checkforquoates(string):
    if not (string.startswith('"') and string.endswith('"')):
    # Add quotation marks
        string = '"'+string+'"'
    return string


class TrieNode:
    def __init__(self):
        self.children = {}
        self.value = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, value):
        node = self.root
        for ch in key:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.value = value

    def delete(self, key):
        key=checkforquoates(key)
        return self._delete(self.root, key, 0)

    def _delete(self, node, key, depth):
        if depth == len(key):
            # The key is present in the trie, so we can delete it
            if node.value is None:
                # The key is not present in the trie
                return False
            node.value = None
            return True
        ch = key[depth]
        child = node.children.get(ch)
        if child is None:
            # The key is not present in the trie
            return False
        if self._delete(child, key, depth + 1):
            # If the child node has no value and no children, we can delete it
            if child.value is None and not child.children:
                del node.children[ch]
            return True
        return False

    def find(self, key):

        key=checkforquoates(key)

        node = self.root
        for ch in key:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node.value
    
    def print_trie(self, node, key=""):
        if node.value is not None:
            print(key, node.value)
        for ch, child in node.children.items():
            self.print_trie(child, key + ch)

def Read_argument():

    print('Start server1 arguments')
    if len(sys.argv)!=5:
        print('ERROR: Something from arguments is missing!')
        return -1
    
    list_arg=sys.argv

    server_ip=''
    server_port=-1

    for index,value in enumerate(list_arg):
        #print(index,value)
        if value=='-a':
            server_ip=list_arg[index+1]
        elif value=='-p':
            server_port=list_arg[index+1]

    
    print('End reading arguments')
    return server_ip, int(server_port)


if __name__ == '__main__':  #python3 server1.py -a 127.0.0.1 -p 5001

    #read argument
    server_ip, server_port=Read_argument()

    #criete trie
    trie=Trie()
  
    # create a socket object
    s = socket.socket()

    # bind the socket to a port
    s.bind((server_ip, server_port))

    # become a server socket
    s.listen(5)
    clientsocket,addr = s.accept()
    print('Server: ',server_ip,', Start listening in port: ',server_port)

    Stored_data=True
    
    while True:
        # establish a connection
        #print(f"Got a connection from {addr}")

        # receive data from the client
        msg = clientsocket.recv(1024).decode()

        data = msg.split(" ", 1)
        if data[0]=='First':

            print(f"First connection from client")
            clientsocket.send(("OK CONNECTION: "+server_ip+" "+str(server_port)+"").encode())

        elif data[0]=="end":
            clientsocket.send("OK END".encode())
            #break

        elif data[0]=="PUT":
            
            data_parts=data[1].split("->", maxsplit=1)
            data_parts[0]=data_parts[0].replace(' ','')
            print(data_parts[0])

            try: 
              trie.insert(data_parts[0],data_parts[1])
              clientsocket.send('OK'.encode())
            except:
                print('ERROR PUT')
                clientsocket.send('ERROR'.encode())
                Stored_data=False
        
        elif data[0]=="CHECKPUT":
            print(data[0])
            if Stored_data==True:
                clientsocket.send('OK'.encode())
            else:
                clientsocket.send('ERROR'.encode())

        elif data[0]=="GET":
            
            #print(data)
            try: 
              res=trie.find(data[1])
              clientsocket.send(res.encode())
            except:
              clientsocket.send("NOT FOUND".encode())

        elif data[0]=="DELETE":
            
            print(data)

            if trie.delete(data[1]):
                clientsocket.send('OK'.encode())
            else:
                clientsocket.send("NOT FOUND".encode())

        
        elif data[0]=="QUERY":

            partofkeys=data[1].split('.')

            try: 
              res=trie.find(partofkeys[0])
              result = search('"'+partofkeys[0]+'" ->'+res,partofkeys)                
              clientsocket.send(result.encode())
            except:
              clientsocket.send("NOT FOUND".encode())



        # close the connection
        #clientsocket.close()
    s.close()

    
        
        