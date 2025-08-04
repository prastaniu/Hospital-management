from flask_mysqldb import MySQL

mysql = MySQL()
def init_db(app):
    app.config['MYSQL_HOST'] = '127.0.0.1' #'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'hospital_management'
    app.config['MYSQL_PORT'] = 3307
    mysql.init_app(app)
