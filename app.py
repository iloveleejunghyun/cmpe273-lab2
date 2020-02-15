from flask import Flask, escape, request
import sqlite3
import json

app = Flask(__name__)

DB = {
	"students": [],
	"classes": []
}

DATABASE = 'mydb.db'

@app.route('/')
def hello():

	uListStr = ""
	sqliteDB = sqlite3.connect(DATABASE)
	print ("Opened database successfully")
	#sqliteDB.execute('DROP TABLE IF exists students')
	sqliteDB.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, addr TEXT, city TEXT, pin TEXT)')
	
	#sqliteDB.execute('DROP TABLE IF exists clazz')
	sqliteDB.execute('CREATE TABLE IF NOT EXISTS clazz (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
	sqliteDB.execute('CREATE TABLE IF NOT EXISTS classstudent (id INTEGER PRIMARY KEY AUTOINCREMENT, class_id INTEGER, student_id INTEGER)')
	
	print ("Table created successfully")
	
	cur = sqliteDB.cursor()
	cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",('wan', '99', 'san', '1111'))

	sqliteDB.commit()
			
	#sqliteDB.row_factory = sql.Row
	cur = sqliteDB.cursor()
	cur.execute("select * from students")
	result = cur.fetchall();
	print(result)
	for data in result:
	    print(data)
	
	print("")
	id = 1
	cur.execute(f"select * from students where id = {id} ")
	result = cur.fetchall();
	for data in result:
		for d in data:
			print(d)
		
	fields = cur.description
	column_list = []
	for i in fields:
		column_list.append(i[0])
	print(column_list)
	# ['Id', 'name', 'password', 'birthplace']
	
	cur.execute(f"select max(id) from students")
	result = cur.fetchall();
	print(result[0][0])
	
	sqliteDB.close()

	s = json.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
	print (s)

	data = request.get_data().decode("utf-8")
	print(data)
	json_data = json.loads(data)
	print(json_data)
	return "hello"


@app.route('/students', methods=['POST'])
def	create_student():
	data = request.get_data().decode("utf-8")
	print(data)
	json_data = json.loads(data)
	name = json_data["name"]
	print(json_data)
	
	sqliteDB = sqlite3.connect(DATABASE)
	cur = sqliteDB.cursor()
	cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(name, '', '', ''))
	sqliteDB.commit()
	cur.execute(f"select max(id) from students")
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
	cur.execute(f"select * from students where id = {id}")
	result = cur.fetchall();
	sqliteDB.close()
	name = result[0][1]
			
	return {
		"id": id, 
		"name":name
	}, 201
	
@app.route('/classes', methods=['POST'])
def	create_class():
	data = request.get_data().decode("utf-8")
	print(data)
	json_data = json.loads(data)
	name = json_data["name"]
	print(json_data)
	
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
		cur.execute(f"select * from students where id = {student_id}")
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
	print(data)
	json_data = json.loads(data)
	class_id = json_data["class_id"]
	student_id = json_data["student_id"]
	print(json_data)
	
	sqliteDB = sqlite3.connect(DATABASE)
	cur = sqliteDB.cursor()
	cur.execute("INSERT INTO classstudent (class_id, student_id) VALUES (?,?)",(class_id, student_id))
	sqliteDB.commit()
	
	cur.execute(f"select * from clazz where id = {class_id}")
	result = cur.fetchall()
	class_name = result[0][1]
	
	cur.execute(f"select * from students where id = {student_id}")
	result = cur.fetchall()
	student_name = result[0][1]
	
	sqliteDB.close()
	
	return {
	"id": class_id, 
	"name":class_name,
	"students": [
		{	"student" :{
			"id" : student_id,
			"name" : student_name
			}
		}
		]
	}, 201