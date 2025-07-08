import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import sys

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.logger = logging.getLogger('BasicBot')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('bot.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            self.logger.info('Connected to Binance Futures Testnet')
        except Exception as e:
            self.logger.error(f'Error connecting to Binance: {e}')
            print(f'Error connecting to Binance: {e}')
            sys.exit(1)

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.logger.info(f'Market order placed: {order}')
            return order
        except BinanceAPIException as e:
            self.logger.error(f'API Error: {e}')
            print(f'API Error: {e}')
        except Exception as e:
            self.logger.error(f'Error: {e}')
            print(f'Error: {e}')
        return None

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            self.logger.info(f'Limit order placed: {order}')
            return order
        except BinanceAPIException as e:
            self.logger.error(f'API Error: {e}')
            print(f'API Error: {e}')
        except Exception as e:
            self.logger.error(f'Error: {e}')
            print(f'Error: {e}')
        return None

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price
            )
            self.logger.info(f'Stop-Limit order placed: {order}')
            return order
        except BinanceAPIException as e:
            self.logger.error(f'API Error: {e}')
            print(f'API Error: {e}')
        except Exception as e:
            self.logger.error(f'Error: {e}')
            print(f'Error: {e}')
        return None

    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        """
        Place an OCO (One Cancels the Other) order on the spot market (Binance Futures does not support OCO natively).
        This is a simulated OCO for demonstration: places a limit and a stop-limit order, and logs both.
        """
        try:
            # Place limit order
            limit_order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            # Place stop-limit order
            stop_limit_order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP_LOSS_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=stop_limit_price,
                stopPrice=stop_price
            )
            self.logger.info(f'OCO order placed: limit={limit_order}, stop_limit={stop_limit_order}')
            return {'limit_order': limit_order, 'stop_limit_order': stop_limit_order}
        except BinanceAPIException as e:
            self.logger.error(f'API Error (OCO): {e}')
            print(f'API Error (OCO): {e}')
        except Exception as e:
            self.logger.error(f'Error (OCO): {e}')
            print(f'Error (OCO): {e}')
        return None

def get_user_input():
    print('--- Binance Futures Trading Bot ---')
    print('Select order type:')
    print('1. Market')
    print('2. Limit')
    print('3. Stop-Limit')
    print('4. OCO (Spot, simulated)')
    order_type_map = {'1': 'market', '2': 'limit', '3': 'stop-limit', '4': 'oco'}
    order_type_choice = input('Enter choice (1-4): ').strip()
    order_type = order_type_map.get(order_type_choice)
    if order_type is None:
        print('Invalid order type.')
        return None
    side = input('Side (buy/sell): ').strip().upper()
    if side not in ['BUY', 'SELL']:
        print('Invalid side.')
        return None
    symbol = input('Symbol (e.g., BTCUSDT): ').strip().upper()
    try:
        quantity = float(input('Quantity: ').strip())
        if quantity <= 0:
            print('Quantity must be positive.')
            return None
    except ValueError:
        print('Invalid quantity.')
        return None
    price = None
    stop_price = None
    stop_limit_price = None
    if order_type == 'limit':
        try:
            price = float(input('Limit Price: ').strip())
            if price <= 0:
                print('Price must be positive.')
                return None
        except ValueError:
            print('Invalid price.')
            return None
    elif order_type == 'stop-limit':
        try:
            stop_price = float(input('Stop Price: ').strip())
            limit_price = float(input('Limit Price: ').strip())
            if stop_price <= 0 or limit_price <= 0:
                print('Prices must be positive.')
                return None
        except ValueError:
            print('Invalid price.')
            return None
        price = (stop_price, limit_price)
    elif order_type == 'oco':
        try:
            price = float(input('OCO Limit Price: ').strip())
            stop_price = float(input('OCO Stop Price: ').strip())
            stop_limit_price = float(input('OCO Stop-Limit Price: ').strip())
            if price <= 0 or stop_price <= 0 or stop_limit_price <= 0:
                print('Prices must be positive.')
                return None
        except ValueError:
            print('Invalid price.')
            return None
        price = (price, stop_price, stop_limit_price)
    return order_type, side, symbol, quantity, price

def main():
    api_key = input('Enter your Binance Testnet API Key: ').strip()
    api_secret = input('Enter your Binance Testnet API Secret: ').strip()
    bot = BasicBot(api_key, api_secret, testnet=True)
    user_input = get_user_input()
    if not user_input:
        print('Invalid input. Exiting.')
        return
    order_type, side, symbol, quantity, price = user_input
    order = None
    if order_type == 'market':
        order = bot.place_market_order(symbol, side, quantity)
    elif order_type == 'limit':
        order = bot.place_limit_order(symbol, side, quantity, price)
    elif order_type == 'stop-limit':
        stop_price, limit_price = price
        order = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
    elif order_type == 'oco':
        limit_price, stop_price, stop_limit_price = price
        order = bot.place_oco_order(symbol, side, quantity, limit_price, stop_price, stop_limit_price)
    if order:
        print('Order placed successfully!')
        print(order)
    else:
        print('Order failed. Check logs for details.')

if __name__ == '__main__':
    main()
