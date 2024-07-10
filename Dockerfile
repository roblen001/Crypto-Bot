# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies including bash and necessary libraries for Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    bash \
    libnss3 \
    libgconf-2-4 \
    libxi6 \
    libgbm1 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxtst6 \
    libasound2 \
    xdg-utils \
    fonts-liberation \
    libappindicator3-1 \
    lsb-release \
    --no-install-recommends

# Add the Google Chrome repository and install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install the specified version of ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Install Python dependencies
COPY flask-api/requirements.txt /app/flask-api/
RUN pip install --no-cache-dir -r /app/flask-api/requirements.txt

RUN apt-get update && apt-get install -y bash

# Copy the application code into the container
COPY flask-api/src/ /app/flask-api/src

# Copy the output_data directory into the container
COPY output_data /app/output_data

# Install Node.js and Gatsby CLI globally
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g gatsby-cli

# Set the working directory for Gatsby
WORKDIR /app/front-end

# Copy only package.json and package-lock.json first for caching
COPY front-end/package.json front-end/package-lock.json ./

# Install Gatsby dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the Gatsby application code in stages to optimize build caching
COPY front-end/gatsby-browser.js ./
COPY front-end/gatsby-config.js ./
COPY front-end/gatsby-node.js ./
COPY front-end/gatsby-ssr.js ./
COPY front-end/.prettierrc ./
COPY front-end/.prettierignore ./

# Copy the src directory separately
COPY front-end/src ./src

# Copy the public directory separately
COPY front-end/public ./public

# Build the Gatsby site
RUN npm run build

# Expose the ports that the Flask and Gatsby apps run on
EXPOSE 5000 8000

# Copy the start script into the container
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Specify the command to run the start script
CMD ["/app/start.sh"]
