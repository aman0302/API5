from flask import Flask, url_for, request, jsonify
import logging
import datetime
from sqlalchemy.orm import sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import and_
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)
db = SQLAlchemy(app)
Session = sessionmaker(bind=db.engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/articles')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        return "ECHO: NONE"


@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + request.data

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"

    else:
        return "415 Unsupported Media Type"


@app.route('/api/1.0/addUser', methods=['POST'])
def addUser():
    logger.info('addUser invoked')

    #handle bad request / text instead of json add silent in jsonify

    data = request.get_json()
    email, password = data['email'], data['password']
    first_name, last_name = data['first_name'], data['last_name']
    date_format = '%d-%m-%Y'
    date_of_birth = datetime.datetime.strptime(data['date_of_birth'],
                                               date_format)

    user = User(email=email, password=password,
                first_name=first_name, last_name=last_name,
                date_of_birth=date_of_birth)

    session = Session()
    if session.query(User).filter(User.email == email).first() is None:
        session.add(user)
        session.commit()

        logger.info('user with Email {0} added'.format(email))
        return jsonify(status='SUCCESS', msg='User added',
                       data=dict(user_id=user.user_id))
    else:
        logger.info('user with Email {0} already exists'.format(email))
        return jsonify(status='FAILED', msg='User already exists', data=dict())

@app.route('/api/1.0/addHome', methods=['POST'])
def addHome():
    logger.info('addHome invoked')

    data = request.get_json()

    user_id = data['user_id']
    name = data['name']
    latitude, longitude = data['latitude'], data['longitude']


    home = Home(name=name, latitude=latitude, longitude=longitude)
    session = Session()
    session.add(home)
    session.commit()
    #if commit fails ?

    logger.info(home.home_id)

    userHomeLink = UserHomeLink(user_id=user_id, home_id=home.home_id)

    session = Session()
    session.add(userHomeLink)
    session.commit()

    logger.info('home added')
    return jsonify(status='SUCCESS', msg='home added',
                       data=dict(home_id=home.home_id))

@app.route('/api/1.0/addRoom', methods=['POST'])
def addRoom():
    logger.info('addRoom invoked')

    data = request.get_json()

    user_id = data['user_id']
    home_id = data['home_id']
    name = data['name']

    session = Session()
    if session.query(UserHomeLink).filter(and_((UserHomeLink.user_id == user_id),(UserHomeLink.home_id == home_id))).first() is not None:

        room = Room(name=name, home_id=home_id)
        session.add(room)
        session.commit()
        logger.info('room added')
        return jsonify(status='SUCCESS', msg='room added',
                       data=dict(room_id=room.room_id))

    else:

        logger.info('user home combination not found')
        return jsonify(status='FAILED', msg='')

@app.route('/api/1.0/linkDevice', methods=['POST'])
def linkDevice():

    logger.info('linkDevice invoked')

    data = request.get_json()

    user_id = data['user_id']
    home_id = data['home_id']
    room_id = data['room_id']
    device_id = data['device_id']

    session = Session()
    if session.query(UserHomeLink).filter(and_((UserHomeLink.user_id == user_id),(UserHomeLink.home_id == home_id))).first() is not None:
        if ((session.query(Room).filter(Room.room_id == room_id).first() is not None) & (session.query(Device).filter(Device.device_id == device_id).first() is not None)):

            deviceRoomLink = DeviceRoomLink(device_id=device_id, room_id=room_id)
            session.add(deviceRoomLink)
            session.commit()
            logger.info('device linked')
            return jsonify(status='SUCCESS',data=dict(id=deviceRoomLink.id))

        else:
            logger.info('room_id or device_id does not exists')
            return jsonify(status='FAILED', msg='room_id or device_id does not exists')

    else:
        logger.info('user home combination not found')
        return jsonify(status='FAILED', msg='user home combination not found')




@app.route('/api/1.0/addDeviceInfo', methods=['POST'])
def addDeviceInfo():

    logger.info('addDeviceInfo invoked')

    data = request.get_json()

    key = data['key']
    password=data['password']

    config1=""
    if data['config']:
        config1= data['config']

    is_claimed=0
    if 'is_claimed' in data:
        is_claimed= data['is_claimed']

    type=""
    if 'type' in data:
        type= data['type']

    in_topic=""
    if 'in_topic' in data:
        in_topic= data['in_topic']

    config=""
    if 'config' in data:
        config= data['config']

    device = Device(key=key, password=password, config=config1, type=type, is_claimed=is_claimed, in_topic=in_topic)

    session= Session()
    session.add(device)
    session.commit()


    logger.info('device info added')
    return jsonify(status='SUCCESS', msg='device info added',
                       data=dict(device_id=device.device_id))




if __name__ == '__main__':
    app.run(host='0.0.0.0')