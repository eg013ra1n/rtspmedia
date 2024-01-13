FROM ubuntu:latest

# Устанавливаем необходимые пакеты
RUN apt-get update && \
    apt-get install -y \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    python3 \
    python3-pip

# Устанавливаем Python-модули
RUN pip3 install watchdog

# Копируем Python-скрипт в контейнер
COPY rtsp_server.py /app/rtsp_server.py

# Запускаем скрипт при старте контейнера
CMD ["python3", "/app/rtsp_server.py"]
