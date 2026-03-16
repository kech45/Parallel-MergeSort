# Parallel Merge Sort

A distributed sorting system that combines parallel processing with a TCP client-server architecture. Large arrays are sent from clients to a central server, sorted using multiprocessing, and returned — all visualized through a Tkinter GUI.

## Architecture

```
[Client 1] ──┐
[Client 2] ──┼──► [TCP Server] ──► [Parallel Merge Sort] ──► sorted array back to clients
[Client N] ──┘
```

- **Client** — generates a random array, serializes it with `pickle`, and sends it over a TCP socket
- **Server** — accepts multiple clients concurrently using threads, sorts each array using parallel merge sort, and returns the result
- **Sorting** — splits the array into chunks, sorts each chunk in a separate process using `multiprocessing.Pool`, then merges the sorted chunks
- **GUI** — Tkinter interface to configure clients, array size, and process count, with a live status log

## Project Structure

```
├── client.py        # TCP client — sends array, receives sorted result
├── server.py        # TCP server — handles multiple clients with threading
├── sortingUtils.py  # Sequential and parallel merge sort implementations
└── mergeSortApp.py  # Tkinter GUI — launches server and clients
```

## How to Run

### GUI (recommended)

```bash
python mergeSortApp.py
```

Configure the number of clients, array size, and server process count, then click **Start Sorting**.

### Manual (server + client separately)

Start the server:

```bash
python server.py <process_count>
# example: python server.py 4
```

Run the client:

```bash
python client.py
# or with multiple clients:
python client.py <num_clients>
```

## Requirements

Python 3.7+ with no external dependencies — only standard library modules are used (`socket`, `pickle`, `multiprocessing`, `threading`, `tkinter`).

## Why Multiprocessing Instead of Multithreading?

Python has a **Global Interpreter Lock (GIL)** that prevents multiple threads from executing Python bytecode simultaneously. For CPU-bound tasks like sorting, threads don't provide true parallelism — only one thread runs at a time.

`multiprocessing` bypasses the GIL by spawning separate processes, each with its own Python interpreter and memory space. This allows sorting chunks to run truly in parallel across multiple CPU cores.

The server still uses **threads** for handling client connections, which is appropriate there since those threads spend most of their time waiting on I/O (network), not doing CPU work.

## Performance Notes

- Arrays smaller than 10,000 elements fall back to sequential merge sort — the overhead of spawning processes outweighs the parallelism gains at small sizes
- Each client connection is handled in its own thread, so multiple clients can be sorted concurrently
- Sorting time is logged server-side per request

## Sorting Algorithm

Sequential merge sort runs in **O(n log n)** time. The parallel version divides the array into `processCount` chunks, sorts each in parallel, then merges in a tournament-style loop:

```
[chunk1] [chunk2] [chunk3] [chunk4]
  └── merge ──┘     └── merge ──┘
       └────── merge ──────┘
```

The merge phase runs sequentially but represents only **O(n)** work after the parallel sort phase completes.
