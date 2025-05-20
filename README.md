# Puzzle Decoder Race Solution

## How to Run the Project

1.  **Prerequisites:**
    * Python 3.8+ installed.
    * Docker installed and running (to host the puzzle server).

2.  **Start the Puzzle Server:**
    Open your terminal or command prompt and run the following Docker command to start the puzzle server locally:
    ```bash
    docker run -p 8080:8080 ifajardov/puzzle-server
    ```
    The server will be accessible at `http://localhost:8080/fragment?id=...`.

3.  **Install Dependencies:**
    Navigate to the directory where you saved the Python script (`main.py`) and install the necessary Python library:
    ```bash
    pip install aiohttp
    ```

4.  **Run the Solution:**
    Execute the Python script:
    ```bash
    python main.py
    ```

## Strategy for Speed and Correctness

Our solution focuses on achieving both speed and correctness by leveraging asynchronous programming and a robust completion detection mechanism.

### Speed Strategy

* **Asynchronous I/O with `asyncio` and `aiohttp`:** The core of our speed strategy is the use of Python's `asyncio` library along with `aiohttp` for making HTTP requests. This allows us to issue multiple concurrent requests to the puzzle fragment server. Since each request has a random delay of 100-400ms, performing requests sequentially would be inefficient. By making requests in parallel, we minimize the total waiting time for responses.
* **Concurrent Request Pool:** Instead of making a fixed number of requests, our program maintains a dynamic pool of active asynchronous tasks (e.g., 50 concurrent requests). As soon as a request completes, a new one is initiated with a different `id`. This ensures that we are continuously querying the server and maximizing our chances of receiving all fragments quickly, irrespective of individual request delays.
* **Incremental ID Generation:** The server allows querying any `id` and will always return a valid piece, with the same `id` always returning the same result. Our strategy is to simply increment an `id` counter and use these sequential numbers for our queries. This avoids the overhead of random ID generation and ensures that we will eventually "discover" all unique pieces, as the number of pieces is bounded (e.g., $\le 10$).

### Correctness Strategy

* **Storing Fragments by Position:** Fragments are collected and stored in a dictionary where the key is the `index` (position) and the value is the `text` of the fragment. This ensures that pieces are organized correctly regardless of the order in which they are received.
* **Robust Completion Detection:** The total number of pieces is unknown.