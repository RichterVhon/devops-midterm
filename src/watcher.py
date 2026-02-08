# this is a placeholder for the Watcher service that will monitor file changes and trigger the appropriate actions.
# you can replace this with actual file watching logic using libraries like watchdog or inotify, but for now, it just simulates a running service that can be gracefully stopped.

import time
import sys

def graceful_shutdown():
    print("🧹 Cleaning up and stopping Watcher...", flush=True)
    # Observer stop logic goes here
    print("💤 Watcher stopped safely.", flush=True)
    sys.exit(0)

print("🚀 Watcher Service Started. Waiting...", flush=True)

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    graceful_shutdown()
finally:
    graceful_shutdown()