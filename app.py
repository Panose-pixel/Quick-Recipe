import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_mysqldb import MySQL

import requests # esto de de Jhosep
from deep_translator import GoogleTranslator







app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='panose0506'
app.config['MYSQL_DB']='flask_app'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)




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



@app.route('/Registro')
def registro():
    return render_template('Registro.html')



@app.route('/QuickRecipe', methods=["GET", "POST"])
def QuickRecipe():
    recetas = []
    if request.method == "POST":
        ingrediente = request.form.get("ingrediente")
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




def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(debug=True, threaded=True)

