from flask import Flask, render_template, request,url_for,session
import sqlite3

app = Flask(__name__)

@app.route('/',methods = ['GET','POST'])
def login():

    if request.method == 'POST':

        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        Username = request.form['u_name']
        password = request.form['pass']

        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (Username, password, ))
        data = cursor.fetchone()


        if request.form['u_name'] == Username and request.form['pass'] == password:
            return render_template("home.html")
        else:
            return render_template("error.html")

    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    msg = ''
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    if request.method == 'POST':


        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        query = "INSERT INTO Users (email,username,password) VALUES(?,?,?)"
        cursor.execute(query,(email,username,password))
        connection.commit()
        msg = 'Your account Created successfully'

        if cursor.rowcount == 1:
            return render_template("home.html",msg=msg)
        else:
            print("data insert not succfull")

    return render_template('signup.html')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/add_expenses',methods=['GET','POST'])
def add_expenses():

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    if request.method == 'POST':

        Date = request.form['date']
        Name = request.form['name']
        Product = request.form['prod_name']
        prod_Qty = request.form['prod_Qty']
        prod_price = request.form['price']

        query = "INSERT INTO Products (Date, Name, Product, prod_Qty, prod_price) VALUES(?,?,?,?,?)"
        cursor.execute(query,(Date, Name, Product, prod_Qty, prod_price))
        connection.commit()
        msg = 'Your Expense Data Saved successfully'

        if cursor.rowcount == 1:
            return render_template("home.html",msg=msg)
        else:
            print("data insert not succfull")

    return render_template('add_expense.html')

@app.route('/view',methods = ['GET','POST'])
def view():

     connection = sqlite3.connect("users.db")
     connection.row_factory = sqlite3.Row
     cursor = connection.cursor()
     cursor.execute("select * from Products")
     rows = cursor.fetchall()
     return render_template("view.html",rows = rows)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)
