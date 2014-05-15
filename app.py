from flask import Flask, render_template, session, request, jsonify, redirect, url_for
import transactions

app = Flask(__name__)

@app.route('/')
def main(balance=None, inventory=None, selected=None):
    if 'balance' not in session and 'inventory' not in session:
        session['balance'] = 100000
        session['inventory'] = []
    return render_template('index.html', balance=session['balance'], inventory=session['inventory'], selected=selected)

# Handles buying and selling of stocks
@app.route('/transaction', methods=['POST'])
def transaction():
    if request.method == 'POST':
        quantity = request.form['quantity']
        stock_symbol = request.form['stock_symbol']
        if request.form['action'] == 'buy':
            transactions.buy_stock(stock_symbol, quantity)
        if request.form['action'] == 'sell':
            transactions.sell_stock(stock_symbol, quantity)
    return redirect(url_for('main'))

# Lookup search button
@app.route('/lookup', methods=['POST'])
def lookup():
    if request.method == 'POST':
        stock_symbol_lookup = request.form['stock_symbol_lookup']
        stock_info = transactions.get_info(stock_symbol_lookup)
    return render_template('index.html', balance=session['balance'], inventory=session['inventory'], selected=stock_info)

# View stock button
@app.route('/viewstock/<stock>')
def viewstock(stock):
    stock_info = transactions.get_info(stock)
    return render_template('index.html', balance=session['balance'], inventory=session['inventory'], selected=stock_info)

# Testing stock api
@app.route('/stocks/<stock>')
def stocks(stock):
    return jsonify(transactions.get_info(stock))

# Formats the current cash balance
@app.template_filter('format_balance')
def format_balance(value):
    return "${:,.2f}".format(value)

app.secret_key = 'benzinga'
if __name__ == '__main__':
    app.run(debug=True)