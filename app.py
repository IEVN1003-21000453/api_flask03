from flask import Flask, render_template, request, make_response, jsonify
import forms
import math
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"


@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    alumnos_clase = forms.UserForm(request.form)
    estudiantes = []  

    if request.method == 'POST' and alumnos_clase.validate():
       
        mat = alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape = alumnos_clase.apellido.data
        em = alumnos_clase.correo.data

        datos = {
            "matricula": mat,
            "nombre": nom,
            "apellido": ape,
            "correo": em
        }

        datos_str = request.cookies.get('estudiante')
        if datos_str:
            try:
                estudiantes = json.loads(datos_str) 
            except json.JSONDecodeError:
                estudiantes = []
        else:
            estudiantes = []

        
        estudiantes.append(datos)


        response = make_response(render_template(
            'alumnos.html',
            form=alumnos_clase,
            estudiantes=estudiantes,
            mat=mat,
            nom=nom,
            ape=ape,
            em=em
        ))
        response.set_cookie('estudiante', json.dumps(estudiantes))
        return response

    return render_template('alumnos.html', form=alumnos_clase)


@app.route("/get_cookie")
def get_cookie():
    datos_str = request.cookies.get('estudiante')
    if not datos_str:
        return "No hay cookie guardada."
    try:
        datos = json.loads(datos_str)
    except json.JSONDecodeError:
        return "Error: la cookie está dañada o vacía."
    return jsonify(datos)


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
        try:
            x1 = float(request.form.get('x1', 0))
            x2 = float(request.form.get('x2', 0))
            resultado = x1 + x2
        except ValueError:
            resultado = "Error: ingresa solo números."
    return render_template('operas.html', resultado=resultado)


@app.route("/distancia")
def distancia():
    return render_template('distancia.html')


@app.route("/layout")
def layout():
    return render_template('layout.html')


@app.route('/pizzas', methods=['GET', 'POST'])
def pizzas():
    cliente_form = forms.ClienteForm(request.form)
 
    pizzas_lista = []
    ventas_lista = []
    total_general = 0
 
    cookie_pizzas = request.cookies.get('pizzas')
    if cookie_pizzas:
        pizzas_lista = json.loads(cookie_pizzas)
 
    cookie_ventas = request.cookies.get('ventas')
    if cookie_ventas:
        ventas_lista = json.loads(cookie_ventas)
        total_general = sum(v['total'] for v in ventas_lista)
 
   
    if 'agregar' in request.form:
        tamano = request.form.get('tamano')
        ingredientes = request.form.getlist('ingredientes')
        cantidad = int(request.form.get('cantidad', 1))
 
        precios = {'chica': 40, 'mediana': 80, 'grande': 120}
       
        subtotal = precios[tamano.lower()] * cantidad + len(ingredientes) * 10 * cantidad
 
        nueva_pizza = {
            'tamano': tamano.capitalize(),
            'ingredientes': ', '.join([i.capitalize() for i in ingredientes]) if ingredientes else 'Ninguno',
            'cantidad': cantidad,
            'subtotal': subtotal
        }
        pizzas_lista.append(nueva_pizza)
 
        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=pizzas_lista,
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('pizzas', json.dumps(pizzas_lista))
        return response
 
   
    if 'quitar' in request.form:
        index = int(request.form['quitar'])
        if 0 <= index < len(pizzas_lista):
            del pizzas_lista[index]
 
        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=pizzas_lista,
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('pizzas', json.dumps(pizzas_lista))
        return response
 
   
    if 'terminar' in request.form and cliente_form.validate():
        total = sum(p['subtotal'] for p in pizzas_lista)
        nombre = cliente_form.nombre.data
        direccion = cliente_form.direccion.data
        telefono = cliente_form.telefono.data
 
        venta = {
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'total': total
        }
 
        ventas_lista.append(venta)
        total_general = sum(v['total'] for v in ventas_lista)
 
        response = make_response(render_template('pizzas.html',
                                                 cliente_form=cliente_form,
                                                 pizzas=[],
                                                 ventas=ventas_lista,
                                                 total_general=total_general))
        response.set_cookie('ventas', json.dumps(ventas_lista))
        response.set_cookie('pizzas', json.dumps([]))
        return response
 
    return render_template('pizzas.html',
                           cliente_form=cliente_form,
                           pizzas=pizzas_lista,
                           ventas=ventas_lista,
                           total_general=total_general)

if __name__ == '__main__':
    app.run(debug=True)
