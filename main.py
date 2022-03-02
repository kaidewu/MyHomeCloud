from flask import Flask, redirect, url_for, session, render_template, send_file, request
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
import db
import hashlib
import re
from dotenv import load_dotenv
load_dotenv('C:\\Users\\kayfe\\Desktop\\Github\\MyHomeCloud\\config.env')
secret_key = os.environ.get('SECRET_KEY')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_host = os.environ.get('MYSQL_HOST')
mysql_db = os.environ.get('MYSQL_DB')
BASE_DIR = os.environ.get('BASE_DIR')
abs_path_folder = []

app = Flask(__name__,template_folder='template')
app.secret_key = secret_key

# Conexion a la base de datos
app.config['MYSQL_HOST'] = mysql_host
app.config['MYSQL_USER'] = mysql_user
app.config['MYSQL_PASSWORD'] = mysql_password
app.config['MYSQL_DB'] = mysql_db
# Iniciar MySQL
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
     # Si algo sale mal que salga un mensaje
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = hashlib.sha256((request.form['password']).encode('utf-8')).hexdigest().upper()
        # If account exists in accounts table in out database
        if db.fetchUserexists(username, password):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = db.fetchUserexists(username, password)['id']
            session['username'] = db.fetchUserexists(username, password)['username']
            session['foldername'] = db.fetchFolderName(session['id'], session['username'])['folder_name']
            abs_path_folder.append(BASE_DIR + session['foldername'] + '\\')
            if (db.fetchUserexists(username, password)['level'] == 'administrator'):
                # Redirect to admin page
                return redirect(url_for('admin'))
            else:
                # Redirect to home page
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# http://192.168.1.47register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = hashlib.sha256((request.form['password']).encode('utf-8')).hexdigest().upper()
        email = request.form['email']
        # If account exists show error and validation checks
        if db.fetchUserexists(username, password):
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            folder_name = hashlib.sha256((username + email).encode('utf-8')).hexdigest().upper()
            db.fetchInsertUser(username, password, email, folder_name)
            os.mkdir(f'E:\\{folder_name}')
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://192.168.1.47/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_list(req_path):
    if 'loggedin' in session:
        global BASE_DIR
        global abs_path_folder
        dir_folders = []
        dir_files = []
        user_folder = BASE_DIR + session['foldername'] + '\\'
        abs_path = os.path.join(user_folder, req_path)
        if len(abs_path_folder) == 10:
            abs_path_folder = []
        if os.path.isdir(abs_path):
            abs_path_folder.append(abs_path)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = os.listdir(abs_path)
        for f in files:
            try:
                abs_file_path = os.path.abspath(user_folder + f)
                if os.path.isdir(abs_file_path):
                    dir_folders.append(f)
                else:
                    dir_files.append(f)
            except:
                return render_template('404.html')
        return render_template('content.html', dir_files=dir_files, dir_folders=dir_folders, abs_path_folder=abs_path_folder)
    return redirect(url_for('login'))

@app.route('/upload', methods = ['GET', 'POST'])
def upload_files():
    global abs_path_folder
    if request.method == 'POST':
            f = request.files.getlist('file')
            if f[0]:
                for file in f:
                    file.save(f'{abs_path_folder[-1]}\\{secure_filename(file.filename)}')
                abs_path_folder = []
                return redirect(url_for('dir_list'))
            else:
                msg = 'Select one file, please'
                return render_template('content.html', msg=msg)

@app.route('/create', methods = ['GET', 'POST'])
def create_folder():
    global abs_path_folder
    if request.method == 'POST':
        name = request.form.get('text')
        if name != '':
            name_folder = os.path.join(abs_path_folder[-1], name)
            os.mkdir(name_folder)
            abs_path_folder = []
            return redirect(url_for('dir_list'))
        else:
            msg = 'Write a name, please'
            return render_template('content.html', msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)