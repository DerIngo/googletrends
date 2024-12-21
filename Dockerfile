# syntax=docker/dockerfile:1.4

# Build-Stage für Python-Dependencies
FROM python:3.12-slim-bullseye AS builder

WORKDIR /app
COPY requirements.txt .

# Nutzung des pip-Cache für schnellere Builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Finale Stage
FROM python:3.12-slim-bullseye

# Vermeidet Interaktive Dialoge während der Installation
ENV DEBIAN_FRONTEND=noninteractive

# System-Pakete installieren
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libglib2.0-0 \
    libfontconfig \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    locales && rm -rf /var/lib/apt/lists/*

# Deutsche Locale generieren und setzen
RUN echo "de_DE.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=de_DE.UTF-8

# Umgebungsvariable setzen
ENV LANG=de_DE.UTF-8 \
    LANGUAGE=de_DE:de \
    LC_ALL=de_DE.UTF-8

# Chrome in separatem Layer installieren
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver installation using webdriver-manager
RUN pip install webdriver-manager

# Python-Pakete von der Builder-Stage kopieren
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Test-Skript anpassen
COPY test_python.py .

# Healthcheck hinzufügen
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from selenium import webdriver; from selenium.webdriver.chrome.options import Options; options = Options(); options.add_argument('--headless'); driver = webdriver.Chrome(options=options); driver.quit()"

# Nicht-Root-Benutzer für bessere Sicherheit
RUN useradd -m -s /bin/bash selenium
USER selenium

CMD ["python", "test_selenium.py"]