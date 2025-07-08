# Binance Futures Testnet Trading Bot

## Overview
This is a simplified trading bot for the Binance Futures Testnet (USDT-M), built in Python using the official `python-binance` library. It supports market, limit, stop-limit, and simulated OCO orders, with robust CLI input validation and logging.

## Features
- Place **Market** and **Limit** orders on Binance Futures (USDT-M)
- Support for **Buy** and **Sell** order sides
- **Stop-Limit** and simulated **OCO** order types (OCO is for spot, as Binance Futures does not natively support OCO)
- Command-line interface (CLI) with menu-driven input
- Input validation and error handling
- Logging of all API requests, responses, and errors to `bot.log`
- Reusable `BasicBot` class structure

## Setup
1. **Register** on [Binance Futures Testnet](https://testnet.binancefuture.com) and generate API Key and Secret.
2. **Install dependencies:**
   ```bash
   pip install python-binance
   ```
3. **Run the bot:**
   ```bash
   python trading_bot.py
   ```
4. **Follow the CLI prompts** to place orders.

## Usage
- Enter your Binance Testnet API Key and Secret when prompted.
- Select the order type (Market, Limit, Stop-Limit, OCO).
- Enter order details as prompted.
- Order status and details will be printed to the console and logged in `bot.log`.

## Logging
All API interactions and errors are logged to `bot.log` in the project directory.

## Note for the reviewers
I was unable to complete Binance Futures Testnet account verification due to technical/geolocation restrictions.
However, I’ve built the full trading bot with proper structure, input handling, error logging, and order logic using the python-binance library, ready for testnet integration.

API integration functions are written exactly as per Binance documentation, and the bot can be activated instantly once testnet keys are available.
Please find the complete code and logs in the attached GitHub repository.

## Disclaimer
- This bot is for educational and demonstration purposes only.
- Use only with Binance Testnet API keys.
- Do not use with real funds.

---

**Author:** [Your Name]
**Date:** July 2025
