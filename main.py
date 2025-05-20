import aiohttp
import asyncio
import time

SERVER_URL = "http://localhost:8080/fragment"

async def fetch_fragment(session, fragment_id, puzzle_pieces, lock, max_index_known):
    url = f"{SERVER_URL}?id={fragment_id}"
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            index = data["index"]
            text = data["text"]

            async with lock:
                if index not in puzzle_pieces:
                    puzzle_pieces[index] = text
                    if index > max_index_known[0]:
                        max_index_known[0] = index
            return True
    except aiohttp.ClientError as e:
        print(f"Error fetching fragment {fragment_id}: {e}")
        return False

async def solve_puzzle():
    puzzle_pieces = {}
    max_index_known = [-1]
    lock = asyncio.Lock()
    start_time = time.time()

    active_tasks = set()
    next_id_to_query = 0

    while True:
        while len(active_tasks) < 50:
            task = asyncio.create_task(fetch_fragment(
                aiohttp.ClientSession(),
                next_id_to_query,
                puzzle_pieces,
                lock,
                max_index_known
            ))
            active_tasks.add(task)
            task.add_done_callback(active_tasks.discard)
            next_id_to_query += 1

        async with lock:
            if max_index_known[0] != -1:
                all_found = True
                for i in range(max_index_known[0] + 1):
                    if i not in puzzle_pieces:
                        all_found = False
                        break
                if all_found and len(puzzle_pieces) == max_index_known[0] + 1:
                    break

        await asyncio.sleep(0.01)

    for task in active_tasks:
        task.cancel()

    end_time = time.time()
    elapsed_time = end_time - start_time

    sorted_fragments = [puzzle_pieces[i] for i in sorted(puzzle_pieces.keys())]
    full_message = "".join(sorted_fragments)

    print(f"Full message: {full_message}")
    print(f"Time taken: {elapsed_time:.2f} seconds")

    if elapsed_time < 1:
        print("Bonus Challenge completed: Puzzle solved in under 1 second!")
    else:
        print("Bonus Challenge not met.")

if __name__ == "__main__":
    async def main():
        async with aiohttp.ClientSession() as session:
            puzzle_pieces = {}
            max_index_known = [-1]
            lock = asyncio.Lock()
            start_time = time.time()

            active_tasks = set()
            next_id_to_query = 0

            while True:
                while len(active_tasks) < 50:
                    task = asyncio.create_task(fetch_fragment(
                        session,
                        next_id_to_query,
                        puzzle_pieces,
                        lock,
                        max_index_known
                    ))
                    active_tasks.add(task)
                    task.add_done_callback(active_tasks.discard)
                    next_id_to_query += 1

                async with lock:
                    if max_index_known[0] != -1:
                        all_found = True
                        for i in range(max_index_known[0] + 1):
                            if i not in puzzle_pieces:
                                all_found = False
                                break
                        if all_found and len(puzzle_pieces) == max_index_known[0] + 1:
                            break

                await asyncio.sleep(0.01)

            for task in active_tasks:
                task.cancel()

            end_time = time.time()
            elapsed_time = end_time - start_time

            sorted_fragments = [puzzle_pieces[i] for i in sorted(puzzle_pieces.keys())]
            full_message = " ".join(sorted_fragments)

            print(f"Full message: {full_message}")
            print(f"Time taken: {elapsed_time:.2f} seconds")

            if elapsed_time < 1:
                print("Bonus Challenge completed: Puzzle solved in under 1 second!")
            else:
                print("Bonus Challenge not met.")

    asyncio.run(main())