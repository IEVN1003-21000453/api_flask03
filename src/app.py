from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)
CORS(app, resources={r"/alumnos/*": {"origins": "http://127.0.0.1:5000"}})

conexion = MySQL(app)

@app.route('/alumnos', methods=['GET'])
def listar_alumnos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursor.close()

        alumnos = []
        for fila in datos:
            alumno = {
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
            alumnos.append(alumno)

        return jsonify({'alumnos': alumnos, 'mensaje': 'Alumnos encontrados', 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f'Error al listar alumnos: {str(ex)}', 'exito': False})


@app.route('/alumnos/<mat>', methods=['GET'])
def leer_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado', 'exito': True})
        else:
            return jsonify({'mensaje': 'Alumno no encontrado', 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': f'Error: {str(ex)}', 'exito': False})


@app.route('/alumnos/', methods=['POST'])
def registrar_alumno():
    try:
        matricula = request.json['matricula']
        alumno = leer_alumno_bd(matricula)

        if alumno:
            return jsonify({'mensaje': "Alumno ya existe, no se puede duplicar", 'exito': False})

        cursor = conexion.connection.cursor()
        sql = """
            INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            request.json['matricula'],
            request.json['nombre'],
            request.json['apaterno'],
            request.json['amaterno'],
            request.json['correo']
        )
        cursor.execute(sql, valores)
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': "Alumno registrado", "exito": True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error al registrar alumno: {str(ex)}", "exito": False})


@app.route('/alumnos/<mat>', methods=['PUT'])
def actualizar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if not alumno:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})

        cursor = conexion.connection.cursor()
        sql = """
            UPDATE alumnos 
            SET nombre = %s, apaterno = %s, amaterno = %s, correo = %s
            WHERE matricula = %s
        """
        valores = (
            request.json['nombre'],
            request.json['apaterno'],
            request.json['amaterno'],
            request.json['correo'],
            mat
        )
        cursor.execute(sql, valores)
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error al actualizar: {str(ex)}", 'exito': False})


@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if not alumno:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})

        cursor = conexion.connection.cursor()
        sql = "DELETE FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (mat,))
        conexion.connection.commit()
        cursor.close()

        return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error al eliminar: {str(ex)}", 'exito': False})


def leer_alumno_bd(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT matricula, nombre, apaterno, amaterno, correo
            FROM alumnos WHERE matricula = %s
        """
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchone()
        cursor.close()

        if datos:
            return {
                'matricula': datos[0],
                'nombre': datos[1],
                'apaterno': datos[2],
                'amaterno': datos[3],
                'correo': datos[4]
            }
        return None
    except Exception:
        return None


def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
