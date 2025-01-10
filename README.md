# Orlando Bus Stops Hash Table Implementation

## Overview
This script implements a custom hash table using linear probing and dynamic resizing. It processes data from a JSON file containing bus stops in Orlando, identified by unique stop codes and names. The implementation demonstrates:

- Hashing with collision resolution via linear probing.
- Dynamic resizing when the load factor exceeds 50%.
- Insertion and search operations on the hash table.

Additionally, the script compares hash table performance with a Python dictionary for data loading.

---

## Features
1. **Hash Table Implementation:**
   - **Linear Probing:** Handles collisions by searching for the next available bucket.
   - **Dynamic Resizing:** Automatically doubles the table size when the load factor exceeds 50%.
2. **Custom Hash Function:** Generates bucket indices based on string keys.
3. **JSON Parsing:** Reads and decodes bus stop data into Python objects.
4. **Performance Metrics:** Measures insertion and search times.

---

## Prerequisites
- Python 3.6 or higher
- JSON file with bus stop data (`stops.json`)

---

## Usage

### Prepare the JSON File
The script requires a JSON file named `stops.json` in the same directory. Each record should include:
```json
[
    {
        "code": "1234",
        "name": "Main St & 1st Ave"
    },
    {
        "code": "5678",
        "name": "Central Ave & 2nd St"
    }
]
```

### Run the Script
 To execute the script in a terminal:
```bash
python3 main.py
```

### Output
- Total bus stops processed and inserted.
- Number of collisions during insertion.
- Results of searching for specific stop codes.
- Comparison of hash table vs dictionary data loading performance.

---

## Performance Highlights
- Dynamic resizing ensures the hash table maintains efficiency even with high load factors.
- Linear probing resolves collisions but may increase search time under high load.

---
