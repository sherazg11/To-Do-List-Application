import sqlite3
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['DATABASE'] = 'database.db'



def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cor = conn.cursor()
    cor.execute("CREATE TABLE IF NOT EXISTS toDoList (item TEXT, count INTEGER) ")
    return conn

def close_db_connection(connection):
    connection.close()

def init_db():
    with app.app_context():
        conn = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()

@app.route('/')
def home():
    get_db_connection()
    return render_template('index.html')

@app.route('/page2', methods=['POST'])
def next():
    return render_template('page2.html')

@app.route('/mainPage', methods=['POST', 'GET'])
def mainPage():
    name = request.form.get("name")
    return render_template('mainPage.html', name=name)

@app.route('/listOptions', methods=['POST'])
def listOptions():
    select = request.form.get('userAction')
    if select == "add":
        name = select
    if select == "remove":
        name = select
    if select == "update":
        name = select
    if select == "view":
        name = select
    return render_template('userAction.html', name=name, select = select)

@app.route('/userAction', methods=['POST'])
def userAction():
    Newitem = request.form.get('Newitem')
    count = request.form.get('count')
    action = request.form.get('select')
    print(action)
    if action == "ADD":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO toDoList (count, item) VALUES (?,?)", (count, Newitem))
        conn.commit()
        print("added")
        cursor.close()
        close_db_connection(conn)
        return render_template("msg.html" , msg = "item added")
    if action == "YES":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM toDoList WHERE count = ?", (count,))
        print("removed")
        conn.commit()
        cursor.close()
        close_db_connection(conn)
        return render_template("msg.html" , msg = "item removed")
    if action == "view":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select * from toDoList")
        print("viewed")
        rows = cursor.fetchall()
        cursor.close()
        close_db_connection(conn)
        return render_template("msg.html" , msg = "item viewed" , rows = rows)
    if action == "update":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE toDoList SET item = ? WHERE count = ?", (Newitem,count))
        print("updated")
        conn.commit()
        cursor.close()
        close_db_connection(conn)
        return render_template("msg.html" , msg = "item updated")
        
    return render_template('mainPage.html')


if __name__ == "__main__":
    app.run(debug=True)