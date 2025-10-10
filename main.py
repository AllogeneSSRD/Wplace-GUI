
import threading
from watchdog.observers import Observer

from Wplace.config import ConfigHandler

config_path = 'config.yaml'


if __name__ == "__main__":
    reload_event = threading.Event()
    cfg = ConfigHandler(config_path, reload_event)
    observer = Observer()
    observer.schedule(cfg, path='.', recursive=False)
    observer.start()
