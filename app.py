# import stat_scraper as ss
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player')
def player():
    return render_template('player_stat_select.html')

@app.route('/squad')
def squad():
    return render_template('squad_stat_select.html')


if __name__ == '__main__':
    app.run(debug=True)
