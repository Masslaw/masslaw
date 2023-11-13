# Use the latest Python image with a specified platform
FROM --platform=linux/amd64 python:3.10

# Update the package repository
RUN apt-get update

# Install necessary packages
RUN apt-get install -y libgl1-mesa-glx  # for cv2
RUN apt-get install -y poppler-utils  # for pdf processing
RUN apt-get install -y \  # tesseract
    curl \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-heb \
    tesseract-ocr-ara
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libreoffice  # process office documents

# Copy the requirements.txt first to leverage Docker cache
COPY /src/requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt

# Copy the source code into the container
COPY /src /src
RUN chmod +x /src/main.py

# Command to run on container start
ENTRYPOINT ["python3", "/src/main.py"]
