import signal
import time

def handle_sigterm(signum, frame):
    print("SIGTERM received, cleaning up...")
    raise SystemExit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

try:
    print("Service running. Press Ctrl+C or send SIGTERM to stop.")
    while True:
        time.sleep(1)
finally:
    print("In finally block: cleanup here.")
