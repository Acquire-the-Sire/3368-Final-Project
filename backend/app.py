from flask import Flask
from flask import jsonify
from flask import request

from backend.sqlfunc import create_connection
from backend.sqlfunc import execute_read_query
from backend.sqlfunc import execute_query

import credentials

app = Flask(__name__)


@app.route('/api/floor', methods=['GET'])
def return_a_floor():  # this is code from class 5 (line 96) with changed variables
    request_data = request.get_json()
    floorlevel = request_data['level']
    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "select * from floor where level = %s" % floorlevel
    floor = execute_read_query(conn, sql)
    return jsonify(floor)


@app.route('/api/floor', methods=['POST'])
def add_new_floor():  # this is partially code from class 5 (line 106)
    request_data = request.get_json()
    newfloorlevel = request_data['level']
    newfloorname = request_data['name']
    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "insert into floor(level, name) values (%s, '%s')" % (newfloorlevel, newfloorname)

    execute_query(conn, sql)
    return 'Add floor request successful.'


@app.route('/api/floor', methods=['PUT'])
def change_floor_name():  # code from hw2
    request_data = request.get_json()
    level = request_data['level']
    newname = request_data['name']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "UPDATE floor SET name = '%s' WHERE level = %s" % (newname, level)

    execute_query(conn, sql)
    return 'Floor name changed.'


@app.route('/api/floor', methods=['DELETE'])
def remove_floor():  # code from hw2
    request_data = request.get_json()
    level = request_data['level']
    name = request_data['name']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "DELETE FROM floor WHERE level = %s AND name = '%s'" % (level, name)

    execute_query(conn, sql)
    return 'Floor Deleted.'


@app.route('/api/allfloor', methods=['GET'])
def all_floor():
    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "select level from floor"

    floor = execute_read_query(conn, sql)
    return jsonify(floor)


@app.route('/api/allroom', methods=['GET'])
def all_room():  # this is code from class 5 (line 96) with changed variables
    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "select number from room"

    room = execute_read_query(conn, sql)
    return jsonify(room)


@app.route('/api/resident', methods=['GET'])
def return_a_resident():  # this is code from class 5 (line 96) with changed variables
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "select resident.age, room.number from resident join room on room.id = resident.room where firstname = '%s' and lastname = '%s'" % (firstname, lastname)
    resident = execute_read_query(conn, sql)
    return jsonify(resident)


@app.route('/api/resident', methods=['POST'])
def add_new_resident():  # this is partially code from class 5 (line 106)
    request_data = request.get_json()
    newresidentfirst = request_data['firstname']
    newresidentlast = request_data['lastname']
    newresidentage = request_data['age']
    newresidentroom = request_data['room']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = ("insert into resident(firstname, lastname, age, room) values "
           "('%s','%s',%s,(select id from room where number = %s))") % (newresidentfirst, newresidentlast, newresidentage,
                                                                    newresidentroom)

    execute_query(conn, sql)
    return 'Add resident request successful.'


@app.route('/api/resident', methods=['PUT'])
def change_resident_name():  # code from hw2
    request_data = request.get_json()
    newage = request_data['age']
    name = request_data['firstname']
    lname = request_data['lastname']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "UPDATE resident SET age = %s WHERE firstname = '%s' and lastname = '%s'" % (newage, name, lname)

    execute_query(conn, sql)
    return 'Resident age changed.'


@app.route('/api/resident', methods=['DELETE'])
def remove_resident():  # code from hw2
    request_data = request.get_json()
    residentfirst = request_data['firstname']
    residentlast = request_data['lastname']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "DELETE FROM resident WHERE firstname = '%s' and lastname = '%s'" % (
    residentfirst, residentlast)

    execute_query(conn, sql)
    return 'Resident removed.'


@app.route('/api/room', methods=['GET'])
def return_a_room():  # this is code from class 5 (line 96) with changed variables
    request_data = request.get_json()
    roomnum = request_data['number']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "SELECT room.capacity, floor.level FROM room JOIN floor ON room.floor = floor.id WHERE room.number = %s" % roomnum

    room = execute_read_query(conn, sql)
    return jsonify(room)


@app.route('/api/room', methods=['POST'])
def add_new_room():  # this is partially code from class 5 (line 106)
    request_data = request.get_json()
    newcapacity = request_data['capacity']
    newnumber = request_data['number']
    newfloor = request_data['floor']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = ("insert into room(capacity, number, floor) values "
           "(%s,%s,(select id from floor where level = %s))") % (newcapacity, newnumber, newfloor)

    execute_query(conn, sql)
    return 'Add room request successful.'


@app.route('/api/room', methods=['PUT'])
def change_room_num():  # code from hw2
    request_data = request.get_json()
    newnum = request_data['number']
    oldnum = request_data['old_number']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "UPDATE room SET number = %s WHERE number = %s" % (newnum, oldnum)

    execute_query(conn, sql)
    return 'Room number changed.'


@app.route('/api/room', methods=['DELETE'])
def remove_room():  # code from hw2
    request_data = request.get_json()
    requestnumber = request_data['number']
    level = request_data['level']

    myCreds = credentials.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    sql = "DELETE FROM room WHERE number = %s and floor = (select id from floor where level = %s)" % (requestnumber, level)

    execute_query(conn, sql)
    return 'Room removed.'


if __name__ == '__main__':
    app.run()
