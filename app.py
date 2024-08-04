from flask import Flask, render_template, request
from stat_scraper import player_stat_display
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player')
def player():
    return render_template('player_templates/player_stat_select.html')

@app.route('/player_stat/')
def player_stat():
    category = request.args.get('category')
    name = request.args.get('name').lower()
    if not os.path.isfile(f'templates/cached_stat_tables/{(name)}.html'):
        df = player_stat_display(category)
        df.to_html(f'templates/cached_stat_tables/{(name)}.html', classes='table table-striped', index=False)
    return render_template('player_templates/player_stats.html', name=name, table_name=f'templates/cached_stat_tables/{name}.html')

@app.route('/squad')
def squad():
    #stat_scraper(selected_stat)
    #df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('squad_stat_select.html')

if __name__ == '__main__':
    app.run(debug=True)
