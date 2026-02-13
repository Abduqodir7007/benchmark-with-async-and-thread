# Async vs Threading Benchmark

A Python benchmark comparing async/await and threading approaches for I/O-bound operations.

## Features

- **Scalability Test**: Compares execution time for varying numbers of tasks
- **Memory Test**: Measures memory consumption for async tasks vs threads

## Setup

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows
```

### Install Dependencies

```bash
pip install psutil
```

## Usage

```bash
python async_thread_benchmark.py
```
