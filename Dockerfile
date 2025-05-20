# Use an appropriate version of Python (e.g., Python 3.9)
FROM python:3.9-slim

# Install system dependencies for OpenCV and other requirements
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean
    
# Set the working directory
WORKDIR /app

# Copy the requirements.txt into the container
COPY . .

# Install necessary dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary ports for the services
EXPOSE 5002

VOLUME ["/app/images/"]

# Set main.py as the entry point to run all the scripts
CMD ["python", "app.py"]