# Crypto Bot Project

This project is a reinforcement learning trading agent (trading agent back-end repository: https://github.com/roblen001/reinforcement_learning_trading_agent) that integrates a Flask API with a Gatsby-based front-end dashboard. The Flask API scrapes news data and allows the trading agent to operate continuously, while the front-end dashboard provides a real-time view of the trading activities.

![image](https://github.com/user-attachments/assets/1a783ba0-6352-4573-9602-76e089a6c9c9)

## Overview

This project is designed to run on a Raspberry Pi 24/7, scraping news data and enabling continuous trading. The front-end dashboard, which can be started with `gatsby develop`, provides a visual interface for monitoring the bot's trading performance.

## Quick Start with Docker

To quickly start the project using Docker, follow these steps from the root directory of the project:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/roblen001/Crypto-Bot.git
   ```
2.    ```bash
   cd Crypto-Bot
   ```
3. **Build Docker Image**:

   ```bash
   docker build --no-cache -t gatsby-flask-app .
   ```

4. **Run Docker Container**:

   ```bash
   docker run -p 5000:5000 -p 8000:8000 gatsby-flask-app
   ```
5. Head to http://localhost:8000/ on your favorite browser

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
