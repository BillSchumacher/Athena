# Use the official Python image as the base image
FROM python:3.10

RUN mkdir -p /app

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends pkg-config && \
    apt-get install -y --no-install-recommends build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        libpng-dev \
        libfreetype6-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN  ln -s /usr/include/freetype2/ft2build.h /usr/include/
# Copy the requirements.txt file into the container
COPY requirements.txt .

RUN pip install pytest

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .
RUN pip install -e .
# Expose the port the API will run on
EXPOSE 5000

# Set the default mode to "api"
ENV ATHENA_MODE=api

# Set the entrypoint script
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
