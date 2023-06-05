from flask import Flask,render_template,request
import sqlite3


app=Flask(__name__)


def createdb():
    con = sqlite3.connect('student.db')
    query = """ CREATE TABLE IF NOT EXISTS stud (
            Roll_no INTEGER UNIQUE ,
            Name VARCHAR(250),
            DOB TEXT,
            mark int,
            grade text

    )"""
    con.execute(query)
    con.close()

createdb()




@app.route('/api/students',methods=['GET','POST'])
def all_students():
    con = sqlite3.connect('student.db')
    cur =con.cursor( )
    query = 'SELECT * FROM stud'
    cur.execute( query)
    viewData = cur.fetchall( )
    con.close()
    print(viewData)
    return render_template ('new.html',data = viewData)
    

@app.route('/api/student/add',methods=['GET','POST'])
def all_students1():
    if request.method=='POST':
        roll  = request.form['roll_no']
        name  =  request.form['sname']
        dob   =  request.form['dob']
        con   = sqlite3.connect('student.db')

        cur = con.cursor( )
        query = 'INSERT INTO stud (roll_no,name,dob) VALUES(?,?,?)'
        tup_vale = (roll,name,dob)
        cur.execute(query,tup_vale)
        con.commit()
        return render_template('new.html',data='successfully added')
    return render_template('insert.html')



@app.route('/api/student/<int:pk>',methods=['GET','POST'])
def change1(pk):
    con = sqlite3.connect('student.db')
    cur =con.cursor( )
    query = 'SELECT * FROM stud where roll_no=?'
    tup_vale =(pk,)
    cur.execute(query,tup_vale)
    viewData = cur.fetchall( )
    con.close()
    print(viewData)
    return render_template ('new.html',data = viewData)



@app.route('/api/student/<int:pk>/<int:mark>',methods=['GET','POST'])
def change2(pk,mark):
    con = sqlite3.connect('student.db')
    cur =con.cursor( )
    query = 'UPDATE stud set mark=? where roll_no=?'
    tup_vale =(mark,roll_no)
    cur.execute(query,tup_vale)
    con.commit()
    viewData = cur.fetchall( )
    con.close()
    print(viewData)
    return render_template ('new.html',data = viewData)

# /api/student/<pk>/mark/
@app.route('/api/student/<int:pk>/<int:mark>',methods=['GET','POST'])
def change3(pk,mark):
    con = sqlite3.connect('student.db')
    cur =con.cursor( )
    query = 'SELECT * FROM stud Where roll_no=?'
    tup_vale =(roll_no,)
    viewData = cur.fetchall( )
    con.close()
    print(viewData)
    return render_template ('new.html',data = viewData)


#/api/student/results/
@app.route('/api/student/results',methods=['GET','POST'])
def result():
    connection = sqlite3.connect('studentdetail.db')
    cursor = connection.cursor()
    cursor.execute("SELECT roll_no,name,mark from stud")
    alldata = cur.fetchall()
    total = len(alldata)
    count = 1
    for each in alldata:
        if each[2]>90:
            grade = 'S'
        elif each[2]>81 & each[2]<90:
            grade = "A"
        elif each[2]>71 & each[2]<80:
            grade = "B"
        elif each[2]>61  & each[2]<70:
            grade = "C"
        elif each[2]>51 & each[2]<60:
            grade = "D"
        elif each[2]>50 & each[2]<55:
            grade = "E"
        else:
            grade='F'
            count = count+1
        

        qry="UPDATE stud SET grade=? WHERE rollno=? "
        tup_word = (each[0],grade)
        cur.execute(qry,tup_word)
        con.commit()
    Pass_percentage = [ ( total - count) / total ]
    Pass_percentage = Pass_percentage* 100
    print(Pass_percentage)

    








if __name__ == '__main__':
    app.run(debug=True)
