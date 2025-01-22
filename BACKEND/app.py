from flask import Flask,jsonify, redirect, render_template, request
import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources= { r"/*": {"origins":"http://localhost:5173"}})


@app.route('/')
def home():
    return "Welcome to the Homepage! <a href='/teacher'>Teacher</a>"

@app.route('/teacher')
def teacher():
    conn = db.connect_db()
    cursor = conn.cursor()
    cursor.execute('select * from teacher')
    rows = cursor.fetchall()
    
    result = [
        {"id":row[0], "name":row[1], "address":row[2], "phone":row[3]}
        for row in rows
    ]
    return jsonify(result)

@app.route('/addTeacher', methods=['POST'])
def addTeacher():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        id = int(data['id'])
        address = data['address']
        phone = data['phone']
        conn = db.connect_db()
        try:
            querry = "insert into teacher(tId,name,address,phone) values(%s,%s,%s,%s)"
            cursor = conn.cursor()
            cursor.execute(querry,(id,name,address,phone))
            conn.commit()
            return jsonify({"success":True,"message":"Teacher Added successfully."})
        except Exception as e:
            conn.rollback()
            return jsonify({"success":False, "message":"Failed to register "})
      

@app.route('/deleteTeacher', methods=['POST'])
def deleteTeacher():
    if request.method == 'POST':
        data = request.get_json()
        id = int(data.get('id'))
        print(id)
        conn = db.connect_db()
        cursor = conn.cursor()
        try:
            querry = "delete from teacher where tId = %s"
            cursor.execute(querry,(id,))
            conn.commit()
            return jsonify({"success":True, "message":"Teacher Deleted successfully"})
        except Exception as e:
            conn.rollback()
            return jsonify({"success":False, "message":"Failed to delete Teacher"})
        finally:
            cursor.close()
            conn.close()
    
    
    

if __name__ == '__main__':
    app.run(debug=True)