from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Olá, mundo do Flask com Oryum!"

if __name__ == "__main__":
    app.run(debug=True)
