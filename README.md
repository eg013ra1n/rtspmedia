# RTSP Stream Server

This project sets up a Real-Time Streaming Protocol (RTSP) server using GStreamer and GstRtspServer. It watches a specified directory for new files, automatically cleans up older files beyond a defined limit, and streams the latest file via RTSP. The server is designed to be robust, with error handling that restarts the streams in case of an interruption.

## Features

- **Directory Watching:** Automatically monitors a specified directory for new files.
- **Automatic Cleanup:** Cleans up the oldest files in the watched directory, maintaining a maximum number of files.
- **File Streaming:** Streams the latest file from the watched directory over RTSP.
- **Robust Error Handling:** Automatically restarts the streaming service in case of errors.

## Requirements

- Python 3.x
- GStreamer 1.0
- GstRtspServer 1.0
- GLib

## Installation

1. **Install GStreamer and GstRtspServer:**

   Ensure you have GStreamer and GstRtspServer installed on your system. These are available from most package managers or from the [GStreamer website](https://gstreamer.freedesktop.org/).

2. **Install Python Dependencies:**

   While the script primarily uses standard libraries, ensure your Python environment is set up with the necessary versions.

3. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

4. **Configuration:**

   Modify `rtsp_server.conf` to set your watched and destination directories, along with the maximum number of files to keep.

## Usage

Run the script using Python:

```bash
python rtsp_server.py
```

The script starts by watching the specified directory for new files, streaming the latest file, and cleaning up old files.

## Configuration

The `rtsp_server.conf` configuration file contains settings for the watched directory (`WatchedDir`), destination directory (`DestDir`), and the maximum number of files to keep (`MaxFiles`). Update these settings according to your requirements.

Example:

```ini
[DEFAULT]
WatchedDir = /path/to/watched/dir
DestDir = /path/to/destination/dir
MaxFiles = 10
```

## Contributions

Contributions are welcome! Please submit a pull request or open an issue to discuss proposed changes.
