from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h2>✅ Flask is working perfectly with Python 3.11!</h2>"

if __name__ == "__main__":
    app.run(debug=True, port=5050)
