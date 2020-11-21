#Vamos a realizar las importaciones de los modulos descargados
#En primer lugar importaremos Flask
from flask import Flask, render_template, request, url_for, redirect, flash

#Importaremos el modulo para MySQL
from flask_mysqldb import MySQL

#Iniciaremos nuestro proyecto de flask
app = Flask(__name__)

#Realizaremos la conexion a la base de MySQL
#Primero daremos nuestro host para la conexion
app.config['MYSQL_HOST'] = 'localhost'
#Daremos el ususario
app.config['MYSQL_USER'] = 'root'
#Daremos la contraseña
app.config['MYSQL_PASSWORD'] = ''
#Nombre de la BD (la tenemos que crear en nuestro XAMPP)
app.config['MYSQL_DB'] = 'perfil'

#Crearemos una sesion para mostrar los mensajes (los guardaremos en memoria)
app.secret_key = 'EsUnSecreto...'

#Introduciremos la configuracion
Basesita = MySQL(app)

#Aqui inicia la contruccion de nuestra API
#Para no comenzar con lo mismo de solo ver la advertencia y para avanzar haremos una ruta para comprobar que se se realizo la conexion
#NOTA: Que no se te olvide que una ruta inicia con @
@app.route('/')
def inicio():
    #Para mostrar los datos de nuestra BD a la tabla creada en nuestro INDEX
    #Comenzaremos a enviar los datos a nuestra BD
    Datos = Basesita.connection.cursor()
    #Vamos a realizar consultas de SQL
    Datos.execute('SELECT * FROM usuarios')
    #Ejecutaremos nuestra consulta
    Resul = Datos.fetchall()

    return render_template('index.html', usuarios = Resul)

#Ruta para agregar usuarios
@app.route('/AddUsu', methods = ['POST'])
def POSTusu():
    #Confirmacion de solicitud de metodo POST
    if request.method == 'POST':
        #Solicitaremos los datos de los inputs y los guardamos en una variable
        Nombre = request.form['Nombre']
        Edad = request.form['Edad']
        Ciudad = request.form['Ciudad']

        #Comenzaremos a enviar los datos a nuestra BD
        Datos = Basesita.connection.cursor()
        #Vamos a realizar consultas de SQL
        Datos.execute('INSERT INTO usuarios (Nombre, Edad, Ciudad) VALUES ( %s, %s, %s )', (Nombre, Edad, Ciudad))
        #Ejecutaremos nuestra consulta
        Basesita.connection.commit()

        #Mostraremos un mensaje de confirmacion (de que se agrego el ususario)
        flash('El ususario {} se agrego con exito'.format(Nombre))

        #Siempre tenemos que retornar algo, en nuestro caso nos redireccionaremos al inicio
        #NOTA: En la funcion de "url_for()" dentro de esta meteremos la funcion que pertenece a la ruta (este caso se llama inicio)
        return redirect(url_for('inicio'))

#Ruta para buscar usuarios
@app.route('/BuscUsu/<id>')
def GETusu(id):
    #Antes de editar vamos a realizar un consulta para obtener un usuario y asi editarlo (se editara en una ruta aparte de index)
    Datos = Basesita.connection.cursor()
    #Vamos a realizar la consulta de SQL
    Datos.execute('SELECT * FROM usuarios WHERE id = {}'.format(id))
    #Ejecutaremos nuestra consulta
    Resul = Datos.fetchall()

    #Retornaremos en el HTML creado para edtitar
    return render_template('editar.html', usuario = Resul[0])

#Ruta para editar usuarios
@app.route('/EditUsu/<id>', methods = ['POST'])
def PUTusu(id):
    #Vamos a realizar una condicional para verificar que el procesos se realice correctamente
    if request.method == 'POST':
        #Especificaremos los datos que tomara de referencia para actualizar
        Nombre = request.form['Nombre']
        Edad = request.form['Edad']
        Ciudad = request.form['Ciudad']

        #Comenzaremos a enviar los datos a nuestra BD
        Datos = Basesita.connection.cursor()
        #Vamos a realizar la modificacion de los datos de SQL
        Datos.execute("""UPDATE usuarios 
        SET Nombre = %s, Edad = %s, Ciudad = %s
        WHERE id = %s""", (Nombre, Edad, Ciudad, id))
        #Ejecutaremos nuestra eliminacion de los datos
        Basesita.connection.commit()
        #Enviaremos un mensaje para confirmar que el proceso se realizo
        flash('¡Ah caray!, ¿eres hechicero?, acabas de modificar un usuario')

        #Siempre tenemos que retornar algo, en nuestro caso nos redireccionaremos al inicio
        #NOTA: En la funcion de "url_for()" dentro de esta meteremos la funcion que pertenece a la ruta (este caso se llama inicio)
        return redirect(url_for('inicio'))


#Ruta para eliminar usuarios
@app.route('/DelUsu/<id>')
def DELusu(id):
    #Comenzaremos a enviar los datos a nuestra BD
    Datos = Basesita.connection.cursor()
    #Vamos a realizar la eliminacion de SQL
    Datos.execute('DELETE FROM usuarios WHERE id = {0}'.format(id))
    #Ejecutaremos nuestra eliminacion de los datos
    Basesita.connection.commit()

    #Mensaje de confirmacion
    flash('Le diste un levanton al usuario satisfactoriamente')

    #Siempre tenemos que retornar algo, en nuestro caso nos redireccionaremos al inicio
    #NOTA: En la funcion de "url_for()" dentro de esta meteremos la funcion que pertenece a la ruta (este caso se llama inicio)
    return redirect(url_for('inicio'))




#Arrancaremos nuestro proyecto de flask
if __name__ == "__main__":
    #Solo usaremos la opcion debug, podemos cambiar el puerto pero pues no lo haremos
    app.run(port = 8089 ,debug = True)