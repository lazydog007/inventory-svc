from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'File {event.src_path} has been modified')

observer = Observer()
observer.schedule(MyHandler(), path='app', recursive=True)
observer.start()
print("observer started")
