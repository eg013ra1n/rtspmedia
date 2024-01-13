import os
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

VIDEO_FOLDER = "/app/videos"
RTSP_PORT = 8554

class RTSPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

class FileHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.event_type == 'modified' or event.event_type == 'created':
            self.server.update_video()

class RTSPServer:
    def __init__(self):
        self.latest_video = None
        self.video_path = os.path.join(VIDEO_FOLDER, "latest.jpg")
        self.file_handler = FileHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.file_handler, path=VIDEO_FOLDER, recursive=False)
        self.observer.start()

    def update_video(self):
        time.sleep(1)  # Добавьте паузу, чтобы файл полностью записался
        self.latest_video = self.video_path
        print(f"Updated video: {self.latest_video}")

    def run(self):
        httpd = TCPServer(("0.0.0.0", RTSP_PORT), RTSPHandler)
        httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)

    rtsp_server = RTSPServer()

    # Запустите RTSP-сервер в отдельном потоке
    rtsp_thread = Thread(target=rtsp_server.run)
    rtsp_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        rtsp_server.observer.stop()

    rtsp_thread.join()
    rtsp_server.observer.join()
