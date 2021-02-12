from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def write_orders():
	# 1. 클라이언트가 준 userName, userPhone, userAddress, orderCount 가져오기.
    userName_receive = request.form['userName_give']
    userPhone_receive = request.form['userPhone_give']
    userAddress_receive = request.form['userAddress_give']
    orderCount_receive = request.form['orderCount_give']

	# 2. DB에 정보 삽입하기
    doc = {
        'userName': userName_receive,
        'userPhone': userPhone_receive,
        'userAddress': userAddress_receive,
        'orderCount': orderCount_receive
    }
    # orders에 review 저장하기
    db.orders.insert_one(doc)

	# 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '주문 완료!'})


@app.route('/order', methods=['GET'])
def read_orders():
    # 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.orders.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)