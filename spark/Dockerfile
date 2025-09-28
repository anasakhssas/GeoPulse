FROM bitnami/spark:3.4

USER root

# Install Python packages
RUN pip install --no-cache-dir \
    psycopg2-binary \
    watchdog \
    pandas \
    numpy

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

USER 1001