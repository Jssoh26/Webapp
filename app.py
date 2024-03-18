from flask import Flask, render_template
import csv, sqlite3

def read_file():
    with open('Events2024.csv','r') as file:
        next(file) #skip first line
        lines = csv.reader(file)
        rows = list(lines)
        #for line in lines:
         #   print(line)
        return rows

def import_data(rows):
    conn = sqlite3.connect('CPSG.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Events(Eid INTEGER, Dates TEXT NOT NULL, Name TEXT NOT NULL, Nature TEXT NOT NULL, Organiser TEXT NOT NULL, Category TEXT, Remarks TEXT);")
    for row in rows:
        cur.execute("INSERT INTO Events(Dates, Name, Nature, Organiser, Category, Remarks) VALUES(?,?,?,?,?,?);",(row[0],row[1],row[2],row[3],row[4],row[5]))
    conn.commit()
    conn.close()
        
app = Flask(__name__)   #create flask object

def fetch_data():
    conn = sqlite3.connect('CPSG.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Events")
    data = cur.fetchall()
    conn.close()
    return data

@app.route('/')
def home():
    data = fetch_data()
    return render_template('index.html',events=data)

recs = read_file()
import_data(recs)
app.run()

