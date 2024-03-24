from flask import Flask
app = Flask(__name__)

@app.route("/ping", methods=['GET'])#엔드포인트 로
def ping():
    return "pong"