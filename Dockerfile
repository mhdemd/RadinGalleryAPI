# Dockerfile
FROM python:3.12-slim


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --default-timeout=120 --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
