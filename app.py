from flask import Flask, redirect, render_template, request, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'Ajeet29599@#'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        username = request.form['u_name']
        password = request.form['pass']
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        global data
        data = cursor.fetchone()
        if data != None:
            session['user'] = data[1]
            flash(f'{session["user"]} Logged in Successfully...')
            return redirect(url_for('home'))    
        else:
            return redirect(url_for('error'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        query = "INSERT INTO Users (email,username,password) VALUES(?,?,?)"
        cursor.execute(query, (email, username, password))
        connection.commit()
        if cursor.rowcount == 1:
            flash('Your account created Successfully...')
            return redirect(url_for('login'))
        else:
            flash('Something Wrong! Try Again...')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/add_expenses', methods=['GET', 'POST'])
def add_expenses():
    if 'user' in session:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        if request.method == 'POST':
            date_ = request.form['date']
            name = request.form['name']
            products = request.form['prod_name']
            prod_qnty = request.form['prod_Qty']
            prod_price = request.form['price']
            query = "INSERT INTO Products (date_, name, products, prod_qnty, prod_price) VALUES(?,?,?,?,?)"
            cursor.execute(query, (date_, name, products, prod_qnty, prod_price))
            connection.commit()
            flash('Expense Saved Successfully')
            if cursor.rowcount == 1:
                return redirect(url_for('add_expenses'))
            else:
                flash('Saved Unsuccessful')
        return render_template('add_expense.html')
    else:
        return redirect(url_for('login'))

@app.route('/view', methods=['GET', 'POST'])
def view():
    if 'user' in session:
        connection = sqlite3.connect("users.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("select * from Products")
        rows = cursor.fetchall()
        return render_template("view.html", rows=rows)
    else:
        return redirect(url_for('login'))

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if 'user' in session:
        connection = sqlite3.connect("users.db")
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('select * from Products WHERE id={0}'.format(id))
        rows = cursor.fetchone()
        connection.close()
        if request.method == 'POST':
            try:
                date_ = request.form['date']
                name = request.form['name']
                products = request.form['prod_name']
                prod_qnty = request.form['prod_Qty']
                prod_price = request.form['price']
                con = sqlite3.connect("users.db")
                cur = con.cursor()
                cur.execute('Update Products set date_= ?, name=?, products=?, prod_qnty=?, prod_price=?  WHERE id=?',
                            (date_, name, products, prod_qnty, prod_price, id))
                con.commit()
                flash('Updated Successfully')
            except:
                flash('Update Error')
            finally:
                return redirect(url_for('view'))
        return render_template('update.html', rows=rows)
    else:
        return redirect(url_for('login'))

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    if 'user' in session:
        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()
        cursor.execute('DELETE from Products WHERE id={0}'.format(id))
        connection.commit()
        flash('Deleted Successfully')
        return redirect(url_for('view'))
    else:
        return redirect(url_for('login'))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/contact')
def contact():
    if 'user' in session:
        return render_template('contact.html')
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    if 'user' in session:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['user'] = data[1]
    session.pop('user', None)
    flash('Logged out Successfully...')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)