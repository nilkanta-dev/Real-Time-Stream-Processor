# Real-Time Stream Processor (Python)

## Overview

A high-performance, real-time streaming analytics engine built in Python to process continuous event streams with **bounded memory**, **sliding windows**, **burst detection**, and **replay-based recovery**.

This project focuses on *how real streaming systems work internally* rather than UI or framework-heavy abstractions.

---

## Key Features

* **Real-time event ingestion** using a producer–consumer architecture
* **Sliding time windows** (5s / 15s / 60s)
* **Top-K frequency analytics** using heap-based selection
* **Duplicate filtering** using Bloom Filters for bounded memory
* **Burst detection** via growth-based frequency analysis
* **Backpressure-aware monitoring** (queue health & EPS)
* **Append-only event logging** for durability
* **Replay-based recovery** to rebuild in-memory state after restart
* **Config-driven behavior** using YAML configuration

---

## Architecture

```
Producer  →  Event Queue  →  Stream Engine
                ↓
        Append-only Event Log
                ↓
          Replay on Restart
```

**Design principles:**

* Separation of concerns (ingestion, processing, monitoring)
* Disposable in-memory state
* Durable event source of truth

---

## Why This Project Exists

Most streaming tutorials hide complexity behind frameworks.

This project was built to deeply understand:

* how streaming systems use data structures in practice
* why memory must remain bounded
* how replay enables recovery
* how bursts and trends emerge from live data

The goal was *systems understanding*, not UI polish.

---

## Core Concepts & Tech Used

* Python
* Threading & producer–consumer model
* Hash maps, heaps, Bloom filters
* Sliding window algorithms
* Backpressure & throughput monitoring
* Append-only logs & replay
* Configuration-driven system design

---

## How to Run

```bash
python main.py
```

The system will:

* start the producer
* ingest events in real time
* compute windowed analytics
* detect bursts
* monitor system health

---

## Example Output

```
=== REAL-TIME TRENDING ===
5s Window Top 3: [(12, 'banana'), (3, 'apple'), (2, 'dog')]
BURST [5s] banana | 4 → 12 (3.0x)

Queue: 12/1000  (1.2%)  Status: HEALTHY
EPS: 950 events/sec
```

---

## Recovery & Replay

* All incoming events are written to an **append-only log**
* On restart, the engine **replays historical events**
* In-memory state (windows, heaps, filters) is rebuilt deterministically

This simulates recovery behavior used in real streaming systems.

---

## Future Improvements

* Checkpoint-based recovery (partial replay)
* Persistent state snapshots
* Distributed ingestion
* REST-based event input
* Real-time dashboard visualization

---

## Final Note

This project emphasizes **engineering fundamentals** over frameworks and demonstrates how real-time systems behave under continuous load.


#### Author
*Nilkanta Rabha*<br>
*Full-Stack Python Developer*
