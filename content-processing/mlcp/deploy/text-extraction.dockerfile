# Use the latest Python image with a specified platform
FROM --platform=linux/amd64 python:3.10

# Update the package repository
RUN apt-get update

# Install necessary packages
# for cv2
RUN apt-get install -y libgl1-mesa-glx
# for pdf processing
RUN apt-get install -y poppler-utils
# tesseract
RUN apt-get install -y \
    curl \
    libtesseract-dev \
    libleptonica-dev \
    tesseract-ocr \
    tesseract-ocr-eng
# process office documents
RUN apt-get update && apt-get install -y --no-install-recommends libreoffice-writer

# install python dependencies
RUN pip3 install boto3==1.28.68
RUN pip3 install botocore==1.31.68
RUN pip3 install matplotlib==3.8.0
RUN pip3 install networkx==3.2
RUN pip3 install numpy==1.24.3
RUN pip3 install opencv_python==4.7.0.72
RUN pip3 install pandas==2.1.3
RUN pip3 install pdf2image==1.16.3
RUN pip3 install pdfplumber==0.10.3
RUN pip3 install Pillow==10.1.0
RUN pip3 install psutil==5.9.5
RUN pip3 install pypdf==3.17.1
RUN pip3 install pytesseract==0.3.10
RUN pip3 install python_dateutil==2.8.2
RUN pip3 install reportlab==4.0.7
RUN pip3 install fpdf==1.7.2

# Copy the source code into the container
COPY /src /src
RUN chmod +x /src/main.py

# Command to run on container start
ENTRYPOINT ["python3", "/src/main.py"]
