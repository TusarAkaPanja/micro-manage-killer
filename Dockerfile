FROM python:3.11-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-utils \
    xdotool \
    scrot \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxcb1 \
    wget \
    gnupg2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome (required for website opening)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY auto_clicker.py .

# Create a script to run Xvfb and then launch the auto clicker
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1280x720x16 &\n\
export DISPLAY=:99\n\
python auto_clicker.py\n\
' > /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Set display environment variable
ENV DISPLAY=:99

# Run the script
CMD ["/app/entrypoint.sh"] 