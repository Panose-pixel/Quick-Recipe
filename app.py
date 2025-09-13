from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from functools import wraps
import datetime
import pymysql
pymysql.install_as_MySQLdb()


import requests # esto de de Jhosep
from deep_translator import GoogleTranslator







app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='flask_app'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)



# Decorador para verificar si el usuario está logueado
def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get('logueado'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorada


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'txtusername' in request.form and 'txtpassword' in request.form:
        _username = request.form['txtusername'].capitalize()
        _password = request.form['txtpassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s', (_username, _password))
        account = cur.fetchone()

        if account:
            session['logueado'] = True
            session['id'] = account.get('id')
            nombre = account.get('usuario', _username)
            session['usuario'] = nombre
            return redirect(url_for('QuickRecipe'))
        
        else:
            return render_template("login.html", mensaje="Usuario o contraseña incorrectos")
    return render_template("login.html")



@app.route('/Registro', methods=['GET', 'POST'])
def registro():
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
        cur.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)',(username, password))
        mysql.connection.commit()
        redirect(url_for('login'))


    return render_template('login.html', mensaje='Usuario y contraseña registrados correctamente')




@app.route('/QuickRecipe', methods=["GET", "POST"])
def QuickRecipe():
    recetas = []
    if request.method == "POST":
        ingrediente = request.form.get("ingrediente")
        if ingrediente:
            # traducir a inglés para la API
            ingrediente_en = GoogleTranslator(source='es', target='en').translate(ingrediente)
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={ingrediente_en}"
            
            try:
                response = requests.get(url, timeout=5)
                data = response.json()
                comidas = data.get("meals")
            except Exception as e:
                print("Error al conectar con la API:", e)
                comidas = None

            if comidas:
                recetas = []
                for comida in comidas:
                    # aseguramos que no rompa si algún campo viene None
                    categoria = comida.get("strCategory") or ""
                    instrucciones = comida.get("strInstructions") or ""

                    comida["strCategory"] = GoogleTranslator(source='auto', target='es').translate(categoria)
                    comida["strInstructions"] = GoogleTranslator(source='auto', target='es').translate(instrucciones)

                    recetas.append(comida)
            else:
                print("No se encontraron recetas para:", ingrediente)

    return render_template("Mipgn.html", recetas=recetas)



@app.route('/Mis_Recetas')
@login_requerido
def mis_recetas():
    nombre_usuario = session.get('usuario')
    cur = mysql.connection.cursor()

    cur.execute(f'SELECT titulo, imagen, categoria, instrucciones, nombre_usuario FROM recetas_guardadas where nombre_usuario = "{nombre_usuario}"')
    
    recetas_guardadas = cur.fetchall()

    
    return render_template('MisRecetas.html', nombre=nombre_usuario, recetas_guardadas=recetas_guardadas)



@app.route('/procesador', methods=['POST'])
def procesador():
    
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        titulo = request.form['strMeal']
        imagen = request.form['strMealThumb']
        categoria = request.form['strCategory']
        instruciones = request.form['strInstructions']
        nombre_usuario = session.get('usuario')
        
        cur.execute(f"SELECT * FROM recetas_guardadas WHERE titulo = '{titulo}' and nombre_usuario = '{nombre_usuario}';")
        receta_ya_guardada = cur.fetchone()

        if receta_ya_guardada:
            mensaje_de_duplicacion = "Ya has guardado antes esta receta"
            return render_template('/Mipgn.html', mensaje_de_duplicacion=mensaje_de_duplicacion)
        else:
            cur.execute('INSERT INTO recetas_guardadas (titulo, imagen, categoria, instrucciones, nombre_usuario) VALUES (%s, %s, %s, %s, %s)', (titulo, imagen, categoria, instruciones, nombre_usuario))
        mysql.connection.commit()

    return redirect(url_for('QuickRecipe'))


@app.route('/eliminador', methods=['POST'])
def eliminador():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        titulo = request.form['strMeal']
        nombre_usuario = session.get('usuario')

        cur.execute(f"DELETE FROM recetas_guardadas WHERE titulo = '{titulo}' and nombre_usuario = '{nombre_usuario}';")
        mysql.connection.commit()



    return redirect(url_for('mis_recetas'))






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



        if comentario:
            cur.execute('INSERT INTO comentarios (usuario_id, usuario, comentario, fecha, estrellas) VALUES (%s, %s, %s, %s, %s)', (usuario_id, usuario, comentario, fecha_comentario, numero_estrellas))
            mysql.connection.commit()

            cur.execute('''
            SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas
            FROM comentarios 
            JOIN usuarios ON comentarios.usuario_id = usuarios.id
            ''')
            comentarios = cur.fetchall()
            flash('Comentario enviado correctamente, gracias por ayudarnos a mejorar 💖')
        return redirect(url_for('comentarios'))
    # Obtener comentarios con nombre del usuario
    cur.execute('''
        SELECT comentarios.comentario, usuarios.usuario, comentarios.fecha, comentarios.estrellas
        FROM comentarios 
        JOIN usuarios ON comentarios.usuario_id = usuarios.id order by comentarios.fecha DESC 
    ''')
    
    comentarios = cur.fetchall()

    if comentarios:
        media_app = cur.execute('SELECT estrellas FROM comentarios')
        media_app = cur.fetchall()

        print(media_app)
    
        cantidad_de_comentarios = len(media_app)

        nota = 0
        for i in media_app:
            nota = nota + i['estrellas']
            print(i)

        print(nota)
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
