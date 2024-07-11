from flask import Flask, render_template ,url_for, request, flash, redirect
from markupsafe import escape
import mysql.connector

# Create a Flask application instance
app = Flask(__name__)
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="npol",
    database="project"
)

mycursor= mydb.cursor(dictionary=True)



# Define a route and a function to handle the route
@app.route('/')
def index():
    mycursor.execute("SELECT * FROM project.employee")
    employees=mycursor.fetchall()
    return render_template('home.html',employees= employees)

@app.route("/employee")
def show_employee_create_form():
    return render_template('create.html')

@app.route('/employee/create',methods=['GET','POST'])
def create():
    if request.method == 'POST':
        # Get form data
        Employeeid = escape(request.form['Employeeid'])
        FirstName = escape(request.form['FirstName'])
        LastName = escape(request.form['LastName'])
        Age = escape(request.form['Age'])
        Designation = escape(request.form['Designation'])
        Salary = escape(request.form['Salary'])
        sql= """insert into employee (Employeeid, FirstName, LastName, Age, Designation, Salary) values (%s, %s, %s, %s, %s, %s)"""
        values=( Employeeid, FirstName, LastName, Age, Designation, Salary)
        mycursor.execute(sql, values)
        mydb.commit()
        if mycursor.rowcount > 0:
            message= " Employee created successfully"
        else:
            message= None
        flash(message)
        return redirect(url_for('index'))
    
@app.route('/employee/edit/<Employeeid>',methods=['GET','POST'])
def edit_employee(Employeeid):
    Employeeid= escape(Employeeid)
    if request.method == 'GET':
        return show_employee_edit_form(Employeeid)
    else:
        Employeeid = escape(request.form['Employeeid'])
        FirstName = escape(request.form['FirstName'])
        LastName = escape(request.form['LastName'])
        Age = escape(request.form['Age'])
        Designation = escape(request.form['Designation'])
        Salary = escape(request.form['Salary'])

        sql= """UPDATE employee  SET Employeeid = %s, FirstName = %s, LastName = %s, Age= %s, Designation= %s, Salary= %s WHERE Employeeid = %s"""
        
        val=(Employeeid, FirstName, LastName, Age, Designation, Salary, Employeeid)
        mycursor.execute(sql,val)
        mydb.commit()
        if mycursor.rowcount >0:
            message= "Employee record updated successfully"
            flash(message)
        return redirect(url_for('index'))
    
def show_employee_edit_form(Employeeid):
    sql = "SELECT * FROM employee WHERE Employeeid = %s"
    val= (Employeeid,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    return render_template("edit.html",employee=myresult)
        
      


if __name__ == '__main__':
    app.run(debug=True)


