from flask import Flask, escape, request
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'mydb.db'


@app.route('/student', methods=['POST'])
def	create_student():
    data = request.get_data().decode("utf-8")
    name = json.loads(data)["name"]

    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("INSERT INTO student (name,addr,city,pin) VALUES (?,?,?,?)",(name, '', '', ''))
    sqliteDB.commit()
    cur.execute(f"select max(id) from student")
    result = cur.fetchall()
    cur_id = result[0][0]
    sqliteDB.close()

    return {
        "id": cur_id, 
        "name": name
    }, 201


@app.route('/student/<id>', methods=['GET'])
def	get_student(id):
	
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute(f"select * from student where id = {id}")
    result = cur.fetchall();
    sqliteDB.close()
    name = result[0][1]
            
    return {
        "id": id, 
        "name":name
    }, 201
	

@app.route('/class', methods=['POST'])
def	create_class():
    data = request.get_data().decode("utf-8")
    name = json.loads(data)["name"]

    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("INSERT INTO clazz (name) VALUES (?)",(name,))
    sqliteDB.commit()
    cur.execute(f"select max(id) from clazz")
    result = cur.fetchall()
    cur_id = result[0][0]
    sqliteDB.close()

    return {
        "id": cur_id, 
        "name": name
    }, 201
	

@app.route('/class/<id>', methods=['GET'])
def	get_class(id):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()

    cur.execute(f"select * from clazz where id = {id}")
    result = cur.fetchall()
    class_name = result[0][1]

    cur.execute(f"select * from classstudent where class_id = {id}")
    result = cur.fetchall()
    student_list = []
    for row in result:
        student_id = row[2]
        cur.execute(f"select * from student where id = {student_id}")
        student = cur.fetchall()
        student_name = student[0][1]
        student_list.append((student_id, student_name))
    sqliteDB.close()

            
    return {
        "id": id, 
        "name": class_name,
        "students": str(student_list)
    }, 201


@app.route('/addstudent', methods=['POST'])
def	add_student_to_class():
	
    data = request.get_data().decode("utf-8")
    json_data = json.loads(data)
    class_id = json_data["class_id"]
    student_id = json_data["student_id"]

    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.cursor()
    cur.execute("INSERT INTO classstudent (class_id, student_id) VALUES (?,?)",(class_id, student_id))
    sqliteDB.commit()

    cur.execute(f"select * from clazz where id = {class_id}")
    result = cur.fetchall()
    class_name = result[0][1]

    cur.execute(f"select * from student where id = {student_id}")
    result = cur.fetchall()
    student_name = result[0][1]

    sqliteDB.close()

    return {
        "id": class_id, 
        "name":class_name,
        "student": [
            {	"student" :{
                "id" : student_id,
                "name" : student_name
                }
            }
            ]
    }, 201