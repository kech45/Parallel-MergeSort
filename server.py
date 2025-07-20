import socket
import pickle
from threading import Thread
import time
from sortingUtils import parallelMergeSort

class MergeSortServer:
    def __init__(self, host='127.0.0.1', port=65432, processCount=None):
        #Initialize the server with host, port, and number of processes for sorting
        #Raise error if processCount not specified (needed for parallel sorting)
        if processCount is None:
            raise ValueError("You must specify process_count.")
        self.host = host
        self.port = port
        self.processCount = processCount

    def start(self):
        #Create a TCP socket, AF_INET - Address family for IPV4
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port)) #Bind the socket to the specified host and port
            s.listen()  #Start listening for incoming client connections
            print(f"[SERVER] Listening on {self.host}:{self.port} with {self.processCount} processes")
            
            #Server runs indefinitely, accepting new connections
            while True:
                conn, addr = s.accept()  #Accept new connection
                #Spawn a new thread to handle this client connection
                thread = Thread(target=self.handleClient, args=(conn, addr))
                thread.start()

    def handleClient(self, conn, addr): #conn - Socket object to communicate with client; addr - Tuple {client address, client port}
        try:
            print(f"[INFO] Connected to {addr}")
            
            chunks = []
            #Reads data from the socket in small chunks of 4096 bytes.
            while True:
                chunk = conn.recv(4096)
                if not chunk:  #No more data, client closed send
                    break
                chunks.append(chunk)
            #Combine all chunks into a single bytes object
            data = b''.join(chunks) # b'' - empty bytes object

            #Deserialize the received bytes into the original array the client sent
            arr = pickle.loads(data)
            print(f"[INFO] Received array of length {len(arr)} from {addr}")

            #Time the sorting operation
            startTime = time.time()
            sortedArr = parallelMergeSort(arr, self.processCount)
            endTime = time.time()
            print(f"[TIME] Sorting took {endTime - startTime:.4f} seconds")
            
            #Serialize the sorted array to bytes object and send it back to the client
            result = pickle.dumps(sortedArr)
            #Using send all because it sends everything back to client, using send might not send everything if input is too large
            conn.sendall(result) 
            print(f"[INFO] Sent sorted array to {addr}")

        except Exception as e:
            #Print error if something went wrong during handling
            print(f"[ERROR] Handling client {addr}: {e}")
        finally:
            #Close the client connection cleanly in any case
            conn.close()
            print(f"[INFO] Closed connection to {addr}")


if __name__ == "__main__":
    import multiprocessing
    import sys

    multiprocessing.freeze_support()  #For compatibility on Windows when using multiprocessing

    #Expect exactly one argument: number of processes to use
    if len(sys.argv) != 2:
        print("Usage: python server.py <process_count>")
        sys.exit(1)

    try:
        #Convert the argument to an integer
        processCount = int(sys.argv[1])
    except ValueError:
        #Exit if the argument is not a valid integer
        print("Process count must be an integer.")
        sys.exit(1)

    #Create server instance and start it
    server = MergeSortServer(processCount=processCount)
    server.start()
