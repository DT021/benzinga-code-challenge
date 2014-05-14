from flask import Flask, render_template, session, request, jsonify, abort, redirect, url_for
import transactions
import requests
import json

app = Flask(__name__)

@app.route('/')
def main():
    session['cache'] = 100000

    return render_template('index.html')

@app.route('/transaction', methods=['POST'])
def transaction():
    error = None
    if requests.method == 'GET':
        quantity = request.form['quantity']
        stock_symbol = request.form['stock_symbol']
        if request.form['action'] == 'buy':
            transactions.buy_stock(stock_symbol, quantity)
        if request.form['action'] == 'sell':
            transactions.sell_stock(stock_symbol, quantity)
    return

@app.route('/lookup', methods=['GET'])
def lookup():
    # error = None
    # if requests.method == 'GET':

    return redirect(url_for('main'))

@app.route('/stocks/<stock>')
def stocks(stock):
    return jsonify(transactions.get_info(stock))

app.secret_key = 'benzinga'
if __name__ == '__main__':
    app.run(debug=True)