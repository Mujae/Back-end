from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1#동시에 많은 접속이 발생하면 문제가 생길 수 있음 -> atomic increment operation 알아볼 것.

@app.route("/ping", methods=['GET'])#엔드포인트
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count+1

    return jsonify(new_user)

