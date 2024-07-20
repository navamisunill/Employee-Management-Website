from flask import Flask, render_template ,url_for, request, flash, redirect,session
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
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "admin" and password == "admin":
            session['username'] = username
            flash('Login successful')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('cover.html', username=username)
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    
@app.route('/elogin', methods=['GET', 'POST'])
def elogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Use your criteria for employee login
        if username == "admin" and password == "12345":
            session['eusername'] = username
            flash('Admin login successful')
            return redirect(url_for('employee'))
        else:
            flash('Invalid admin username or password')
            return redirect(url_for('elogin'))
    
    return render_template('elogin.html')


@app.route('/employee')
def employee():
        if 'eusername' in session:
            mycursor.execute("SELECT * FROM project.employee")
            employees = mycursor.fetchall()
            return render_template('home.html', employees=employees)

        else:
            flash('You need to log in as an admin first.')
            return redirect(url_for('elogin'))

@app.route("/employee/create" , methods=['GET'])
def show_employee_create_form():
    if 'eusername' in session:
        return render_template('create.html')
    else:
        flash('You need to log in as an admin first.')
        return redirect(url_for('elogin'))

@app.route('/employee/createemployee', methods=['POST'])
def create():
    if 'eusername' in session:
            # Get form data
            Employeeid = escape(request.form['Employeeid'])
            FirstName = escape(request.form['FirstName'])
            LastName = escape(request.form['LastName'])
            Age = escape(request.form['Age'])
            Designation = escape(request.form['Designation'])
            Salary = escape(request.form['Salary'])
            sql = """INSERT INTO employee (Employeeid, FirstName, LastName, Age, Designation, Salary) VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (Employeeid, FirstName, LastName, Age, Designation, Salary)
            mycursor.execute(sql, values)
            mydb.commit()
            if mycursor.rowcount > 0:
                flash("Employee created successfully")
            else:
                flash("Failed to create employee")

            return redirect(url_for('employee'))
        
    else:
        flash('You need to log in as an admin first.')
        return redirect(url_for('elogin'))

@app.route('/employee/edit/<Employeeid>', methods=['GET', 'POST'])
def edit_employee(Employeeid):
    if 'eusername' in session:
        Employeeid = escape(Employeeid)
        if request.method == 'GET':
            return show_employee_edit_form(Employeeid)
        else:
            FirstName = escape(request.form['FirstName'])
            LastName = escape(request.form['LastName'])
            Age = escape(request.form['Age'])
            Designation = escape(request.form['Designation'])
            Salary = escape(request.form['Salary'])

            sql = """UPDATE employee SET FirstName = %s, LastName = %s, Age = %s, Designation = %s, Salary = %s WHERE Employeeid = %s"""
            
            val = (FirstName, LastName, Age, Designation, Salary, Employeeid)
            mycursor.execute(sql, val)
            mydb.commit()
            if mycursor.rowcount > 0:
                flash("Employee record updated successfully")
            else:
                flash("Failed to update employee record")
            
            return redirect(url_for('employee'))
    else:
        flash('You need to log in as an admin first.')
        return redirect(url_for('elogin'))

def show_employee_edit_form(Employeeid):
    if 'eusername' in session:
        sql = "SELECT * FROM employee WHERE Employeeid = %s"
        val = (Employeeid,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        return render_template("edit.html", employee=myresult)
    else:
        flash('You need to log in as an admin first.')
        return redirect(url_for('elogin'))
    
@app.route('/employee/delete/<Employeeid>', methods=['GET', 'POST'])
def delete_employee(Employeeid):
    Employeeid=escape(Employeeid)
    if request.method=='GET':
        return show_employee_delete_form(Employeeid)
    else:
        Employeeid=escape(Employeeid)
        sql="DELETE FROM employee where Employeeid= %s"
        val=(Employeeid,)
        mycursor.execute(sql,val)
        mydb.commit()
        if mycursor.rowcount>0:
            flash("Employee deleted successfully")
        else:
            flash("Failed to delete employee")
        return redirect(url_for('employee'))
    
def show_employee_delete_form(Employeeid):
    if 'eusername' in session:
        sql = "SELECT * FROM employee WHERE Employeeid = %s"
        val = (Employeeid,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()
        return render_template("delete.html", employee=myresult)
    else:
        flash('You need to log in as an admin first.')
        return redirect(url_for('elogin'))
    
@app.route('/employee/actions/<Employeeid>', methods=['GET', 'POST'])
def actions(Employeeid):
    Employeeid = escape(Employeeid)
    # Retrieve the employee object
    sql = "SELECT * FROM employee WHERE Employeeid = %s"
    val = (Employeeid,)
    mycursor.execute(sql, val)
    employee = mycursor.fetchone()

    # Check if employee exists
    if employee:
        return render_template('eactions.html', employee=employee)
    else:
        flash("Employee not found")
        return redirect(url_for('employee'))



if __name__ == '__main__':
    app.run(debug=True)


