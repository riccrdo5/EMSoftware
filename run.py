from flask import Flask, url_for, render_template


app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

app.run(debug=True)