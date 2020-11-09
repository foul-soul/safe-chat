from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import os
from rsa_algo import generateKeys
from diffeHellman import pk, secret, skid
from aescbc import encrypt, decrypt

from wtforms.fields.html5 import EmailField

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '#Mo6@mysql'
app.config['MYSQL_DB'] = 'chatdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            flash('Unauthorized, Please logged in', 'danger')
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('Unauthorized, You logged in', 'danger')
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


@app.route('/')
def index():
    return render_template('home.html')


class LoginForm(Form):  # Create Message Form
    username = StringField('Username', [validators.length(min=1)], render_kw={'autofocus': True})


# User Login
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['name']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                flash('You are now logged in', 'success')

                return redirect(url_for('index'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=3, max=50)], render_kw={'autofocus': True})
    username = StringField('Username', [validators.length(min=3, max=25)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email(), validators.length(min=4, max=25)])
    password = PasswordField('Password', [validators.length(min=3)])


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        get_username = cur.execute("SELECT * FROM users WHERE username=%s", [username])
        if get_username > 0:
            flash('username already exist', 'danger')
            return redirect(url_for('register'))
        else:
            cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                        (name, email, username, password))
            # Commit cursor
            mysql.connection.commit()
            # get id
            get_id = cur.execute("SELECT * FROM users WHERE username=%s", [username])
            data = cur.fetchone()
            if get_id > 0:
                rid = data['id']
                ppvk, ppbk = generateKeys()
                get_ppbk = cur.execute("SELECT * FROM rsa WHERE ppbk=%s", [ppbk])
                while get_ppbk > 0:
                    ppvk, ppbk = generateKeys()
                    get_ppbk = cur.execute("SELECT * FROM rsa WHERE ppbk=%s", [ppbk])
                cur.execute("INSERT INTO rsa(id, ppbk, ppvk) VALUES(%s, %s, %s)", (rid, ppbk, ppvk))
                mysql.connection.commit()
                cur.execute("SELECT * FROM users")
                users = cur.fetchall()
                cur.close()
            flash('You are now registered and can login', 'success')

            return redirect(url_for('index'))

    return render_template('register.html', form=form)


class MessageForm(Form):  # Create Message Form
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.connection.cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data['name']
            uid = session['uid']
            session['lid'] = id
            id = int(id)
            uid = int(uid)
            if id < uid:
                user1 = id
                user2 = uid
            else:
                user1 = uid
                user2 = id
            secretkid = skid(id, uid)
            get_skey = cur.execute("SELECT * FROM skey WHERE skid=%s", [secretkid])
            secretkey = cur.fetchone()
            if get_skey > 0:
                sk = secretkey['sk']
            else:
                if id < uid:
                    user1 = id
                    user2 = uid
                else:
                    user1 = uid
                    user2 = id
                get_keys = cur.execute("SELECT * FROM rsa WHERE id=%s", [user1])
                get_keys_user1 = cur.fetchone()
                user1pvk = get_keys_user1['ppvk']
                user1pbk = get_keys_user1['ppbk']
                get_keys = cur.execute("SELECT *FROM rsa WHERE id=%s", [user2])
                get_keys_user2 = cur.fetchone()
                user2pvk = get_keys_user2['ppvk']
                user2pbk = get_keys_user2['ppbk']
                sharedpkuser2 = pk(user2pvk, user1pbk, user2pbk)
                sk = secret(user1pvk, user2pbk, sharedpkuser2)
                cur.execute("INSERT INTO skey(skid, sk) VALUES(%s, %s)", (secretkid, sk))
                mysql.connection.commit()
            if request.method == 'POST' and form.validate():
                txt_bod = form.body.data
                sk = bytes(str(sk), "utf-8")
                txt_body = encrypt(sk, txt_bod, 100000)
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, id, uid))
                # Commit cursor
                mysql.connection.commit()

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            return render_template('chat_room.html', users=users, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        # Create cursor
        cur = mysql.connection.cursor()
        secretkid = skid(id, uid)
        cur.execute("SELECT * FROM skey WHERE skid=%s", [secretkid])
        secretkey = cur.fetchone()
        sk = secretkey['sk']
        sk = bytes(str(sk), "utf-8")
        # Get message
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (id, uid, uid, id))

        chats = cur.fetchall()
        for message in chats:
            cipher = message['body']
            plaintext = decrypt(sk, cipher, 100000)
            plaintext = plaintext.decode('utf-8')
            message['body'] = plaintext
        # Close Connection
        cur.close()
        return render_template('chats.html', chats=chats,)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
