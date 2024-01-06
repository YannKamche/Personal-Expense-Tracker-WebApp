# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request, redirect, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import snowflake.connector
import json


app = Flask(__name__)


app.secret_key = 'a'
  
app.config['SNOWFLAKE_ACCOUNT'] = 'nnuvqtc-fn75306'
app.config['SNOWFLAKE_USER'] = 'YANN'
app.config['SNOWFLAKE_PASSWORD'] = 'Snowflake2023'
app.config['SNOWFLAKE_DATABASE'] = 'PERSONAL_EXPENSE_TRACKER'
app.config['SNOWFLAKE_WAREHOUSE'] = None

# Function to get Snowflake connection
def get_snowflake_connection():
    with open('snowflake_credentials.json') as credentials_file:
        credentials = json.load(credentials_file)

    connection = snowflake.connector.connect(
        account=credentials['SNOWFLAKE_ACCOUNT'],
        user=credentials['SNOWFLAKE_USER'],
        password=credentials['SNOWFLAKE_PASSWORD'],
        database=credentials['SNOWFLAKE_DATABASE'],
        warehouse=credentials['SNOWFLAKE_WAREHOUSE'],
    )
    return connection


# Query execution using Snowflake connection
def execute_snowflake_query(query, params=None):
    connection = get_snowflake_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result



#HOME--PAGE
@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")



#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT * FROM register WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only characters and numbers!'
        else:
            cursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, password))

            get_snowflake_connection().commit()
            msg = 'You have successfully registered!'
            return render_template('signup.html', msg=msg)

        return render_template('signup.html', msg=msg)
 
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password ),)
        account = cursor.fetchone()
        print (account)
        
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)



       





#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense', methods=['POST'])
def addexpense():
    try:
        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']

        # Validate input
        if date is None or expensename is None or amount is None or paymode is None or category is None:
            # Handle the error or return an appropriate response
            return redirect("/display")  # Redirect to display even if there's an error

        cursor = get_snowflake_connection().cursor()

        # Insert into expenses table
        cursor.execute('INSERT INTO expenses (userid, date, expensename, amount, paymode, category) VALUES (%s, %s, %s, %s, %s, %s)',
                       (session['id'], date, expensename, amount, paymode, category))

        # Commit the transaction
        get_snowflake_connection().commit()

        print(date + " " + expensename + " " + amount + " " + paymode + " " + category)

        return redirect("/display")

    except Exception as e:
        # Handle the exception, you might want to log it for debugging
        error_msg = f'Error adding expense: {str(e)}'
        return redirect("/display")  # Redirect to display even if there's an error

    finally:
        cursor.close()




#DISPLAY---graph 

@app.route("/display")
def display():
    print(session["username"], session['id'])

    cursor = get_snowflake_connection().cursor()
    cursor.execute('SELECT * FROM expenses WHERE userid = %s ORDER BY date DESC', (str(session['id']),))
    expense = cursor.fetchall()

    if expense is not None:
        return render_template('display.html', expense=expense)
    else:
        # Handle the case where there are no records in the "expenses" table
        error_message = "No expense records found."
        return render_template("error.html", error_message=error_message)


                          



#delete---the--data

@app.route('/delete/<string:id>', methods = ['POST', 'GET' ])
def delete(id):
     cursor = get_snowflake_connection().cursor()
     cursor.execute('DELETE FROM expenses WHERE  id = {0}'.format(id))
     get_snowflake_connection().commit()
     print('deleted successfully')    
     return redirect("/display")
 
    
#UPDATE---DATA

@app.route('/edit/<id>', methods = ['POST', 'GET' ])
def edit(id):
    cursor = get_snowflake_connection().cursor()
    cursor.execute('SELECT * FROM expenses WHERE  id = %s', (id,))
    row = cursor.fetchall()
   
    print(row[0])
    return render_template('edit.html', expenses = row[0])




@app.route('/update/<id>', methods = ['POST'])
def update(id):
  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
    
      cursor = get_snowflake_connection().cursor()
       
      cursor.execute("UPDATE `expenses` SET `date` = % s , `expensename` = % s , `amount` = % s, `paymode` = % s, `category` = % s WHERE `expenses`.`id` = % s ",(date, expensename, amount, str(paymode), str(category),id))
      get_snowflake_connection().commit()
      print('successfully updated')
      return redirect("/display")
     
      
#limit
@app.route("/limit" )
def limit():
    return redirect('/limitn')

@app.route("/limitnum", methods=['POST'])
def limitnum():
    if request.method == "POST":
        number = request.form['number']
        cursor = get_snowflake_connection().cursor()
        cursor.execute('INSERT INTO "limits" VALUES (NULL, %s, %s)', (session['id'], number))
        get_snowflake_connection().commit()
        return redirect('/limitn')

@app.route("/limitn")
def limitn():
    cursor = get_snowflake_connection().cursor()
    cursor.execute('SELECT limitss FROM limits ORDER BY id DESC LIMIT 1')
    x = cursor.fetchone()

    if x is not None:
        s = x[0]
        return render_template("limit.html", y=s)
    else:
        # Handle the case where there are no records in the "limits" table
        s = "No data found"
        return render_template("limit.html", y=s)



#REPORT

@app.route("/today")
def today():
    try:
        # Fetch time and amount
        with get_snowflake_connection().cursor() as cursor:
            cursor.execute('SELECT TIME(date), amount FROM expenses WHERE userid = %s AND DATE(date) = CURRENT_DATE', (str(session['id']),))
            texpense = cursor.fetchall()
            print(texpense)

        # Fetch all columns and order by date
        with get_snowflake_connection().cursor() as cursor:
            cursor.execute('SELECT * FROM expenses WHERE userid = %s AND DATE(date) = CURRENT_DATE ORDER BY date DESC', (str(session['id']),))
            expense = cursor.fetchall()

        total = 0
        t_food = 0
        t_entertainment = 0
        t_business = 0
        t_rent = 0
        t_EMI = 0
        t_other = 0

        for x in expense:
            total += x[4]
            if x[6] == "food":
                t_food += x[4]
            elif x[6] == "entertainment":
                t_entertainment += x[4]
            elif x[6] == "business":
                t_business += x[4]
            elif x[6] == "rent":
                t_rent += x[4]
            elif x[6] == "EMI":
                t_EMI += x[4]
            elif x[6] == "other":
                t_other += x[4]

        print(total, t_food, t_entertainment, t_business, t_rent, t_EMI, t_other)

        return render_template("today.html", texpense=texpense, expense=expense, total=total,
                               t_food=t_food, t_entertainment=t_entertainment,
                               t_business=t_business, t_rent=t_rent,
                               t_EMI=t_EMI, t_other=t_other)

    except Exception as e:
        print(str(e))
        return render_template('error.html', error=str(e))
     

@app.route("/month")
def month():
    try:
        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= %s AND MONTH(DATE_TRUNC(\'MONTH\', CURRENT_DATE())) = MONTH(DATE_TRUNC(\'MONTH\', date)) GROUP BY DATE(date) ORDER BY DATE(date) ', (str(session['id']),))
        texpense = cursor.fetchall()
        print(texpense)

        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT * FROM expenses WHERE userid = %s AND MONTH(DATE_TRUNC(\'MONTH\', CURRENT_DATE())) = MONTH(DATE_TRUNC(\'MONTH\', date)) ORDER BY date DESC', (str(session['id']),))
        expense = cursor.fetchall()

        total = 0
        t_food = 0
        t_entertainment = 0
        t_business = 0
        t_rent = 0
        t_EMI = 0
        t_other = 0

        for x in expense:
            total += x[4]
            if x[6] == "food":
                t_food += x[4]
            elif x[6] == "entertainment":
                t_entertainment += x[4]
            elif x[6] == "business":
                t_business += x[4]
            elif x[6] == "rent":
                t_rent += x[4]
            elif x[6] == "EMI":
                t_EMI += x[4]
            elif x[6] == "other":
                t_other += x[4]

        print(total, t_food, t_entertainment, t_business, t_rent, t_EMI, t_other)

        return render_template("today.html", texpense=texpense, expense=expense, total=total,
                               t_food=t_food, t_entertainment=t_entertainment,
                               t_business=t_business, t_rent=t_rent,
                               t_EMI=t_EMI, t_other=t_other)

    except Exception as e:
        print(str(e))
        return render_template('error.html', error=str(e))


@app.route("/year")
def year():
    try:
        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= %s AND YEAR(DATE_TRUNC(\'YEAR\', CURRENT_DATE())) = YEAR(DATE_TRUNC(\'YEAR\', date)) GROUP BY MONTH(date) ORDER BY MONTH(date) ', (str(session['id']),))
        texpense = cursor.fetchall()
        print(texpense)

        cursor = get_snowflake_connection().cursor()
        cursor.execute('SELECT * FROM expenses WHERE userid = %s AND YEAR(DATE_TRUNC(\'YEAR\', CURRENT_DATE())) = YEAR(DATE_TRUNC(\'YEAR\', date)) ORDER BY date DESC', (str(session['id']),))
        expense = cursor.fetchall()

        total = 0
        t_food = 0
        t_entertainment = 0
        t_business = 0
        t_rent = 0
        t_EMI = 0
        t_other = 0

        for x in expense:
            total += x[4]
            if x[6] == "food":
                t_food += x[4]
            elif x[6] == "entertainment":
                t_entertainment += x[4]
            elif x[6] == "business":
                t_business += x[4]
            elif x[6] == "rent":
                t_rent += x[4]
            elif x[6] == "EMI":
                t_EMI += x[4]
            elif x[6] == "other":
                t_other += x[4]

        print(total, t_food, t_entertainment, t_business, t_rent, t_EMI, t_other)

        return render_template("today.html", texpense=texpense, expense=expense, total=total,
                               t_food=t_food, t_entertainment=t_entertainment,
                               t_business=t_business, t_rent=t_rent,
                               t_EMI=t_EMI, t_other=t_other)

    except Exception as e:
        print(str(e))
        return render_template('error.html', error=str(e))

#log-out

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

             

if __name__ == "__main__":
    app.run(debug=True)