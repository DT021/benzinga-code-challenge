import requests
import json

cookie = False

if cookie:
	balance = cookie.balance
	portfolio = cookie.portfolio
else:
	balance = 100000
	portfolio = []

def get_info(stock):
    """Gets all relevant info for a stock in puts it all into a dictionary
    """
    all_info = requests.get('http://data.benzinga.com/stock/' + stock).json()

    if 'status' in all_info and 'msg' in all_info:
    	return 'Symbol not found'
    
    stock_info = {}
    stock_info['name'] = all_info['name']
    stock_info['symbol'] = all_info['symbol']
    stock_info['name'] = all_info['name']
    stock_info['ask_price'] = all_info['ask']
    stock_info['bid_price'] = all_info['bid']
    stock_info['quantity'] = 0
    return stock_info

def buy_stock(stock_symbol, quantity):
	stock_info = get_info('stock_symbol')
	if balance - stock_info.ask_price * quantity < 0:
		return "Not enough money to perform transaction"
	stock_info['quantity'] += quantity
	balance -= stock_info['ask_price'] * quantity 
	portfolio.append(stock_info)
	

def sell_stock(stock_symbol, quantity):
	stock_info = get_info('stock_symbol')
	if quantity > stock_info['quantity']:
		return "You do not have enough of this stock to sell"
	stock_info['quantity'] -= quantity
	balance += stock_info['bid_price'] * quantity 
	portfolio.append(stock_info)

def get_balance():
	return balance

def get_portfolio():
	return portfolio

print get_info('GOOG')