import configparser
import os
import shutil
import time
import logging
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reading the configuration file
config = configparser.ConfigParser()
config.read('rtsp_server.conf')

WATCHED_DIR = config['DEFAULT']['WatchedDir']
DEST_DIR = config['DEFAULT']['DestDir']
MAX_FILES = int(config['DEFAULT']['MaxFiles'])

def cleanup_watched_dir():
    try:
        files = sorted([os.path.join(WATCHED_DIR, f) for f in os.listdir(WATCHED_DIR)], key=os.path.getmtime, reverse=True)
        for f in files[MAX_FILES:]:
            os.remove(f)
            logging.info(f"Removed old file: {f}")
    except Exception as e:
        logging.error(f"Failed to clean up watched directory: {e}")

def copy_latest_file():
    try:
        # Find the latest file in the watched directory
        latest_file = max([os.path.join(WATCHED_DIR, f) for f in os.listdir(WATCHED_DIR) if os.path.isfile(os.path.join(WATCHED_DIR, f))], key=os.path.getmtime)
        latest_file_time = os.path.getmtime(latest_file)

        # Path to the temporary and final destination files
        dest_file_tmp = os.path.join(DEST_DIR, "last_image_tmp.jpg")
        dest_file = os.path.join(DEST_DIR, "last_image.jpg")

        # Check if the destination file exists and compare modification times
        if not os.path.exists(dest_file) or os.path.getmtime(dest_file) < latest_file_time:
            shutil.copy2(latest_file, dest_file_tmp)

            # Remove the existing symbolic link if it exists
            if os.path.islink(dest_file):
                os.unlink(dest_file)
            # Or if it's a regular file, remove it
            elif os.path.exists(dest_file):
                os.remove(dest_file)

            os.symlink(dest_file_tmp, dest_file)
            logging.info(f"Copied latest file to {DEST_DIR}")
        else:
            logging.info("The latest file is already the most recent. No copy needed.")
    except ValueError:
        logging.info("No files to copy.")


def initialize_and_start_streams():
    # Initialize GStreamer and set up the RTSP server
    logging.info("Initializing GStreamer and setting up the RTSP server...")
    Gst.init(None)

    server = GstRtspServer.RTSPServer.new()
    server.set_service("8554")

    factory1 = GstRtspServer.RTSPMediaFactory.new()
    factory1.set_launch("( multifilesrc location=/tmp/indoor/last_image.jpg caps=\"image/jpeg,framerate=1/2\" loop=true ! jpegdec ! videoscale ! video/x-raw,width=640,height=480 ! videoconvert ! x264enc bitrate=300 tune=zerolatency ! rtph264pay name=pay0 pt=96 )")
    factory1.set_shared(True)

    mounts = server.get_mount_points()
    mounts.add_factory("/spica", factory1)

    server.attach(None)
    logging.info("RTSP server is up and running.")

# Run cleanup and copy functions in the background
def manage_files():
    while True:
        copy_latest_file()
        cleanup_watched_dir()
        time.sleep(10)

# Main loop to restart streams in case of an error
if __name__ == "__main__":
    # Start file management in a separate thread
    from threading import Thread
    file_manager_thread = Thread(target=manage_files)
    file_manager_thread.daemon = True
    file_manager_thread.start()

    while True:
        try:
            initialize_and_start_streams()
            loop = GLib.MainLoop()
            logging.info("Main loop started.")
            loop.run()
        except Exception as e:
            logging.error(f"An error occurred: {e}. Restarting streams...")
            time.sleep(5)  # Delay before retrying
