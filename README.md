# Crypto Bot Project

This project is a reinforcement learning trading agent that integrates a Flask API with a Gatsby-based front-end dashboard. The Flask API scrapes news data and allows the trading agent to operate continuously, while the front-end dashboard provides a real-time view of the trading activities.

![Project Image](https://user-images.githubusercontent.com/51753527/147854745-9ec9bac7-174a-4328-a6ab-7ded6c47893c.png)

## Quick Start with Docker

To quickly start the project using Docker, follow these steps from the root directory of the project:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/roblen001/Crypto-Bot.git
    ```

2. **Build Docker Image**:
    ```bash
    docker build -t gatsby-flask-app .
    ```

3. **Run Docker Container**:
    ```bash
    docker run -p 5000:5000 -p 8000:8000 gatsby-flask-app
    ```

### What the Docker Image Does

The Docker image is configured to:

1. **Use the Official Python Image**: 
    ```dockerfile
    FROM python:3.9-slim
    ```

2. **Set the Working Directory**: 
    ```dockerfile
    WORKDIR /app
    ```

3. **Install Dependencies**: 
    ```dockerfile
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
    ```

4. **Install Google Chrome and ChromeDriver**: 
    ```dockerfile
    RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
        apt-get update && \
        apt-get install -y google-chrome-stable

    RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip && \
        unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
        mv /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
        chmod +x /usr/local/bin/chromedriver && \
        rm /tmp/chromedriver.zip
    ```

5. **Install Python Dependencies**: 
    ```dockerfile
    COPY flask-api/requirements.txt /app/flask-api/
    RUN pip install --no-cache-dir -r /app/flask-api/requirements.txt
    ```

6. **Copy Application Code**: 
    ```dockerfile
    COPY flask-api/src/ /app/flask-api/src
    COPY output_data /app/output_data
    ```

7. **Install Node.js and Gatsby CLI**: 
    ```dockerfile
    RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
        apt-get install -y nodejs && \
        npm install -g gatsby-cli
    ```

8. **Set Up Gatsby Front-End**: 
    ```dockerfile
    WORKDIR /app/front-end
    COPY front-end/package.json front-end/package-lock.json ./
    RUN npm install --legacy-peer-deps
    COPY front-end/gatsby-browser.js ./
    COPY front-end/gatsby-config.js ./
    COPY front-end/gatsby-node.js ./
    COPY front-end/gatsby-ssr.js ./
    COPY front-end/.prettierrc ./
    COPY front-end/.prettierignore ./
    COPY front-end/src ./src
    COPY front-end/public ./public
    RUN npm run build
    ```

9. **Expose Ports**: 
    ```dockerfile
    EXPOSE 5000 8000
    ```

10. **Set Up Start Script**: 
    ```dockerfile
    COPY start.sh /app/start.sh
    RUN chmod +x /app/start.sh
    CMD ["/app/start.sh"]
    ```

## Overview

This project is designed to run on a Raspberry Pi 24/7, scraping news data and enabling continuous trading. The front-end dashboard, which can be started with `gatsby develop`, provides a visual interface for monitoring the bot's trading performance.

### Project Structure

- `flask-api/`: Contains the backend Flask API for scraping news and running the trading bot.
- `front-end/`: Contains the Gatsby-based front-end for the trading dashboard.
- `strategy_testing/`: Contains data and scripts for testing various trading strategies.

## Modifying the Flask App

The Flask app is located in the `flask-api/src/app/` directory. Here are the key components and how you can modify them:

### Key Components

- `app.py`: The main application file where the Flask app is initialized and routes are defined.
- `run_all_news_scraper.py`: Script to scrape all news data.
- `run_top_news_scraper.py`: Script to scrape top news data.
- `run_trading_bot.py`: Script to run the trading bot.
- `config.py`: Configuration file for the Flask app.

### How to Modify

1. **Add New Routes**: To add new routes, edit `app.py` and define new Flask routes as needed.
2. **Update Scraping Logic**: Modify `run_all_news_scraper.py` or `run_top_news_scraper.py` to change how news data is scraped.
3. **Adjust Trading Logic**: Update `run_trading_bot.py` to alter the bot's trading behavior.

## Modifying the UI Trading Dashboard

The front-end dashboard is located in the `front-end/` directory. It uses Gatsby to create a dynamic web interface.

### Key Components

- `src/pages/`: Contains the main pages of the dashboard.
- `src/components/`: Contains React components used throughout the dashboard.
- `gatsby-config.js`: Configuration file for the Gatsby site.
- `gatsby-node.js`: Custom Node.js scripts for Gatsby.

### How to Modify

1. **Update UI Components**: Edit files in `src/components/` to change the look and feel of the dashboard components.
2. **Add New Pages**: Create new pages in `src/pages/` to add new sections to the dashboard.
3. **Modify Configuration**: Update `gatsby-config.js` and `gatsby-node.js` to change site settings and add custom Node.js functionality.

## Modifying and Running Individual Components of The Project

I highly encourage people to dig in and modify the app and the strategies. I encourage you to use the trained models from my reinforcement learning trading agent in this project to easily put it into production and manage its trading ability.

### Prerequisites

- Python 3.x
- Node.js and npm
- Gatsby CLI
- Docker

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/roblen001/Crypto-Bot.git
    ```

2. **Set Up Flask API**:
    ```bash
    cd flask-api
    pip install -r requirements.txt
    ```

3. **Set Up Front-End**:
    ```bash
    cd ../front-end
    npm install
    ```

### Running the Project without Docker

1. **Start Flask API**:
    ```bash
    cd flask-api/src/app
    python app.py
    ```

2. **Start Front-End**:
    ```bash
    cd front-end
    gatsby develop
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
