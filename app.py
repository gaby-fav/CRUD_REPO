# CONTROLADOR
# En carpeta templates va la vista

from time import time
from flask import Flask, request
from flask import render_template, request
from flaskext.mysql import MySQL
from datetime import datetime

# punto de entrada de la aplicación.- siempre es igual
app = Flask(__name__)

# Configuracion de base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema22072'
mysql.init_app(app)

# enrutamientos
@app.route('/')
def index():
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'DATO DE PRUEBA 2', 'CORREOPRUEBA2@GMAIL.COM', 'FOTO2.JPG');"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')  #carga el template

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route("/store", methods=['POST'])
def storage():
    _nombre = request.form ['txtNombre']
    _correo = request.form ['txtCorreo']
    _foto = request.files ['txtFoto']

    now = datetime.now()
    time = now.strftime('%Y%H%M%S')

    if _foto.filename != '':
        nuevoNombreFoto = time + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre , _correo , nuevoNombreFoto)
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return render_template('empleados/index.html')

if __name__=='__main__':
    app.run(debug=True)
