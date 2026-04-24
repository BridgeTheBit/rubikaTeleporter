import json
import time
import os
import logging
from pathlib import Path

QUEUE_FILE = Path("queue/tasks.jsonl")
LOG_FILE = Path("logs/app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [RUB] %(levelname)s: %(message)s",
)


def get_next_task():
    if not QUEUE_FILE.exists():
        return None

    with open(QUEUE_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        return None

    task = json.loads(lines[0])

    with open(QUEUE_FILE, "w") as f:
        f.writelines(lines[1:])

    return task


def upload_to_rubika(file_path, target):
    # اینجا بعداً API واقعی روبیکا قرار می‌گیرد
    logging.info(f"Uploading {file_path} to {target}")
    time.sleep(3)
    logging.info(f"Uploaded {file_path}")


def worker():
    logging.info("Rubika worker started")

    while True:
        task = get_next_task()

        if not task:
            time.sleep(5)
            continue

        file_path = task.get("file_path")
        target = task.get("target")

        if not file_path or not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            continue

        try:
            upload_to_rubika(file_path, target)

            try:
                os.remove(file_path)
                logging.info(f"Deleted local file: {file_path}")
            except Exception as e:
                logging.warning(f"Could not delete file {file_path}: {e}")

        except Exception as e:
            logging.error(f"Upload failed: {e}")

            with open(QUEUE_FILE, "a") as f:
                f.write(json.dumps(task) + "\n")

            time.sleep(5)


if __name__ == "__main__":
    worker()
