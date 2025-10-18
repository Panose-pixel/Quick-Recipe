import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from functools import wraps
import datetime



app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='panose0506'
app.config['MYSQL_DB']='flask_app'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/creditos')
def creditos_api():
    return redirect('https://www.themealdb.com')



# Decorador para verificar si el usuario está logueado
def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada


def Admin_app(f):
    @wraps(f)
    def verificador_admin(*args, **kwargs):
        if not session.get('admin?'):
            return redirect(url_for('QuickRecipe'))
        return f(*args, **kwargs)
    return verificador_admin




@app.route('/eliminador_recetas_totales', methods=['POST'])
def eliminador_recetas_totales():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        nombre_receta_eliminiar = request.form.get('nombre')
        instrucciones_receta_eliminiar = request.form.get('instrucciones')

        cur.execute('DELETE FROM recetas_totales WHERE nombre = (%s) and instrucciones = (%s)', (nombre_receta_eliminiar, instrucciones_receta_eliminiar))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('administracion'))




@app.route('/administracion', methods=['GET','POST'])
@Admin_app
def administracion():

    cur = mysql.connection.cursor()
    cur.execute('SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas, comentarios.rol FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id order by comentarios.fecha DESC')
    
    comentarios = cur.fetchall()

    #Para evitar borrar recetas importantes
    cur.execute('SELECT * FROM recetas_totales limit 99999 OFFSET 26;') #sin limite y muestra recetas después de la 26
    recetas = cur.fetchall()

    
    if request.method == 'POST':
        nombre_del_que_hizo_el_comentario = str(request.form.get('autor_comentario'))
        contenido_del_comentario = str(request.form.get('contenido_comentario'))

        cur.execute('DELETE FROM comentarios WHERE usuario = (%s) and comentario = (%s)', (nombre_del_que_hizo_el_comentario, contenido_del_comentario))
        
        cur.execute('SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas, comentarios.rol FROM comentarios JOIN usuarios ON comentarios.usuario_id = usuarios.id order by comentarios.fecha DESC')
        comentarios = cur.fetchall()
        mysql.connection.commit()


    nombre_del_admin = session.get('usuario')
    if nombre_del_admin == 'Juanangel':
        Juanangel = True
        Jhosep = False
    else:
        Jhosep = True
        Juanangel = False

    return render_template('administracion.html', Juanangel=Juanangel, Jhosep=Jhosep, comentarios=comentarios, recetas=recetas)


@app.route('/contacto', methods=['POST'])
def contacto():
    if request.method == 'POST':
        cur = mysql.connection.cursor()

        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')

        cur.execute('INSERT INTO contactos(nombre,email,mensaje) VALUES (%s,%s,%s)', (nombre,email,mensaje))
        mysql.connection.commit()

        mensaje = "Mensaje enviado exitosamente, trataremos de responderte luego"
    return render_template('Mipgn.html', mensaje_contacto=mensaje)









@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST' and 'txtusername' in request.form and 'txtpassword' in request.form:
        _username = request.form['txtusername'].capitalize()
        _password = request.form['txtpassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s', (_username, _password))
        account = cur.fetchone() 

        cur.close()


        if account:
            session['logueado'] = True
            session['id'] = account.get('id')
            nombre = account.get('usuario', _username)
            session['usuario'] = nombre

            rol = account['rol'] #captura el rol del ususario (si es admin o usuario corriente)


            if rol == 'admin':
                session['admin?'] = True #si el rol del usuario es admin, se almacenará en caché que su rol es admin y será usado
                #en el decorador para entrar a la página administracion 


            return redirect(url_for('QuickRecipe'))
        
        else:
            return render_template("login.html", mensaje="Usuario o contraseña incorrectos")
        
    return render_template("login.html")



@app.route('/Registro', methods=['GET', 'POST'])
def registro():
    session.clear()
    return render_template('Registro.html')

# Registro conectado con formulario
@app.route('/crear_registro', methods=['POST'])
def crear_registro():
    username = request.form['txtusername'].capitalize()
    password = request.form['txtpassword']

    cur = mysql.connection.cursor()

    cur.execute('SELECT usuario FROM usuarios WHERE usuario = %s', (username,))
    usuario_existente = cur.fetchone()

    if usuario_existente:
        return render_template('Registro.html', mensaje='El usuario que ingresó ya se encuentra registrado')
    else:
        cur.execute('INSERT INTO usuarios (usuario, contraseña, rol) VALUES (%s, %s, %s)',(username, password, "usuario"))
        mysql.connection.commit()
        redirect(url_for('login'))

    cur.close()
    return render_template('login.html', mensaje='Usuario y contraseña registrados correctamente')






@app.route('/QuickRecipe', methods=["GET", "POST"])
@login_requerido
def QuickRecipe():
    cur = mysql.connection.cursor()
    ingrediente = (request.args.get("ingrediente") or "")
    recetas = []
    if ingrediente:
        cur.execute('''
            SELECT * FROM recetas_totales 
            WHERE categoria LIKE %s
            OR ingrediente1 LIKE %s
            OR ingrediente2 LIKE %s
            OR ingrediente3 LIKE %s
            OR ingrediente4 LIKE %s
            OR ingrediente5 LIKE %s
            OR ingrediente6 LIKE %s
            OR ingrediente7 LIKE %s
            OR ingrediente8 LIKE %s
            OR ingrediente9 LIKE %s
            OR ingrediente10 LIKE %s
            OR ingrediente11 LIKE %s
            OR ingrediente12 LIKE %s
            OR ingrediente13 LIKE %s
            OR ingrediente14 LIKE %s
            OR ingrediente15 LIKE %s
            OR ingrediente16 LIKE %s
            OR ingrediente17 LIKE %s
            OR ingrediente18 LIKE %s
            OR ingrediente19 LIKE %s
            OR ingrediente20 LIKE %s
        ''', (f"%{ingrediente}%",)*21)
        recetas = cur.fetchall()
    cur.close()
    return render_template("Mipgn.html", recetas=recetas, ingrediente=ingrediente)







@app.route('/Mis_Recetas')
@login_requerido
def mis_recetas():
    nombre_usuario = session.get('usuario')
    cur = mysql.connection.cursor()

    cur.execute('SELECT id, titulo, img, categoria, instrucciones, video, nombre_usuario FROM recetas_guardadas where nombre_usuario = (%s)', (nombre_usuario))
    
    recetas_guardadas = cur.fetchall()
    
    return render_template('MisRecetas.html', nombre=nombre_usuario, recetas_guardadas=recetas_guardadas)



@app.route('/procesador', methods=['POST'])
def procesador():
    cur = mysql.connection.cursor()
    titulo = request.form['nombre']
    imagen = request.form['img']
    categoria = request.form['categoria']
    instruciones = request.form['instrucciones']
    video = request.form['video']
    nombre_usuario = session.get('usuario')
    ingrediente = (request.form.get('ingrediente') or '').strip()

    cur.execute("SELECT * FROM recetas_guardadas WHERE titulo = %s AND nombre_usuario = %s;", (titulo, nombre_usuario))
    receta_ya_guardada = cur.fetchone()

    if receta_ya_guardada:
        return redirect(url_for('QuickRecipe', ingrediente=ingrediente, mensaje_de_duplicacion="Ya has guardado antes esta receta"))

    cur.execute(
        'INSERT INTO recetas_guardadas (titulo, img, categoria, instrucciones, video, nombre_usuario) VALUES (%s, %s, %s, %s, %s, %s)',
        (titulo, imagen, categoria, instruciones, video, nombre_usuario)
    )
    mysql.connection.commit()
    return redirect(url_for('QuickRecipe', ingrediente=ingrediente, mensaje_exito="Receta guardada"))







@app.route('/eliminador', methods=['POST'])
def eliminador():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        titulo = request.form.get('nombre')
        nombre_usuario = session.get('usuario')

        cur.execute("DELETE FROM recetas_guardadas WHERE titulo = (%s) and nombre_usuario = (%s);", (titulo,nombre_usuario))
        mysql.connection.commit()



    return redirect(url_for('mis_recetas'))


@app.route('/sugerencias', methods=['GET','POST'])
@login_requerido
def sugerencias():
    ingredientes = []
    ingredientes_texto = str('ingrediente1')
    for i in range(2, 21):
        ingredientes.append(request.form.get(f"ingrediente{i}"))

        ingredientes_texto = ingredientes_texto + ', '+ str(request.form.get(f"ingrediente{i}"))
        

    

    if request.method == 'POST':
        cur = mysql.connection.cursor()

        nombre = request.form.get("nombre")
        img = request.form.get("img")
        instrucciones = request.form.get("instrucciones")
        categoria = request.form.get("categoria")
        video = request.form.get("video")
        #ingredientes
        ingrediente1 = request.form.get("ingrediente1")
        ingrediente2 = request.form.get("ingrediente2")
        ingrediente3 = request.form.get("ingrediente3")
        ingrediente4 = request.form.get("ingrediente4")
        ingrediente5 = request.form.get("ingrediente5")
        ingrediente6 = request.form.get("ingrediente6")
        ingrediente7 = request.form.get("ingrediente7")
        ingrediente8 = request.form.get("ingrediente8")
        ingrediente9 = request.form.get("ingrediente9")
        ingrediente10 = request.form.get("ingrediente10")
        ingrediente11 = request.form.get("ingrediente11")
        ingrediente12 = request.form.get("ingrediente12")
        ingrediente13 = request.form.get("ingrediente13")
        ingrediente14 = request.form.get("ingrediente14")
        ingrediente15 = request.form.get("ingrediente15")
        ingrediente16 = request.form.get("ingrediente16")
        ingrediente17 = request.form.get("ingrediente17")
        ingrediente18 = request.form.get("ingrediente18")
        ingrediente19 = request.form.get("ingrediente19")
        ingrediente20 = request.form.get("ingrediente20")

        cur.execute("""INSERT INTO recetas_totales (nombre, img, instrucciones, categoria, video, ingrediente1,ingrediente2, ingrediente3, ingrediente4, ingrediente5,ingrediente6, ingrediente7, ingrediente8, ingrediente9, ingrediente10,ingrediente11, ingrediente12, ingrediente13, ingrediente14, ingrediente15,ingrediente16, ingrediente17, ingrediente18, ingrediente19, ingrediente20) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (nombre, img, instrucciones, categoria, video, ingrediente1, ingrediente2, ingrediente3, ingrediente4, ingrediente5, ingrediente6, ingrediente7, ingrediente8, ingrediente9, ingrediente10, ingrediente11, ingrediente12, ingrediente13, ingrediente14, ingrediente15, ingrediente16, ingrediente17, ingrediente18, ingrediente19, ingrediente20))

        mysql.connection.commit()
        cur.close()
        return redirect(url_for('sugerencias'))

    return render_template('sugerencias.html')






@app.route('/comentarios', methods=['GET', 'POST'])
@login_requerido
def comentarios():

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        comentario = request.form.get('comentario').capitalize() # Coloca en mayúscula la primera letra del comentario
        usuario_id = session.get('id')
        usuario = session.get('usuario')
        fecha_comentario = datetime.datetime.now()
        fecha_comentario = fecha_comentario.strftime('%Y-%m-%d %H:%M:%S') #fecha del comentario
        numero_estrellas = int(request.form.get('rating'))
        
        if session.get('admin?'):
            rol = 'admin'
        else:
            rol = 'usuario'



        if comentario:
            cur.execute('INSERT INTO comentarios (usuario_id, usuario, comentario, fecha, estrellas, rol) VALUES (%s, %s, %s, %s, %s, %s)', (usuario_id, usuario, comentario, fecha_comentario, numero_estrellas, rol))
            mysql.connection.commit()

            cur.execute('''
            SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas, comentarios.rol
            FROM comentarios 
            JOIN usuarios ON comentarios.usuario_id = usuarios.id order by comentarios.fecha DESC
            ''')
            comentarios = cur.fetchall()
            flash('Comentario enviado correctamente, gracias por ayudarnos a mejorar 💖')

        return redirect(url_for('comentarios'))
    # Obtener comentarios con nombre del usuario
    cur.execute('''
        SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas, comentarios.rol
        FROM comentarios 
        JOIN usuarios ON comentarios.usuario_id = usuarios.id order by comentarios.fecha DESC 
    ''')
    
    comentarios = cur.fetchall()

    if comentarios:
        media_app = cur.execute('SELECT estrellas FROM comentarios')
        media_app = cur.fetchall()

    
        cantidad_de_comentarios = len(media_app)

        nota = 0
        for i in media_app:
            nota = nota + i['estrellas']


        if nota and cantidad_de_comentarios:
            media = (nota/cantidad_de_comentarios)
            media = round(media, 2)

    if not media:
        media = False


    return render_template('comentarios.html', comentarios=comentarios, media=media)



def status_401(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def status_404(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True, threaded=True)
