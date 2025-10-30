from flask import Flask, render_template, request
import forms
import math

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


@app.route("/alumnos",methods=['GET', 'POST'])
def alumnos():
    mat = 0
    nom = ""
    ape = ""
    em = ""
    alumnos_clase = forms.UserForm(request.form)
    
    if request.method == 'POST' and alumnos_clase.validate:
        mat = alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape = alumnos_clase.apellido.data
        em = alumnos_clase.correo.data
    
    return render_template(
        'alumnos.html',
        form=alumnos_clase,
        mat=mat,
        nom=nom,
        ape=ape,
        em=em
    )

@app.route("/figuras", methods=['GET', 'POST'])
def figuras():
    form = forms.FigurasForm(request.form)
    area = ""
    figura = ""
    if request.method == 'POST' and form.validate():
        figura = request.form.get('figura')
        v1 = form.valor1.data
        v2 = form.valor2.data

        if figura == 'circulo':
            area = math.pi * (v1 ** 2)
        elif figura == 'triangulo':
            area = (v1 * v2) / 2
        elif figura == 'rectangulo':
            area = v1 * v2
        elif figura == 'pentagono':
            area = (v1 * v2) / 2

    return render_template('figuras.html', form=form, area=area, figura=figura)


@app.route('/index')
def index():
    titulo = "IEVN1003 - PWA"
    listado = ["Opera 1", "Opera 2", "Opera 3"]
    return render_template('index.html', titulo=titulo, listado=listado)


@app.route('/about')
def about():
    return "<h1>Esta es la página About.</h1>"


@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"ID: {id} | Nombre: {username}"


@app.route("/numero/<int:n>")
def numero(n):
    return f"Número: {n}"


@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"La suma es: {n1 + n2}"


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
    resultado = None
    if request.method == 'POST':
        x1 = float(request.form.get('x1', 0))
        x2 = float(request.form.get('x2', 0))
        resultado = x1 + x2
    return render_template('operas.html', resultado=resultado)


@app.route("/distancia")
def distancia():
    return render_template('distancia.html')


@app.route("/layout")
def layout():
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)
