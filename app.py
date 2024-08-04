from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Import routes after the app is defined
import routes

if __name__ == '__main__':
    app.run(debug=True)
