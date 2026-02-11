import os
import time
import signal
import sys
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from processor import process_single_image
import sentry_sdk

VALID_EXTENSIONS = (".jpg", ".png", ".jpeg")

class ImageWatcher(FileSystemEventHandler):
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.processing_cache = set() # Simple memory to prevent double-processing

    def is_valid(self, path):
        return path.lower().endswith(VALID_EXTENSIONS)

    def process_file(self, file_path):
        abs_path = os.path.abspath(file_path)
        
        # 1. Prevent double-processing (Ignore if we just did this file in the last 2 seconds)
        if abs_path in self.processing_cache:
            return
        
        if self.is_valid(abs_path):
            # 2. RETRY LOOP: Wait for file to be "ready" (Unlocked by OS)
            retries = 5
            while retries > 0:
                try:
                    # Try to open the file to check if it's locked
                    with open(abs_path, 'rb'):
                        break 
                except IOError:
                    time.sleep(0.5) # Wait for copy to finish
                    retries -= 1
            
            print(f"⚙️  Processing: {os.path.basename(abs_path)}", flush=True)
            process_single_image(abs_path, self.output_dir)
            print(f"✅ Saved to: {os.path.join(self.output_dir, 'processed')}", flush=True)
            
            # Add to cache and clean it up after a delay
            self.processing_cache.add(abs_path)
            time.sleep(0.1) # Small breather for RAM

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.dest_path)
    
def graceful_shutdown(signum, frame):
    print("\n🧹 Cleaning up and stopping Watcher...", flush=True)
    observer.stop()
    observer.join()
    sys.exit(0)
    
if __name__ == "__main__":
    # --- 1. Standardizing Paths using Absolute Paths ---
    # os.getcwd() ensures that in Docker, we are at /app
    # In VS Code, it ensures we are in your project root
    base_path = os.getcwd() 
    input_dir = os.path.join(base_path, "input")
    output_dir = os.path.join(base_path, "output")

    # Ensure directories exist before the scan
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the handler with the absolute output path
    event_handler = ImageWatcher(output_dir)
    observer = Observer()
    
    # --- 2. Handle OS Signals for Clean Shutdown ---
    if os.name != 'nt': # Linux/Docker
        signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    # --- 3. 🚀 STARTUP SCAN (Process existing files) ---
    # We use absolute paths here so the processor never gets confused
    print("🔍 Scanning for existing files...", flush=True)
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            full_path = os.path.join(input_dir, filename)
            # Ignore hidden files (like .gitignore) and debug folders
            if os.path.isfile(full_path) and not filename.startswith('.'):
                event_handler.process_file(full_path)

    # --- 4. START WATCHER ---
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.start()

# --- 📢 USER INSTRUCTIONS ---
    print("\n" + "="*50)
    print("🚀 Watcher Service is LIVE.")
    print(f"📍 Input:  {input_dir}")
    print(f"📦 Output: {output_dir}")
    print("\n💡 Press Ctrl+C to stop the service and exit.")
    print("="*50 + "\n", flush=True)

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\nStopping observer...")
        observer.stop()
    except Exception as e:
        print(f"Unexpected error: {e}")
        observer.stop()
        
    observer.join()