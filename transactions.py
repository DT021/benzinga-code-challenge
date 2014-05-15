import requests
from flask import session, flash, redirect, url_for

def get_info(stock):
    """Gets all relevant info for a stock in puts it all into a dictionary"""
    all_info = requests.get('http://data.benzinga.com/stock/' + stock).json()

    if 'status' in all_info and 'msg' in all_info:
        flash("Stock symbol not found!", "danger")
        return redirect(url_for('main'))
    
    stock_info = {}
    stock_info['name'] = all_info['name']
    stock_info['symbol'] = all_info['symbol']
    stock_info['ask_price'] = all_info['ask']
    stock_info['bid_price'] = all_info['bid']
    stock_info['quantity'] = 0
    return stock_info

def get_current_quantity(stock_symbol):
    for stock in session['inventory']:
        if stock[1] == stock_symbol:
            return stock[2]
    return 0

def set_info(stock_name, stock_symbol, current_quantity, ask_price):
    found = False
    for i in range(len(session['inventory'])):
        stock = session['inventory'][i]
        if stock[1] == stock_symbol:
            found = True
            if ask_price == -1:
                ask_price = stock[3]
            if current_quantity == 0:
                session['inventory'].remove(stock)
            else:
                session['inventory'][i] = (stock_name, stock_symbol, current_quantity, ask_price)
    if not found:
        session['inventory'].append((stock_name, stock_symbol, current_quantity, ask_price))


    

def buy_stock(stock_symbol, quantity):
    stock_info = get_info(stock_symbol)
    current_quantity = get_current_quantity(stock_symbol)
    quantity = int(quantity)
    stock_info['ask_price'] = float(stock_info['ask_price'])
    if session['balance'] - stock_info['ask_price'] * quantity < 0:
        flash("Not enough money to complete transaction!", "danger")
        return redirect(url_for('main'))
    current_quantity += quantity
    session['balance'] -= stock_info['ask_price'] * quantity
    set_info(stock_info['name'], stock_symbol, current_quantity, stock_info['ask_price'])
    flash("Transaction successful!", "success")
    return redirect(url_for('main'))

def sell_stock(stock_symbol, quantity):
    stock_info = get_info(stock_symbol)
    current_quantity = get_current_quantity(stock_symbol)
    quantity = int(quantity)
    stock_info['bid_price'] = float(stock_info['bid_price'])
    if quantity > current_quantity:
        flash("Not enough stock to sell!", "danger")
        return redirect(url_for('main'))
    current_quantity -= quantity
    session['balance'] += stock_info['bid_price'] * quantity 
    set_info(stock_info['name'], stock_symbol, current_quantity, -1)
    flash("Transaction successful!", "success")
    return redirect(url_for('main'))
