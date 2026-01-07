from pipeline.producer import start_producer
from pipeline.stream_engine import run_engine


if __name__ == "__main__":
    start_producer(batch_size=5, interval=0.2)
    run_engine()
