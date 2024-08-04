from flask import Flask, render_template, request
from stat_scraper import player_stat_display

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
    df = player_stat_display(category)
    df_html = df.to_html(classes='table table-striped', index=False)
    # Render the appropriate template based on the category
    template_map = {
        'stats': 'player_templates/player_standard_stats.html',
        'keepers': 'player_templates/player_goalkeeping.html',
        'keepersadv': 'player_templates/player_advanced_goalkeeping.html',
        'shooting': 'player_templates/player_shooting.html',
        'passing': 'player_templates/player_passing.html',
        'pass_types': 'player_templates/player_pass_types.html',
        'gca': 'player_templates/player_goal_shot_creation.html',
        'defense': 'player_templates/player_defensive_action.html',
        'possession': 'player_templates/player_possession.html',
        'playingtime': 'player_templates/player_playing_time.html',
        'misc': 'player_templates/player_misc_stats.html'
    }

    if category in template_map:
        return render_template(template_map[category], dataframe=df_html)
    else:
        return "Invalid category", 404

@app.route('/squad')
def squad():
    #stat_scraper(selected_stat)
    #df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('squad_stat_select.html')

if __name__ == '__main__':
    app.run(debug=True)
