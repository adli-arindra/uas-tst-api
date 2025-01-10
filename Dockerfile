FROM python:3.10.5
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && python -m pip install --upgrade pip \
    && python -m pip install dlib


EXPOSE 5000
CMD ["python", "haircut.py"]