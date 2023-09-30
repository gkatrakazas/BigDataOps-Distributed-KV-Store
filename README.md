
# BigDataOps - Distributed Key-Value Store with Query Engine

Welcome to BigDataOps, a powerful and scalable solution for managing big data and executing complex queries in a distributed environment. This project showcases a robust key-value store system and a query engine designed for big data sets.

## Overview
BigDataOps consists of two main components:

1. **Data Creation:** The data generation script (`genData.py`) generates synthetic data with nested structures, creating a dataset for testing and experimentation.

2. **Key-Value Store and Query Engine:** The key-value store and query engine are implemented in Python, utilizing a distributed architecture across multiple servers (`server1.py`, `server2.py`, `server3.py`). The client (`kvClient.py`) interacts with the servers to perform various operations, including GET, DELETE, QUERY, and complex COMPUTE operations.

## Getting Started
Follow these steps to set up and run BigDataOps: 1. **Generate Synthetic Data:** 
```
python3 genData.py -k keyFile.txt -n 100 -d 3 -l 4 -m 5
```
This command generates synthetic data for your testing needs.

 -  **Start Servers:**
    
    -   Start server1:
	    ```
	     python3 server1.py -a 127.0.0.1 -p 5001`
	    ```
	   
	 - Start server2: 
        ```
        python3 server2.py -a 127.0.0.1 -p 5002` 
        ```
    -   Start server3:        
        ```
        python3 server3.py -a 127.0.0.1 -p 5003` 
        ```
3.  **Index Data:**
    ```
    python3 kvClient.py -s serverFile.txt -i dataToIndex.txt -k 2` 
    ```
    This command indexes the generated data across the servers.
    
4.  **Interact with the Key-Value Store:** Use the client (`kvClient.py`) to interact with the key-value store and query engine. You can perform operations like GET, DELETE, QUERY, and complex COMPUTE operations.
    
 ## Example Executions

Here are some example interactions with the BigDataOps system:

-   Retrieving a value:  
    ```
    Enter Question: GET key1
    Received Answer: key1 -> [ "level" -> [ "height" -> 80.38 | "name" -> "oq" | " level" -> 26 ] | "height" -> [ "name" -> "uk" | " age" -> 18 | "level" -> 89 | "height" -> 10.56 | "street" -> "fo" ] | " age" -> [ "street" -> "r" | "height" -> 59.67 | "age" -> 45 | "level" -> 7 ] | "street" -> [] | "name" -> [ "street" -> "fopv" | " height" -> 43.01 ] ]
    ```
    
-   Deleting a key:  
    ```Enter Question: DELETE key1
    Received Answer: key1 -> OK
    ```
-   Complex query and computation:
    ```Enter Question: COMPUTE log(x)+tan(y)-2x WHERE x = QUERY key3.height.level AND y = QUERY key10.age.level
    Received Answer: -332.21845269437216
    ``` 

 ## Handling Server Failures

BigDataOps gracefully handles server failures. It checks the availability of servers before sending queries and provides appropriate error messages when servers are down.

Please feel free to explore, modify, and contribute to this project as needed. If you have any questions or encounter issues, don't hesitate to reach out to the project maintainers.

Happy data management and querying with BigDataOps! 🚀
