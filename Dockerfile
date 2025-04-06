# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Fira Code font
RUN mkdir -p /app/app/static/fonts \
    && wget https://github.com/tonsky/FiraCode/releases/download/6.2/Fira_Code_v6.2.zip -O /tmp/fira_code.zip \
    && unzip /tmp/fira_code.zip -d /tmp/fira_code \
    && cp /tmp/fira_code/ttf/FiraCode-Regular.ttf /app/app/static/fonts/ \
    && rm -rf /tmp/fira_code*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]