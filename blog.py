#!flask/bin/python
from flask import Flask, jsonify
import mysql.connector as ms
import random
# from flask_wtf import FlaskForm
from flask import request, make_response
import datetime
# conn=''
app = Flask(__name__)
host='localhost'
password='P@ssword123'
user='root'
db='university'
conn=ms.connect(host=host, passwd=password, user=user, database=db)
cursor = conn.cursor()

@app.route('/user/add/', methods=['post'])
# @auth.login_required
def createuser():
    if not request.json:
        # print(request.json)
        print('error')
        # abort(404)
        return make_response({'error': 'no json file found'})
    num = random.randrange(1000000000, 9999999999)
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    user_id =  name[0:3]+str(num)
    email=request.json['email']
    mobile=request.json['mobile']
    password=request.json['password']
    try:
        sql = 'insert into user values(%s,%s,%s,%s,%s,%s)'
        val = (user_id, email, password, first_name, last_name, mobile)
        cursor.execute(sql, val)
        return make_response(jsonify({'success' : True}))
    except Exception as e:
        print(e)
        conn.rollback()
        return make_response(jsonify({'error': 'insertion error', 'success': False}))
    # address = request.json['planid']


@app.route('/user/display/<string:email>', methods=['get'])
# @auth.login_required
def displayUser(email):
    sql = 'select * from user where email = '+ascii(email)
    try:
        cursor.execute(sql)
        ans = {}
        res=cursor.fetchall()
        for row in res:
            ans['userid']=row[0]
            ans['email']=row[1]
            ans['password']=row[2]
            ans['first_name']=row[3]
            ans['last_name']=row[4]
            ans['mobile']=row[5]
            # ans['age']=row[6]
        ans['success']=True
        return make_response(jsonify(ans))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False, 'message':'Can\'t display detail due to internal error'}))

@app.route('/user/login/<string:email>', methods=['get'])
def login(email):
    # email = request.json['email']
    # password = request.json['password']
    try:
        sql = 'select password from user where email = '+ascii(email)
        cursor.execute(sql)
        res = cursor.fetchone()
        return make_response(jsonify({'success': True, 'password': res[0]}))
    except Exception as e:
        print(e)
        return make_response(jsonify({'success': False, 'error': 'not found'}))

if __name__ == '__main__':
    app.run(debug=True)