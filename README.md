# Big-Data-Management-Project

==== Data Creation ====

python3 genData.py -k keyFile.txt -n 100 -d 3 -l 4 -m 5

Initially, the max level of the  nested string we take as an argument is the max (pairs key -> value), except for the high key
Also, if  max_number_of_keys greater than the length  of the keyfile  is given.txt then the  max_number_of_keys then becomes equal to the  length of  the keyfile.txt  
As far as the dataset is concerned,  the implementation is done by recursion (def generate_nested_string).

=========================

==== Key Value Store ====

python3 kvClient.py -s serverFile.txt -i dataToIndex.txt -k 2
python3 server1.py -a 127.0.0.1 -p 5001
python3 server2.py -a 127.0.0.1 -p 5002
python3 server3.py -a 127.0.0.1 -p 5003

All functions have been implemented.
Initially, on the client side, conection is made  with  all the servers with sockets and if it does not connect to someone it terminates.
After connecting, it sends random to a k server each record, and after it finishes it asks the servers if they had any error when saving the records.
(This check on the server side is  done with  a Boolean variable, where it becomes false if  a record is not successfully inserted.
Storage is done in trie based only on the high key.
After each user's question, before the client sends  the question checks if we have at least k server UP, if not it terminates.
Each server recognizes what type of question it is as the message includes GET, QUERY , etc.
a) GET key: sends the query to everyone on  the servers and it then they call the trie. find where the value returns.
If it does not exist, it returns NOT FOUND
b) DELETE key: sends the query to all servers, and each deleted trie. delete
c) QUERY keypath: we send the entire keypath to all  servers, where each server splits  the first key  -> value running the trie.   find  to find value 
and then calls search where the input gets all  the keys and the original value. and return the value we are looking for if he finds it. 
Search turns  the keypath into a dictionary to  make it easier to search and returns it to the format it was originally.
d) COMPUTE f(x) WHERE x = QUERY key1. key2...: Initially  the client splits  all  queries  and sends them to all servers. After getting the answers then the function is calculated.
In the dataset the keys and values are with "". While in the questions it is without!
Example Execution:
$ python3 genData. py -k keyFile. txt -n 100 -d 3 -l 4 -m 5
100 records file was created  , which also exists in the repository
$ python3 server1.py -a 127.0.0.1 -p 5001
$ python3 server2.py -a 127.0.0.1 -p 5002
$ python3 server3.py -a 127.0.0.1 -p 5003
$ python3 kvClient.py -s serverFile.txt -i dataToIndex.txt -k 2
Start reading arguments
End reading arguments
Server: 127.0.0.1 : 5001 IS UP!
Server: 127.0.0.1 : 5002 IS UP!
Server: 127.0.0.1 : 5003 IS UP!
All Servers is UP
Start send data to index in Servers
End send data to index in Servers
Index Data: OK
Index Data: OK
Index Data: OK
Enter Question: GET key1
Received Answer: key1 -> [ "level" -> [ "height" -> 80.38 | "name" -> "oq" | " level" -> 26 ] | "height" -> [ "name" -> "uk" | " age" -> 18 | "level" -> 89 | "height" -> 10.56 | "street" -> "fo" ] | " age" -> [ "street" -> "r" | "height" -> 59.67 | "age" -> 45 | "level" -> 7 ] | "street" -> [] | "name" -> [ "street" -> "fopv" | " height" -> 43.01 ] ]
Enter Question: GET key1000
Received Answer: key1000 -> NOT FOUND
Enter Question: DELETE key1
Received Answer: key1 -> OK
Enter Question: GET key1
Received Answer: key1 -> NOT FOUND
Enter Question: QUERY key2.street
Received Answer: key2.street -> [ "height" -> 74.13 | "name" -> "v" ]
Enter Question: QUERY key2.street.name
Received Answer: key2.street.name -> v
Enter Question: QUERY key2.street.nam
Received Answer: key2.street.nam -> NOT FOUND
Enter Question: COMPUTE 2*x WHERE x = QUERY key3.height.level
Received Answer: 108
Enter Question: COMPUTE log(x)+tan(y)-2*x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.level
Received Answer: -332.21845269437216
Enter Question: GETT key3
Wrong format of question! Try again
Enter Question: COMPUTE 2*x WHERE x = QUERY key3.height.name
ERROR: x = QUERY key3.height.name is STRING, can not compute
Enter Question: COMPUTE 2*x WHERE x = QUERY key3.height.id
ERROR: x = QUERY key3.height.id NOT FOUND
Enter Question: COMPUTE log(x)+tan(y)-2*x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.le
ERROR: y = QUERY key10.age.le NOT FOUND
#No we test with down servers, In our test we have 3 total servers and 2 more index
#We down one server
Enter Question: COMPUTE log(x)+tan(y)-2*x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.level
Received Answer: -332.21845269437216
#And now we down onother one
Enter Question: COMPUTE log(x)+tan(y)-2*x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.level
WARNING: All server are= 2 or more servers are down and therefore it cannot guarantee the correct output
ERROR: x = QUERY key3.height.level NOT FOUND
#we down and the last server
Enter Question: COMPUTE log(x)+tan(y)-2*x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.level
All server are down

=========================

