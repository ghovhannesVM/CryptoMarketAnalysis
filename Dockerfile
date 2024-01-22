FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Run main.py when the container launches
ENTRYPOINT ["python3", "src/main.py"]
