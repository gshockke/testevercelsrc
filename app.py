from flask import Flask, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL


def create_app():
    from app import routes
    routes.init_app(app)
    return app

app = Flask('__name__')

# conexão com o banco de dados
app.config['MYSQL_Host'] = 'localhost' # 127.0.0.1
app.config['MYSQL_USER'] = 'ubuntu'
app.config['MYSQL_PASSWORD'] = 'lequinha'
app.config['MYSQL_DB'] = 'dbdesafio3jean'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quem_somos')
def quem_somos():
    return render_template('quem_somos.html')


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        email = request.form['email']
        assunto = request.form['assunto']
        descricao = request.form['descricao']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contato(ctto_email, ctto_assunto, ctto_descricao) VALUES (%s, %s, %s)", (email, assunto, descricao))
       
        mysql.connection.commit()
        
        cur.close()

        return 'Dados cadastrados com sucesso'
    return render_template('contato.html')


# rota usuários para listar todos os usuário no banco de dados.
@app.route('/users')
def users():
    cur = mysql.connection.cursor()

    users = cur.execute("SELECT * FROM contato")

    if users != '':
        userDetails = cur.fetchall()

        return render_template('contatos.html', userDetails=userDetails)

if __name__ == '_main_': app.run(host='0.0.0.0')
   
