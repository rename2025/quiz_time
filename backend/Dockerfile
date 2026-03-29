FROM python:3.13-slim

# Setenvironment variabls

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ON_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1


# Install System dependenices

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# cerate app directory

WORKDIR /app

#copy riquarments and install python dependecise

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# copy project files

COPY . .
#Make entrypoint exeuteble


RUN chmod +x entrypoint.sh

# Create no-root user

RUN adduser -disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Entrypoint

ENTRYPOINT ["./entrypoint.sh"]



















