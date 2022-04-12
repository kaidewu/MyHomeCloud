from flask import Flask, redirect, url_for, session, render_template, send_file, request
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from database import db
from datetime import datetime
from hurry.filesize import size
import os
import hashlib
import re
import ssl
from flask_sslify import SSLify

# Importamos el contenido de config.env
from dotenv import load_dotenv
# Ruta en Windows donde este el fichero config.env
load_dotenv('C:\\Users\\kayfe\\Desktop\\Github\\MyHomeCloud\\config.env') # Ruta donde lo guardaste

secret_key = os.environ.get('SECRET_KEY')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_host = os.environ.get('MYSQL_HOST')
mysql_db = os.environ.get('MYSQL_DB')
BASE_DIR = os.environ.get('BASE_DIR')

abs_path_folder = []

app = Flask(__name__,template_folder='template')
sslify = SSLify(app)
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
    # Comprovamos si "username" y "password" POST request existe (los datos los recogemos de los formularios)
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
            abs_path_folder.append(f"{BASE_DIR}{session['foldername']}\\")
            """
            if (db.fetchUserexists(username, password)['level'] == 'administrator'):
                # Redirect to admin page
                return redirect(url_for('admin'))
            else:
                # Redirect to home page
                return redirect(url_for('home'))
            """
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

# http://192.168.1.47/register - Este va ser la pagina donde se van a registrar.
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
            msg = 'Ya existe la cuenta!'
            return render_template('login.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            folder_name = hashlib.sha256((username + email).encode('utf-8')).hexdigest().upper()
            db.fetchInsertUser(username, password, email, folder_name)
            os.mkdir(f'{BASE_DIR}{folder_name}')
            msg_verify = 'La cuenta se ha creado correctamente!'
            return render_template('login.html', msg_verify=msg_verify)
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

"""
# Ruta de los administradores
@app.route('/admin')
def admin():
    if 'loggedin' in session:
        return render_template('admin.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta de la lista de usuarios que hay resgistrado
@app.route('/admin/users')
def userlist():
    if 'loggedin' in session:
        user_info = {}
        num_users = db.fetchCountUsers()
        for i in range(7):
            user_info[i] = {}
            try:
                id_number = db.fetchListUser()['id']
                level = db.fetchListUser()['level']
                users = db.fetchListUser()['username']
                email = db.fetchListUser()['email']
                foldername = db.fetchListUser()['folder_name']
            except:
                return render_template('404.html')
            user_info[i]['id'] = id_number
            user_info[i]['level'] = level
            user_info[i]['users'] = users
            user_info[i]['email'] = email
            user_info[i]['foldername'] = foldername
        return render_template('userlist.html', users=user_info)
    return redirect(url_for('login'))
"""

#Ruta de los usuarios normales
@app.route('/home')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dir_list'))
    return redirect(url_for('login'))

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>', methods = ['GET', 'POST'])
def dir_list(req_path):
    global BASE_DIR
    global abs_path_folder
    dir_folders = {}
    dir_files = {}
    if 'loggedin' in session:
        """
        if (db.fetchCheckUser(session['id'], session['username'])['level'] == 'administrator'):
            # Redirect to admin page
            return redirect(url_for('admin'))
        """
        user_folder = f"{BASE_DIR}{session['foldername']}\\"
        abs_path = os.path.join(user_folder, req_path).replace('/', '\\')
        if len(abs_path_folder) == 10:
            abs_path_folder = []
        if os.path.isdir(abs_path):
            abs_path_folder.append(abs_path)
        if os.path.isfile(abs_path):
            return send_file(abs_path)
        files = os.listdir(abs_path)
        for f in files:
            if f != '':
                try:
                    abs_file_path = os.path.abspath(abs_path + '\\' + f)
                    dir_stats = os.stat(abs_file_path)
                    if os.path.isdir(abs_file_path):
                        # Pruebas
                        dir_folders[f] = {}
                        try:
                            datetime_creation = datetime.fromtimestamp(dir_stats.st_ctime).strftime('%H:%M:%S %d-%m-%Y')
                            datetime_modification = datetime.fromtimestamp(dir_stats.st_mtime).strftime('%H:%M:%S %d-%m-%Y')
                        except:
                            datetime_creation = '---'
                            datetime_modification = '---'
                        dir_folders[f]['name'] = f
                        dir_folders[f]['ctime'] = datetime_creation
                        dir_folders[f]['mtime'] = datetime_modification
                        #dir_folders.append(folder_information)
                    elif os.path.isfile(abs_file_path):
                        # Pruebas
                        dir_files[f] = {}
                        try:
                            datetime_creation = datetime.fromtimestamp(dir_stats.st_ctime).strftime('%H:%M:%S %d-%m-%Y')
                            datetime_modification = datetime.fromtimestamp(dir_stats.st_mtime).strftime('%H:%M:%S %d-%m-%Y')
                            file_size = size(dir_stats.st_size)
                        except:
                            datetime_creation = '---'
                            datetime_modification = '---'
                            file_size = '---'
                        dir_files[f]['name'] = f
                        dir_files[f]['ctime'] = datetime_creation
                        dir_files[f]['mtime'] = datetime_modification
                        dir_files[f]['size'] = file_size
                        #dir_files.append(file_information)
                    else:
                        return render_template('404.html')
                except:
                    return render_template('404.html')
        return render_template('content.html', dir_files=dir_files, dir_folders=dir_folders, abs_path_folder=abs_path_folder)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods = ['GET', 'POST'])
def upload_files():
    global abs_path_folder
    try:
        if request.method == 'POST':
                f = request.files.getlist('file')
                if f[0]:
                    for file in f:
                        file.save(f'{abs_path_folder[-1]}\\{secure_filename(file.filename)}')
                    abs_path_folder = []
                    return redirect(url_for('dir_list'))
                else:
                    return redirect(url_for('dir_list'))
    except:
        return render_template('404.html')

@app.route('/create', methods = ['GET', 'POST'])
def create_folder():
    global abs_path_folder
    try:
        if request.method == 'POST':
            name = request.form.get('text')
            name_folder = os.path.join(abs_path_folder[-1], name)
            if name != '' and os.path.exists(name_folder) == False:
                os.mkdir(name_folder)
                abs_path_folder = []
                return redirect(url_for('dir_list'))
            else:
                return render_template('404.html')
    except:
        return render_template('404.html')

if __name__ == '__main__':
     context = ssl.Context(SSL.PROTOCOL_TLS_SERVER)
     context.load_cert_chain('/home/Username/myhomecloud/certs/key.pem', '/home/Username/myhomecloud/certs/cert.pem')
     app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)
