import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, session, Response, abort, current_app
from flask_mysqldb import MySQL
from functools import wraps


import requests # esto de de Jhosep
from deep_translator import GoogleTranslator







app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='panose0506'
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
        _username = request.form['txtusername']
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
    username = request.form['txtusername']
    password = request.form['txtpassword']

    cur = mysql.connection.cursor()

    cur.execute('SELECT usuario FROM usuarios WHERE usuario = %s', (username,))
    usuario_existente = cur.fetchone()

    if usuario_existente:
        return render_template('Registro.html', mensaje='El usuario que ingresó ya se encuentra registrado')

    cur.execute('INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)',(username, password))
    mysql.connection.commit()
    return render_template('login.html', mensaje='Usuario y contraseña registrados correctamente')




@app.route('/QuickRecipe', methods=["GET", "POST"])
@login_requerido
def QuickRecipe():
    recetas = []
    if request.method == "POST":
        ingrediente = GoogleTranslator(source='es', target='en').translate(request.form.get("ingrediente"))
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={ingrediente}"
        response = requests.get(url)
        data = response.json()
        comidas = data.get("meals")

        if comidas:
            for comida in comidas:
                comida["strCategory"] = GoogleTranslator(source='auto', target='es').translate(comida["strCategory"])
                comida["strInstructions"] = GoogleTranslator(source='auto', target='es').translate(comida["strInstructions"])
            recetas = comidas
        else:
            print("No se encontraron recetas para:", ingrediente)
    return render_template("Mipgn.html", recetas=recetas)


@app.route('/comentarios', methods=['GET', 'POST'])
def comentarios():

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        comentario = request.form.get('comentario')
        usuario_id = session.get('id')
        usuario = session.get('usuario')

        if comentario:
            cur.execute('INSERT INTO comentarios (usuario_id, usuario, comentario) VALUES (%s, %s, %s)', (usuario_id, usuario, comentario))
            mysql.connection.commit()
            return render_template('comentarios.html', mensaje='Comentario enviado correctamente, gracias por ayudarnos a mejorar 💖')

    # Obtener comentarios con nombre del usuario
    cur.execute('''
        SELECT comentarios.comentario, usuarios.usuario 
        FROM comentarios 
        JOIN usuarios ON comentarios.usuario_id = usuarios.id
    ''')
    comentarios = cur.fetchall()

    return render_template('comentarios.html', comentarios=comentarios)



def status_401(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def status_404(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True, threaded=True)
