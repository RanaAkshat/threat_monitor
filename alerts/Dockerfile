# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the alerts directory content into the container
COPY . .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# Run the alert script
CMD ["python", "alert_system.py"]
