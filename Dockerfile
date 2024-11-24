FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libglib2.0 \
    libgl1-mesa-glx \
    libturbojpeg && \
    apt-get clean

RUN git clone https://github.com/ria-com/nomeroff-net.git /nomeroff-net
WORKDIR /nomeroff-net
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
