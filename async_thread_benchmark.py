from concurrent.futures import ThreadPoolExecutor
import threading
import psutil
import asyncio
import time
import os


def get_memory_mb():
    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    return mem.rss / 1024 / 1024


def get_thread_count():
    process = psutil.Process(os.getpid())
    num_threads = process.num_threads()
    return num_threads


def blocking_io_operation(task_id: int, duration: float = 0.01):
    time.sleep(duration)


async def async_operation(task_id: int, duration: float = 0.01):
    await asyncio.sleep(duration)


def run_with_threads(num_tasks: int, num_threads: int):
    with ThreadPoolExecutor(num_threads) as executor:
        results = list(
            executor.map(lambda i: blocking_io_operation(i), range(num_tasks))
        )

        return results


async def run_with_async(num_tasks: int):
    tasks = [async_operation(i) for i in range(num_tasks)]
    results = await asyncio.gather(*tasks)
    return results


def demo_scalability():
    print("=" * 50)
    print("Checking Scalability")
    print("=" * 50)

    test_cases = [100, 500, 1000, 5000]

    for num_tasks in test_cases:
        print(f"Doing {num_tasks} tasks")
        print("-" * 70)

        num_threads = 100
        print("Running multi-threaded version")
        start = time.time()
        run_with_threads(num_tasks=num_tasks, num_threads=num_threads)
        thread_duration = time.time() - start
        print(f"Time taken: {thread_duration:.3f} seconds")

        print("-" * 60)

        print("Running async version")
        start = time.time()
        asyncio.run(run_with_async(num_tasks))
        duration = time.time() - start
        print(f"Time taken {duration:.3f} seconds")


async def demo_memory_async_version():
    print("=" * 50)
    print("Checking Memory")
    print("=" * 50)

    baseline_memory = get_memory_mb()
    task_counts = [50, 100, 200, 500, 1000, 5000, 10000]
    task_list = []
    print(f"Baseline memory {baseline_memory:.1f} MB")

    for i in range(len(task_counts)):

        tasks_to_create = (
            task_counts[i] if i == 0 else task_counts[i] - task_counts[i - 1]
        )

        for j in range(tasks_to_create):
            task = asyncio.create_task(async_operation(j, duration=5))
            task_list.append(task)

        await asyncio.sleep(0.1)

        current_memory = get_memory_mb()

        memory_increase = current_memory - baseline_memory
        print(
            f"Current memory: {current_memory:.1f} MB. Memory increase: {memory_increase:.1f}"
        )

    await asyncio.gather(*task_list)


def demo_memory_threaded_version():
    print("=" * 50)
    print("Checking Memory")
    print("=" * 50)

    baseline_memory = get_memory_mb()
    baseline_threads = get_thread_count()

    thread_counts = [50, 100, 200, 500, 1000]

    print(
        f"Baseline memory {baseline_memory:.1f} MB, Number of threads: {baseline_threads}"
    )

    for i in range(len(thread_counts)):
        threads_to_create = (
            thread_counts[i] if i == 0 else thread_counts[i] - thread_counts[i - 1]
        )

        for _ in range(threads_to_create):
            thread = threading.Thread(target=time.sleep, args=(5,))
            thread.start()

        time.sleep(0.1)

        current_memory = get_memory_mb()
        num_threads = get_thread_count()

        memory_increase = current_memory - baseline_memory

        print(
            f"Current memory: {current_memory:.1f} MB. Number of threads: {num_threads}"
        )


def main():
    # demo_scalability()
    asyncio.run(demo_memory_async_version())


if __name__ == "__main__":
    main()
