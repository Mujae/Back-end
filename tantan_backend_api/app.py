from flask import Flask, jsonify, request
from flask.json import JSONEncoder #set자료구조를 JSON으로 변환하려면 원래 되는 list로 바꿔야함

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

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

app.tweets=[]
@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400
    if len(tweet) > 300:
        return '300자를 초과했습니다', 400
    
    user_id = int(payload['id'])
    app.tweets.append({
        'user_id' : user_id,
        'tweet' :tweet
    })

    return '', 200


app.json_encoder = CustomJSONEncoder

@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않음", 400
    
    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않음', 400
    
    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)#여기서 remove를 사용하면 없는 경우 에러가 뜨지만 discard는 없으면 무시함
    
    return jsonify(user)

#트윗기록 엔드포인트
@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return '사용자자가 존재하지 않습니다. 가세요라.', 400
    
    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id':user_id,
        'timeline':timeline
    })