# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose Flask default port
EXPOSE 5000
# Run with Gunicorn WSGI server (production-like)
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "app:app"]
