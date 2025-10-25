from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


@app.route('/index')
def index():
    titulo="IEVN1003 - PWA"
    listado=["opera 1", "opera 2", "Opera 3"]
    return render_template('index.html', titulo=titulo, listado=listado)


@app.route('/about')
def about():
    return "<h1>Esta es la página About.</h1>"


@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} | Nombre: {}".format(id, username)


@app.route("/numero/<int:n>")
def numero(n):
    return "Número: {}".format(n)


@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "La suma es: {}".format(n1 + n2)


@app.route("/prueba")
def prueba():
    return '''
    <h1>Prueba de HTML</h1>
    <p>Esto es un párrafo</p>
    <ul>
        <li>Elemento 1</li>
        <li>Elemento 2</li>
        <li>Elemento 3</li>
    </ul>
    '''

@app.route("/operas", methods=['GET', 'POST'])
def operas():
 if request.method=='POST':
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    resultado=x1+x2
    return render_template('operas.html', resultado=resultado)

@app.route("/distancia")
def distancia():
    return render_template('distancia.html')


@app.route("/layout")
def layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)
