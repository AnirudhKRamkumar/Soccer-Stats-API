from flask import Flask, render_template, request
import stat_scraper

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/player')
def player():
    return render_template('player_templates/player_stat_select.html')

@app.route('/player_stat/<category>')
def player_stats(category):
    category = request.args.get('category')
    df = stat_scraper(category)
    df_html = df.to_html(classes='table table-striped', index=False)
    if category == 'standard':
        return render_template('player_templates/player_standard_stats.html', dataframe=df_html)
    elif category == 'goalkeeping':
        return render_template('player_templates/player_goalkeeping.html', dataframe=df_html)
    elif category == 'advanced_goalkeeping':
        return render_template('player_templates/player_advanced_goalkeeping.html', dataframe=df_html)
    elif category == 'shooting':
        return render_template('player_templates/player_shooting.html', dataframe=df_html)
    elif category == 'passing':
        return render_template('player_templates/player_passing.html', dataframe=df_html)
    elif category == 'pass_types':
        return render_template('player_templates/player_pass_types.html', dataframe=df_html)
    elif category == 'goal_shot_creation':
        return render_template('player_templates/player_goal_shot_creation.html', dataframe=df_html)
    elif category == 'defensive_action':
        return render_template('player_templates/player_defensive_action.html', dataframe=df_html)
    elif category == 'possession':
        return render_template('player_templates/player_possession.html', dataframe=df_html)
    elif category == 'playing_time':
        return render_template('player_templates/player_playing_time.html', dataframe=df_html)
    elif category == 'misc_stats':
        return render_template('player_templates/player_misc_stats.html', dataframe=df_html)

@app.route('/squad')
def squad():
    #stat_scraper(selected_stat)
    #df_html = df.to_html(classes='table table-striped', index=False)
    return render_template('squad_stat_select.html')

if __name__ == '__main__':
    app.run(debug=True)
