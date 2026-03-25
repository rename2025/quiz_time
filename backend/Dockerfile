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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# cerate app directory

WORKDIR / app

#copy riquarments and install python dependecise

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files

COPY .. .

#Make entrypoint exeuteble

RUN chomd +x entrypoint.hs

# Create no-root user

RUN adduser -disabeled-password --gecos '' appuser && \
    chown -R appuser:appuser / app \
USER appuser

# Entrypoint

ENTRYPOINT ["./entrypoint.sh"]



















