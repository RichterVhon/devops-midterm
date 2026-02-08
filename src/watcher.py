# this is a simple watcher script that can be used to keep a container running and handle graceful shutdowns
# you can fully replace the contents of this file with your own code, but make sure to keep the graceful shutdown logic if you want to handle signals properly

import signal
import sys
import time

def graceful_shutdown(signum=None, frame=None):
    # This function now handles BOTH manual calls and OS signals
    print("\n🧹 Cleaning up and stopping Watcher...", flush=True)
    # Observer cleanup logic goes here
    print("💤 Watcher stopped safely.", flush=True)
    sys.exit(0)

# Register the signals explicitly
# SIGINT = Ctrl+C
# SIGTERM = Docker Stop
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

print("🚀 Watcher Service Started. Waiting...", flush=True)

try:
    while True:
        time.sleep(1)
except Exception as e:
    print(f"❌ Unexpected Error: {e}", flush=True)
    sys.exit(1)