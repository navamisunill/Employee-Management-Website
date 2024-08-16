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
    
    return render_template('alogin.html')


@app.route('/employee')
def employee():
    if 'eusername' in session:
        # Retrieve all employees
        mycursor.execute("SELECT * FROM project.employee")
        employees = mycursor.fetchall()

        # Retrieve the count of pending leave applications for each employee
        sql = """
        SELECT Employeeid, COUNT(*) as pending_count 
        FROM project.leave_applications 
        WHERE status = 'Pending' 
        GROUP BY Employeeid
        """
        mycursor.execute(sql)
        pending_counts = mycursor.fetchall()

        # Create a dictionary for easy lookup of pending leave counts
        pending_counts_dict = {item['Employeeid']: item['pending_count'] for item in pending_counts}

        return render_template('home.html', employees=employees, pending_counts=pending_counts_dict)

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
    
    
    
@app.route("/employee_register", methods=['GET', 'POST'])
def employee_register():
    if request.method == "POST":
        Employeeid= escape(request.form["Employeeid"])
        password= escape(request.form["password"])
        
        sql="insert into employee_login (Employeeid, password) values (%s,%s)"
        val=(Employeeid , password)
        mycursor.execute(sql,val)
        mydb.commit()
        flash("Registration Succesful")
        return redirect (url_for('employee_login'))
    
    return render_template("empregister.html")


@app.route("/employee_login", methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        Employeeid= escape( request.form["Employeeid"])
        password= escape(request.form["password"])
        
        sql= "select * from employee_login where Employeeid = %s and password = %s"
        val= (Employeeid, password)
        mycursor.execute(sql,val)
        employee=mycursor.fetchone()
        
        if employee:
            session["Employeeid"] = Employeeid 
            flash("Login Succesful")
            return redirect(url_for("employee_dashboard"))
            
            
        else:
            flash("Invalid Employeeid or password")
            return redirect(url_for ("employee_login"))
        
    return render_template("emplogin.html")


@app.route("/employee_dashboard", methods=['GET', 'POST'])
def employee_dashboard():
    if "Employeeid" in session:
        Employeeid = session["Employeeid"]
        
        sql= "select * from employee where Employeeid = %s"
        val= (Employeeid,)
        mycursor.execute(sql, val )
        employee = mycursor.fetchone()
        
        if employee:
                return render_template("empdashboard.html", employee=employee)
        else:
            flash("No employee details found.")
            return redirect(url_for("employee_login"))
    
    else:
        flash("You need to login first")
        return redirect(url_for ("employee_login"))
    



@app.route("/employee/apply_leave", methods=['GET', 'POST'])
def apply_leave():
    if "Employeeid" in session:
        Employeeid = session["Employeeid"]

        if request.method == 'POST':
            # Retrieve form data
            leave_type = escape(request.form['leave_type'])
            other_leave_type = escape(request.form['other_leave_type']) if 'other_leave_type' in request.form else ''
            leave_reason = escape(request.form['leave_reason'])
            leave_start = escape(request.form['leave_start'])
            leave_end = escape(request.form['leave_end'])

            # Use the "Other" leave type if it's specified
            if leave_type == "Other" and other_leave_type:
                leave_type = other_leave_type

            # Insert the new leave application into the database
            sql = """
                INSERT INTO leave_applications (Employeeid, leave_type, leave_reason, leave_start, leave_end)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (Employeeid, leave_type, leave_reason, leave_start, leave_end)
            mycursor.execute(sql, values)
            mydb.commit()

            if mycursor.rowcount > 0:
                flash("Leave application submitted successfully.")
            else:
                flash("Failed to submit leave application.")
            return redirect(url_for("apply_leave"))

        # Retrieve all leave applications for the current employee
        sql = "SELECT * FROM leave_applications WHERE Employeeid = %s"
        mycursor.execute(sql, (Employeeid,))
        leaves = mycursor.fetchall()

        return render_template("apply_leave.html", leaves=leaves)
    else:
        flash("You need to login first.")
        return redirect(url_for("employee_login"))


@app.route('/employee/view_leave_applications/<Employeeid>', methods=['GET', 'POST'])
def view_leave_applications(Employeeid):
    if 'eusername' in session:
        if request.method == 'POST':
            # Retrieve form data
            application_id = request.form['application_id']
            admin_decision = request.form['admin_decision']

            # Update the leave application status in the database
            sql = "UPDATE leave_applications SET status = %s WHERE sno = %s"
            mycursor.execute(sql, (admin_decision, application_id))
            mydb.commit()

            flash("Leave application updated successfully.")
            return redirect(url_for("view_leave_applications", Employeeid=Employeeid))

        # Retrieve all leave applications for the specific employee
        sql = "SELECT * FROM leave_applications WHERE Employeeid = %s"
        mycursor.execute(sql, (Employeeid,))
        leave_applications = mycursor.fetchall()

        # Retrieve employee details
        sql = "SELECT * FROM employee WHERE Employeeid = %s"
        mycursor.execute(sql, (Employeeid,))
        employee = mycursor.fetchone()

        return render_template("admin_leave_applications.html", employee=employee, leave_applications=leave_applications)
    else:
        flash("You need to login as admin first.")
        return redirect(url_for("alogin"))
    
    
@app.route("/logout")
def logout():
    session.pop("Employeeid", None) 
    flash ("You have been logged out")
    return redirect(url_for ("employee_login"))

           

if __name__ == '__main__':
    app.run(debug=True)


