import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_single_image

VALID_EXTENSIONS = (".jpg", ".png", ".jpeg")


class ImageWatcher(FileSystemEventHandler):

    def __init__(self, output_dir):
        self.output_dir = output_dir

    def is_valid(self, path):
        return path.lower().endswith(VALID_EXTENSIONS)

    def on_created(self, event):
        print(f"[CREATED] {event.src_path}")

        if event.is_directory:
            return

        if self.is_valid(event.src_path):
            print("→ Valid image detected (created)")
            process_single_image(event.src_path, self.output_dir)

    def on_moved(self, event):
        print(f"[MOVED] {event.dest_path}")

        if event.is_directory:
            return

        if self.is_valid(event.dest_path):
            print("→ Valid image detected (moved)")
            process_single_image(event.dest_path, self.output_dir)


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "..", "input")
    output_dir = os.path.join(base_dir, "..", "output")

    os.makedirs(output_dir, exist_ok=True)

    event_handler = ImageWatcher(output_dir)
    observer = Observer()
    observer.schedule(event_handler, input_dir, recursive=False)
    observer.start()

    print("🚀 Watcher Service Started. Waiting...")

    try:
        while True:
            time.sleep(1)  # low CPU usage
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
