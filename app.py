#CONTROLADOR
#En carpeta templates va la vista

from flask import Flask
from flask import render_template

#punto de entrada de la aplicación.- siempre es igual
app = Flask(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema22072'
mysql.init_app(app)

#enrutamientos
@app.route('/')
def index():
    return render_template('empleados/index.html')  #carga el template

if __name__=='__main__':
    app.run(debug=True)