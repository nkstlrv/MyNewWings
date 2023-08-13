from celery import shared_task
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")


@shared_task
def debug_task():
    for i in range(10):
        logging.info(f"TESTING WORKER")
        time.sleep(0.3)
    return True
