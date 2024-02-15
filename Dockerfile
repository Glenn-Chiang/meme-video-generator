FROM python:3.9.5

WORKDIR /app

# Install cv2 dependencies that are normally present on local machine but missing in container
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]