import threading
import tkinter as tk
from tkinter import messagebox
import random
from server import MergeSortServer
from client import MergeSortClient
import time

class MergeSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parallel Merge Sort")

        #Number of clients
        tk.Label(root, text="Number of Clients:").pack()
        self.clientCountEntry = tk.Entry(root, justify='right')
        self.clientCountEntry.pack()

        #Array size
        tk.Label(root, text="Array Size per Client:").pack()
        self.arraySizeEntry = tk.Entry(root, justify='right')
        self.arraySizeEntry.pack()

        #Number of processes
        tk.Label(root, text="Number of Processes (Server):").pack()
        self.processCountEntry = tk.Entry(root, justify='right')
        self.processCountEntry.pack()

        #Start button
        self.startButton = tk.Button(root, text="Start Sorting", command=self.startSorting)
        self.startButton.pack(pady=10)

        #Status log box
        self.statusText = tk.Text(root, height=15, width=60)
        self.statusText.pack()

    def startSorting(self):
        try:
            clientCount = int(self.clientCountEntry.get())
            arraySize = int(self.arraySizeEntry.get())
            processCount = int(self.processCountEntry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers.")
            return

        self.startButton.config(state='disabled') #disable button after getting clicked
        self.log("Starting server and clients...")

        #Start server
        serverThread = threading.Thread(target=self.serverTarget, args=(processCount,), daemon=True)
        serverThread.start()

        #Start clients
        for i in range(clientCount):
            clientThread = threading.Thread(target=self.clientTarget, args=(i, arraySize), daemon=True)
            clientThread.start()

    #Same as __main__ in server
    def serverTarget(self, processCount):
        try:
            self.server = MergeSortServer(processCount=processCount)
            self.server.start()
        except Exception as e:
            self.log(f"Server error: {e}")

    #Same as __main__ in client
    def clientTarget(self, clientId, arraySize):
        try:
            client = MergeSortClient()
            randomArray = [random.randint(0, 10000000) for _ in range(arraySize)]
            startTime = time.time()
            sortedArray = client.sendArray(randomArray)
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.log(f"Client {clientId} completed task in {elapsedTime:.4f} seconds!")
            self.log(f"First 5 elements of Client {clientId}: {sortedArray[:5]}")
        except Exception as e:
            self.log(f"Client {clientId} error: {e}")

    def log(self, message):
        self.statusText.insert(tk.END, message + "\n" )
        self.statusText.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MergeSortApp(root)
    root.mainloop()
