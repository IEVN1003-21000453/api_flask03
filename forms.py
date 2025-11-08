from wtforms import Form, StringField, FloatField, EmailField, PasswordField, IntegerField, SelectField, SelectMultipleField
from wtforms import validators

class UserForm(Form):
    matricula = IntegerField('Matrícula', [
        validators.DataRequired(message="La matrícula es obligatoria")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es obligatorio")
    ])
    apellido = StringField('Apellido', [
        validators.DataRequired(message="El apellido es obligatorio")
    ])
    correo = EmailField('Correo', [
        validators.DataRequired(message="El correo es obligatorio"),
        validators.Email(message="Debe ser un correo válido")
    ])


class FigurasForm(Form):
    valor1 = IntegerField(
        'Valor 1',
        [validators.DataRequired(message="Ingresa el primer valor")]
    )

    valor2 = IntegerField(
        'Valor 2 (si aplica)',
        [validators.Optional()]
    )


class ClienteForm(Form):
    nombre = StringField('Nombre completo', [validators.DataRequired()])
    direccion = StringField('Dirección', [validators.DataRequired()])
    telefono = StringField('Teléfono', [
        validators.DataRequired(),
        validators.Length(min=8, max=15, message="Número de teléfono no válido")
    ])
   
class PizzaForm(Form):
    tamano = SelectField('Tamaño', choices=[
        ('chica', 'Chica'),
        ('mediana', 'Mediana'),
        ('grande', 'Grande')
    ], validators=[validators.DataRequired()])
 
    ingredientes = SelectMultipleField('Ingredientes', choices=[
        ('jamon', 'Jamón'),
        ('piña', 'Piña'),
        ('champiñones', 'Champiñones')
    ])
 
    cantidad = IntegerField('Número de pizzas', [validators.DataRequired()])
 