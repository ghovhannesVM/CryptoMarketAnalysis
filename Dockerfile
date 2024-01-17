FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run data_collector.py when the container launches
CMD ["python3", "data_collector.py"]

#CMD ["python3", "script2.py"]
