from flask import Flask, render_template, request
from stat_scraper import player_stat_display
from cache import get_dataframe, set_dataframe

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
    name = request.args.get('name')
    df = get_dataframe(key)
    if df is None:
        df = player_stat_display(category)
        df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('player_templates/player_stats.html', dataframe=df_html, name=name)

@app.route('/squad')
def squad():
    #stat_scraper(selected_stat)
    #df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('squad_stat_select.html')

if __name__ == '__main__':
    app.run(debug=True)
