# 1. Build the React app
FROM node:16 as build-stage
RUN mkdir -p /app
WORKDIR /app
COPY ./athena-app/package*.json ./
RUN npm install
COPY ./athena-app/ ./
RUN npm run build


# Set up Nginx to serve the React app
FROM nginx:1.19 as nginx-stage
COPY --from=build-stage /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf


# Use the official Python image as the base image
FROM python:3.10 as python-stage


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

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 4. Copy the API code
COPY athena /app/athena
COPY plugins /app/plugins