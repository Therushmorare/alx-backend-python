# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app source code
COPY . .

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django app on all network interfaces
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

