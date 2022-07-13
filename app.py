# CONTROLADOR
# En carpeta templates va la vista

from flask import Flask, redirect, request
from flask import render_template, request
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

# punto de entrada de la aplicación.- siempre es igual
app = Flask(__name__)

# Configuracion de base de datos
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema22072'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

# enrutamientos
#para mostrar la foto en el html
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)



@app.route('/')
def index():
    sql = "SELECT * FROM `empleados`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql) 
    empleados = cursor.fetchall() #trae todo y lo mete en una tupla
    conn.commit()

    return render_template('empleados/index.html', empleados = empleados)  #carga el template

@app.route('/update' , methods = ['POST'])
def update():
    _id = request.form['txtId']
    _nombre = request.form ['txtNombre']
    _correo = request.form ['txtCorreo']
    _foto = request.files ['txtFoto']

    sql= "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    datos=(_nombre, _correo, _id)
    conn= mysql.connect()
    cursor=conn.cursor()
    now = datetime.now()
    time = now.strftime('%Y%H%M%S')

    if _foto.filename != '':
        nuevoNombreFoto = time + _foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)

    #BORRAR FOTO ANTERIOR: Me traigo el nombre de la foto guardada y luego la borro
    cursor.execute('SELECT foto FROM empleados WHERE id=%s', _id)
    fila = cursor.fetchone()
    os.remove(os.path.join(app.config['CARPETA'],fila[0]))
    cursor.execute('UPDATE empleados SET foto=%s WHERE id=%s',(nuevoNombreFoto, _id))

    cursor.execute(sql,datos) 
    empleados = cursor.fetchall() #trae todo y lo mete en una tupla
    conn.commit()

    return redirect('/')


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

    return redirect('/')

@app.route("/delete/<int:id>")
def delete(id):
    conn= mysql.connect()
    cursor=conn.cursor()
    #busco nombre de la foto y la elimino de la carpeta uploads antes de borrar registro en bbdd
    cursor.execute('SELECT foto FROM empleados WHERE id=%s', id)
    fila = cursor.fetchone()
    os.remove(os.path.join(app.config['CARPETA'],fila[0]))
    cursor.execute("DELETE FROM empleados WHERE id=%s" , (id)) 
    conn.commit()

    return redirect('/')

@app.route("/edit/<int:id>")
def edit(id):
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id)) 
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()

    return render_template('empleados/edit.html', empleados = empleados)



if __name__=='__main__':
    app.run(debug=True)
