import flask

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    print ("Request received")
    return "Hello World"

app.run(debug=True)