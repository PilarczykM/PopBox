# PopBox
PopBox is a lightweight event-driven task queue using FastAPI, Redis, and asyncio. It features async task dispatching, retries, and scalable worker design — ideal for learning or as a base for background job systems.

---

## 📦 Tech Stack

| Area                | Technology                        |
|---------------------|-----------------------------------|
| API Backend         | FastAPI                           |
| Queue & Broker      | Redis                             |
| Worker              | Python asyncio                    |
| Packaging           | uv (PEP 621 project manager)      |
| Lint & Format       | Ruff (unified tool)               |
| Containerization    | Docker + Docker Compose           |
| Frontend (optional) | React + SWR + WebSockets          |
| Monitoring          | Prometheus + Grafana (optional)   |
| Tracing             | OpenTelemetry + Jaeger (optional) |

---

## 🔧 Setup Instructions

### 1. Create the environment with uv

```bash
uv venv .venv
source .venv/bin/activate
uv sync
```

---

# 🚀 Development Stages

## Stage 1 – Project Scaffolding
- [ ] Set up directory structure
- [x] Create `pyproject.toml` and initialize virtualenv with `uv`
- [ ] Add `.env` and configuration loader using `python-dotenv`
- [x] Set up `Dockerfile` and `docker-compose.yml`
- [x] Enable Ruff and configure auto-formatting in `pyproject.toml`

## Stage 2 – API & Enqueue (Producer)
- [x] Build FastAPI route `POST /task` to enqueue tasks
- [x] Use `RPUSH` to add tasks to Redis queue
- [x] JSON-serialize task payloads
- [ ] Start with basic task: `send_email`

## Stage 3 – Worker (Consumer)
- [ ] Create `worker.py` with `BLPOP` loop to consume tasks
- [ ] Dispatch tasks dynamically using `importlib`
- [ ] Handle exceptions with retry mechanism
- [ ] Add optional dead-letter queue using `ZADD`

## Stage 4 – Task Handlers
- [ ] `send_email` → simulate via `print` or logging
- [ ] `generate_report` → write a fake file to `/tmp/`
- [ ] Each task resides in `app/tasks/*.py`

## Stage 5 – Testing
- [ ] Unit test for enqueue function
- [ ] Worker task execution tests
- [ ] Retry logic test (simulate failures)

## Stage 6 (Optional) – Web Dashboard
- [ ] WebSocket server to stream worker activity
- [ ] React + SWR frontend to display logs in real time
- [ ] Optional: analytics or status visualization with charts

## Stage 7 (Optional) – Monitoring
- [ ] Install the `prometheus_client` Python library
- [ ] Add a `/metrics` endpoint to the FastAPI app for Prometheus scraping
- [ ] Export relevant metrics such as:
    - Task execution count (`Counter`)
    - Task duration (`Histogram`)
    - Retry and failure count (`Counter`)
    - Queue length via Redis's `LLEN`

- [ ] Configure Prometheus in `docker-compose.yml` with proper scrape settings
- [ ] Add Grafana to `docker-compose.yml` and link it to Prometheus
- [ ] Build dashboards in Grafana to visualize:
    - Task throughput over time
    - Task execution latency
    - Retry and error rates
    - Queue depth over time

- [ ] (Optional) Configure alerting rules in Grafana or Prometheus Alertmanager, e.g.:
    - Task backlog growing too fast
    - High failure or retry rate
    - Long queue wait times

## Stage 8 (Optional) – Observability with Tracing
- [ ] Install `opentelemetry-api` and `opentelemetry-sdk`
- [ ] Instrument FastAPI app with `OpenTelemetryMiddleware`
- [ ] Add trace spans in `enqueue_task()` and worker dispatcher
- [ ] Export traces to Jaeger/Grafana Tempo
---

# 🤔 Why Use an Event-Driven Queue?

Event-driven queues allow services to communicate in an asynchronous and decoupled way. This leads to better scalability, fault isolation, and system responsiveness. They're ideal for offloading time-consuming or failure-prone tasks such as:

* Sending emails
* Generating reports
* Performing background computations
* Communicating with unreliable third-party APIs

This architectural pattern promotes loose coupling and high cohesion.

---

# 🗺 System Architecture

```
Client
   |
   v
POST /task (FastAPI)
   |
   v
Redis Queue (RPUSH)
   |
   v
Worker (BLPOP)
   |
   v
Task Handler (send_email, generate_report, etc.)
```

**Component Overview:**

* Client/API Layer: Sends tasks to the system
* Redis Queue: Stores tasks until consumed
* Worker: Listens for new tasks and executes them
* Task Handlers: Implement specific logic per task type

Each component follows SRP and is easily testable and replaceable (📘 "Single Responsibility Principle", "Design for Replaceability").

---

# 🔁 Retry on Failure

When a task fails (e.g. exception raised in handler), the system retries it N times. If it still fails, it's moved to a dead-letter queue via `ZADD`.

Retry strategies can include:
* Constant delay
* Exponential backoff
* Jitter

This promotes resilience and observability

---

# 📊 Monitoring and Logging

Monitoring and logging are crucial to understanding how the system behaves in production.

**Logging**

* Each worker logs:
    * When a task starts and completes
    * Exceptions and retries
    * Final failure and DLQ (dead-letter queue) insertions

Python’s built-in logging module is used, with log levels like `INFO`, `ERROR`, and `DEBUG`.

**Monitoring**

* Integrate with Prometheus using the prometheus_client library
* Expose metrics such as:
    * Task execution count and duration
    * Retry attempts
    * Queue sizes and latency
* Add /metrics route in FastAPI for Prometheus to scrape
* Use Grafana for building dashboards and alerting rules

Tracing tools like OpenTelemetry can also be integrated for deep visibility into task flows

---

# 🔁 Queue Design (Redis)
* RPUSH queue_name → enqueue
* BLPOP queue_name → blocking dequeue
* Retry on failure → custom logic or exponential backoff
* Dead-letter → ZADD dead_queue with timestamp and reason

# 🧠 Optional Extensions
* Dead-letter TTL expiration and monitoring
* Prometheus integration (for metrics)
* API Rate limiting with Redis
* Multi-priority queues
