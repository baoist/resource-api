from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/foo")
def foo():
    return "Goodbye World!"

@app.route("/bar")
def bar():
    return "Goodbye World!"

@app.route("/wib")
def wib():
    return "Goodbye World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
