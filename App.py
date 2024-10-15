from flask import Flask, flash, render_template, request,redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
# coneccion mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM contacts')
  data = cur.fetchall()
  return render_template('index.html',contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    print(fullname)
    print(phone)
    print(email)
    cur= mysql.connection.cursor()
    cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',
    (fullname,phone,email))
    mysql.connection.commit()
    flash('contacto agregado')
    return redirect(url_for('Index'))
    

  

@app.route('/edit/<id>')
def get_contact(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM contacts WHERE id = %s',[id])
  data = cur.fetchall()
  return render_template('edit-contact.html' , contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
  cur = mysql.connection.cursor()          #triple comillas para poder escribir en varias lineas
  cur.execute("""                
     UPDATE contacts                   
     SET fullname = %s,
      email = %s,
      phone = %s
      WHERE id = %s
       """, (fullname, email, phone, id))
  mysql.connection.commit()
  flash('contacto actualizado')
  return redirect(url_for('Index'))

@app.route('/delete/<string:id>') # ver que pasas si lo paso a int
def delete_contact(id):
 cur = mysql.connection.cursor()
 cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id)) #formatea el dato de str a int
 mysql.connection.commit()
 flash('contacto removido')
 return redirect(url_for('Index'))

if __name__ == '__main__':
  app.run(port = 3000,debug= True)