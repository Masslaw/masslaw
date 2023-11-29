# Use the latest Python image with a specified platform
FROM --platform=linux/amd64 python:3.10

# Update the package repository
RUN apt-get update

# Install necessary packages
# --

# install python dependencies
RUN pip3 install boto3==1.28.68
RUN pip3 install botocore==1.31.68
RUN pip3 install gremlinpython==3.7.0
RUN pip3 install matplotlib==3.8.0
RUN pip3 install networkx==3.2
RUN pip3 install numpy==1.24.3
RUN pip3 install pandas==2.1.3
RUN pip3 install Pillow==10.1.0
RUN pip3 install psutil==5.9.5
RUN pip3 install python_dateutil==2.8.2
RUN pip3 install spacy==3.5.4
RUN pip3 install coreferee==1.4.1
RUN python -m spacy download en_core_web_lg
RUN python -m coreferee install en

# Copy the source code into the container
COPY /src /src
COPY /some_text.txt /some_text.txt
COPY /process_configuration.json /process_configuration.json
RUN chmod +x /src/main.py

# Command to run on container start
ENTRYPOINT ["python3", "/src/main.py"]
