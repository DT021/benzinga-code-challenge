from flask import Flask, render_template, session
import requests

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')
    # return urllib2.urlopen('http://data.benzinga.com/stock/F')

if __name__ == '__main__':
    app.run(debug=True)