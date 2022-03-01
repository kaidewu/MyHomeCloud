from flask import Flask, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

#
abs_path_env = os.path.abspath('config.env')
load_dotenv('abs_path_env')