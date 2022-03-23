from datetime import timedelta
from flask import Flask, redirect, render_template, request, url_for, session ,flash
import sqlite3

app = Flask(__name__)
app.secret_key= 'Ajeet'
app.permanent_session_lifetime=timedelta(minutes=10)


@app.route('/', methods=['GET','POST'] )
def index():
    return render_template('index.html')


@app.route('/login',methods = ['GET','POST'])
def login():

    if request.method == 'POST':
        session.permanent=True
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()

        Username = request.form['u_name']
        password = request.form['pass']
        
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (Username, password ))
        data = cursor.fetchone()
        
        if  data!=None:
            flash('Logged in Successfully...')
            session['email']=data[1]
            return redirect(url_for('home'))
        else:
            return redirect(url_for('error'))

    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        query = "INSERT INTO Users (email,username,password) VALUES(?,?,?)"
        cursor.execute(query,(email,username,password))
        connection.commit()

        if cursor.rowcount == 1:
            return redirect(url_for('login'))
        else:
            print("data insert not successfull")
    return render_template('signup.html')

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:     
        return redirect(url_for('login'))

@app.route('/add_expenses',methods=['GET','POST'])
def add_expenses():
    if 'email' in session:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        if request.method == 'POST':

            date_ = request.form['date']
            name = request.form['name']
            products = request.form['prod_name']
            prod_qnty = request.form['prod_Qty']
            prod_price = request.form['price']
            user_id = request.form['user-id']

            query = "INSERT INTO Products (date_, name, products, prod_qnty, prod_price,user_id) VALUES(?,?,?,?,?,?)"
            cursor.execute(query,(date_, name, products, prod_qnty, prod_price,user_id))
            connection.commit()
            flash('Expense Saved Successfully')
            if cursor.rowcount == 1:
                return redirect(url_for('add_expenses'))
            else:
                flash('Saved Unsuccessfull')
        return render_template('add_expense.html')
    else:
        return redirect(url_for('login'))

@app.route('/view',methods = ['GET','POST'])
def view():
    if 'email' in session: 
        connection = sqlite3.connect("users.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("select * from Products")
        rows = cursor.fetchall()
        return render_template("view.html",rows = rows)
    else:
        return redirect(url_for('login'))

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('select * from Products WHERE id={0}'.format(id))
    rows = cursor.fetchone()
    connection.close()

    if request.method=='POST':
        try:
            date_ = request.form['date']
            name = request.form['name']
            products = request.form['prod_name']
            prod_qnty = request.form['prod_Qty']
            prod_price = request.form['price']
            user_id = request.form['user-id']
            con = sqlite3.connect("users.db")
            cur=con.cursor()
            cur.execute('Update Products set date_= ?, name=?, products=?, prod_qnty=?, prod_price=?,user_id=?  WHERE id=?',(date_,name,products,prod_qnty,prod_price,user_id,id))
            con.commit()
            flash('Updated Successfully')
        except:
            flash('Updation Error')
        finally:
            return redirect(url_for('view'))
    return render_template('update.html',rows = rows)

@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    cursor.execute('DELETE from Products WHERE id={0}'.format(id))
    connection.commit() 
    flash('Deleted Successfully')
    return redirect(url_for('view'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    flash('Logged out Successfully...')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)