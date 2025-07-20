#client.py
import socket
import pickle
import random
import sys  
import threading

BUFFER_SIZE = 4096

class MergeSortClient:
    #Initialize the client's target server address and port
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def sendArray(self, arr):
        #Serialize(convert) the array to bytes using pickle
        message = pickle.dumps(arr)
        #Create a TCP socket and connect to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port)) #Connect to the server
            s.sendall(message) #Send the serialized array
            s.shutdown(socket.SHUT_WR)  #Tell server no more data will be sent

             #Receive the response (sorted array) in chunks
            chunks = []
            while True:
                chunk = s.recv(BUFFER_SIZE) #Read up to BUFFER_SIZE bytes
                if not chunk:
                    break #Exit loop when no more data is received
                chunks.append(chunk) #Accumulate chunks
                
        #Combine all received chunks into a single bytes object        
        data = b''.join(chunks)
        
        #Convert(Deserialize) bytes object ot sorted array
        return pickle.loads(data)
 
 
#Test function   
def runClient(clientID, arraySize = 10000000):
        #Create an instance of the client
    client = MergeSortClient()

#Generate a large array of 10 million random integers
    randomArray = [random.randint(0, arraySize) for _ in range(arraySize)]

#Send the array to the server and receive the sorted result
    sortedArr = client.sendArray(randomArray)
    print(f"Client {clientID}'s sorted array's first 10 elements:", sortedArr[:10])
    
if __name__ == "__main__":
    # Default: 1 client
    num_clients = 1

    if len(sys.argv) > 1:
        try:
            num_clients = int(sys.argv[1])
        except ValueError:
            print("Usage: python client.py [num_clients]")
            sys.exit(1)

    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=runClient, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"All {num_clients} clients finished.")