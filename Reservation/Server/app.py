from flask import Flask, jsonify, request, abort
import mysql.connector
import hashlib
from datetime import datetime
import hashlib
import random

app = Flask(__name__)

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database = "users"
    )
    
def checkToken(account,token):
    cursor = mydb.cursor()    
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    result = False
    for member in tokens_list:
        if account == member[0].lower():
            if token == member[1]:
                result = True
    cursor.close()            
    return result


#Retrieve a random joke from all jokes in the database
@app.route('/restrv1/login/get_nonce/<string:username>', methods=['GET'])
def get_nonce(username):
    nonce =  ''.join([str(random.randint(0, 9)) for i in range(8)])
    cursor = mydb.cursor()
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    sql = "INSERT INTO login_session (nonce,timestamp,username) VALUES (%s,%s,%s)"
    val = (nonce,timestamp,username)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return jsonify({'nonce': nonce})
    
@app.route('/restrv1/get_restaurant', methods=['GET'])
def get_restaurants():
    restaurants=[]
    cursor = mydb.cursor()
    cursor.execute("SELECT restaurant_name,address FROM restaurants")
    restaurant_list = cursor.fetchall()
    for member in restaurant_list:
        restaurant={
            'name': member[0],
            'address': member[1]
        }
        restaurants.append(restaurant)
    cursor.close()
    return jsonify(restaurants),200
    
@app.route('/restrv1/<string:res_name>/timeslots', methods=['GET'])
def get_restaurant_timeslot(res_name):
    timeslots=[]
    cursor = mydb.cursor();
    table = res_name+"_timeslot"
    cursor.execute("SELECT timeslot,available FROM {}".format(table))
    timeslot_list = cursor.fetchall()
    for member in timeslot_list:
        timeslot={
            'timeslot': member[0],
            'available': member[1]
        }
        timeslots.append(timeslot)
    cursor.close()
    return jsonify(timeslots),200

@app.route('/restrv1/<string:res_name>/booking', methods=['PUT'])
def book(res_name):
    cursor = mydb.cursor()
    name = request.json["name"]
    timeslot = request.json["timeslot"]
    seats = request.json["seats"]
    
    print(name)
    print(timeslot)
    print(seats)
    table = res_name+"_timeslot"
    booking = res_name+"_book"
    cursor.execute("SELECT timeslot,available FROM {}".format(table))
    timeslot_list = cursor.fetchall()
    for member in timeslot_list:
        if timeslot == member[0]:
            if int(seats) > member[1]:
                abort(422)
            else:
                new_available = member[1] - int(seats)
                sql = "UPDATE {} SET available = {} WHERE timeslot = '{}'".format(table,new_available,timeslot)
                cursor.execute(sql)
                mydb.commit()
                
                
    sql = "INSERT INTO {} (customer,timeslot,seats) VALUES (%s,%s,%s)".format(booking)
    val = (name,timeslot,seats)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return jsonify({'status':'ok'}),200
    
@app.route('/restrv1/<string:account>/<string:token>/available', methods=['GET'])
def get_availability(account,token):
    
    cursor = mydb.cursor()
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    for member in tokens_list:
        if account == member[0].lower():
            if token != member[1]:
                abort(401)
                
    account_timeslot = account+"_timeslot"
    cursor.execute("SELECT timeslot,available FROM {}".format(account_timeslot))
    
    timeslots = cursor.fetchall()
    
    timeframes=[]
    
    for timeslot in timeslots:
        timeframe = {
            'timeslot': timeslot[0],
            'available': timeslot[1]
        }
        timeframes.append(timeframe)
    cursor.close()
    return jsonify(timeframes),200
    
@app.route('/restrv1/<string:account>/<string:token>/customers', methods=['GET'])
def get_booking(account,token):
        
    cursor = mydb.cursor()
    
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    for member in tokens_list:
        if account == member[0].lower():
            if token != member[1]:
                abort(401)
    
    account_book = account+"_book"
    cursor.execute("SELECT customer,timeslot,seats FROM {}".format(account_book))
    
    timeslots = cursor.fetchall()
    
    customers=[]
    
    for member in timeslots:
        customer = {
            'customer': member[0],
            'timeslot': member[1],
            'seats': member[2]
        }
        customers.append(customer)
    cursor.close()
    return jsonify(customers),200
    
@app.route('/restrv1/<string:account>/<string:token>/addSlot', methods=['PUT'])
def add_slot(account,token):
    cursor = mydb.cursor()
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    for member in tokens_list:
        if account == member[0].lower():
            if token != member[1]:
                abort(401)
        
    timeslot = request.json['timeslot']
    available = request.json['available']
    
    account_timeslot = account+"_timeslot"
    sql = "INSERT INTO {} (timeslot,available) VALUES (%s,%s)".format(account_timeslot)
    val = (timeslot,available)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    return jsonify({'status': "ok"}),200

@app.route('/restrv1/<string:account>/<string:token>/delete/booking', methods=['DELETE'])
def delete_booking(account,token):
    cursor = mydb.cursor()
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    for member in tokens_list:
        if account == member[0].lower():
            if token != member[1]:
                abort(401)
        
    customer = request.json['customer']
    timeslot = request.json['timeslot']
    
    booking = account+"_book"
    sql = "DELETE FROM {} WHERE timeslot = '{}', customer='{}'".format(booking,timeslot, name)
    cursor.execute(sql)
    mydb.commit()
    cursor.close()
    return jsonify({'status': "ok"}),200    
    
@app.route('/restrv1/<string:account>/<string:token>/delete', methods=['DELETE'])
def delete_slot(account,token):
    cursor = mydb.cursor()
    cursor.execute("SELECT login_info.username, login_token.token FROM login_info, login_token WHERE login_token.res_id = login_info.res_id")
    tokens_list = cursor.fetchall()
    
    for member in tokens_list:
        if account == member[0].lower():
            if token != member[1]:
                abort(401)
        
    timeslot = request.json['timeslot']
    
    
    account_timeslot = account+"_timeslot"
    sql = "DELETE FROM {} WHERE timeslot = '{}'".format(account_timeslot,timeslot)
    cursor.execute(sql)
    mydb.commit()
    cursor.close()
    return jsonify({'status': "ok"}),200
    
@app.route('/restrv1/login', methods=['PUT'])
def receive_login():
    
    username=request.json['username']
    
    cnonce=request.json['cnonce']
    
    hash=request.json['hash']

    cursor = mydb.cursor()
    
    cursor.execute("SELECT username FROM login_session")
    
    usrs_list = cursor.fetchall()
    
    usrs = []
    for usr in usrs_list:
        usrs.append(usr[0])
    
    if username not in usrs:
        abort(401)
    salt = "_76dwDOPNiui"
    cursor.execute("SELECT login_info.username, login_info.password, login_session.nonce FROM login_session, login_info WHERE login_info.username = login_session.username")

    accounts = cursor.fetchall()
    
    hashed_pwd= None
    
    for account in accounts:
        if username == account[0]:
            password = account[1] + cnonce + account[2]
            hashed_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    if hashed_pwd != hash:
        abort(401)
    
    log = open("log.txt","a")
    current = datetime.now().strftime('%Y-%m-%d %H:%M')
    login = username+"\t"+hashed_pwd+"\n"+hash+"\n" 
    content = current + "\t" + login + "\n"
    log.write(content)
    log.close()
    
    cursor.execute("SELECT login_info.username, restaurants.restaurant_name, login_info.res_id FROM login_info, restaurants WHERE login_info.res_id = restaurants.id")
    
    restaurants = cursor.fetchall()
    res_name = None
    res_id = None
    for restaurant in restaurants:
        if username == restaurant[0]:
            res_name = restaurant[1]
            res_id = restaurant[2]
            
    token =  ''.join([str(random.randint(0, 9)) for i in range(8)])
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    
    cursor.execute("SELECT res_id FROM login_token")
    sessions = cursor.fetchall()
    res_ids = []
    for session in sessions:
        res_ids.append(session[0])
        
    if res_id not in res_ids:
        sql = "INSERT INTO login_token (token,timestamp,res_id) VALUES (%s,%s,%s)"
        val = (token,timestamp,res_id)
        cursor.execute(sql, val)           
        mydb.commit()
    else:
        sql = "UPDATE login_token SET token = {}, timestamp = {} WHERE res_id={}".format(token,timestamp,res_id)
        cursor.execute(sql)
        mydb.commit()
    
        
    cursor.close()       
    return jsonify({'name':res_name, 'token': token}),200
    
if __name__ == '__main__':

    app.run(debug=True)
