from pipeline.event_queue import event_queue

def queue_health():
    size = event_queue.qsize()
    maxsize = event_queue.maxsize
    percent = (size / maxsize) * 100

    if percent < 40:
        status = "HEALTHY"
    elif percent < 80:
        status = "WARNING"
    else:
        status = "CRITICAL (BACKPRESSURE)"

    return size, maxsize, round(percent, 2), status
