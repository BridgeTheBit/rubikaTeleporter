import subprocess
import sys
import signal
import os

processes = []


def shutdown(signum=None, frame=None):
    for p in processes:
        if p.poll() is None:
            p.terminate()
    sys.exit(0)


def main():
    global processes

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    processes = [
        subprocess.Popen([sys.executable, "telebot.py"]),
        subprocess.Popen([sys.executable, "rub.py"]),
    ]

    while True:
        for p in processes:
            if p.poll() is not None:
                shutdown()
        signal.pause()


if __name__ == "__main__":
    main()
