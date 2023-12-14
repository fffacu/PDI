# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in tkinter.txt
RUN pip install --trusted-host pypi.python.org -r tkinter.txt

# Make port 9099 available to the world outside this container
EXPOSE 9099

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "cliente.py"]
