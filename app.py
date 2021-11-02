from flask import Flask, render_template, jsonify, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
import hashlib
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbbook

SECRET_KEY = '18'


@app.route('/')
def home():
    rows = db.articles.find({}, {'id': False})

    return render_template('index.html', rows=rows)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_main')
def login_main():
    rows = db.articles.find({}, {'id': False})
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.bookReview_team.find_one({"id": payload['id']})
        return render_template('main.html', id=user_info["id"], rows=rows)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/joinMem')
def joinMem():
    return render_template('joinMem.html')


@app.route('/join_info', methods=['POST'])
def join_info():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash
    }

    db.bookReview_team.insert(doc)

    return jsonify({'msg': '가입이 되었습니다.'})


@app.route('/logins', methods=['POST'])
def logins():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.bookReview_team.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.bookReview_team.find_one({'id': payload['id']}, {'_id': False})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


@app.route('/memo', methods=['GET'])
def listing():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles': articles})


@app.route('/viewList', methods=['POST'])
def view():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    user_info = db.bookReview_team.find_one({"id": payload["id"]})
    url_receive = request.form['url_give']
    reviewMemo_give = request.form['reviewMemo_give']
    reviewTitle_give = request.form['reviewTitle_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    doc = {
        'id': user_info['id'],
        'title': title,
        'image': image,
        'desc': desc,
        'url': url_receive,
        'reviewMemo': reviewMemo_give,
        'reviewTitle': reviewTitle_give
    }

    db.articles.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
