from django.db import models
from django.contrib.auth.models import User
from datetime import *
from django.utils.crypto import get_random_string
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


cedula_validator = RegexValidator(
    regex=r"^\d{3}-\d{6}-\d{4}[A-Z]$",
    message="La cédula no tiene el formato correcto (Ejemplo: 001-030725-1040G)",
)

def non_negative_validator(value):
    if value < 0:
        raise ValidationError('Introduzca un valor correcto')
    

class client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cedula = models.CharField(max_length=20, validators=[cedula_validator], null=True)
    nombre = models.CharField(max_length = 25)
    apellido = models.CharField(max_length=25, null=True)
    email = models.EmailField()
    telefono = models.CharField(max_length = 25, null=True, blank=True)
    direccion = models.CharField(max_length = 50, null=True, blank=True)
    codigo = models.CharField(max_length=7,default=get_random_string(length=7).upper(), editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"


SEXO = [
    ('Macho', 'Macho'),
    ('Hembra', 'Hembra'),

]

ESTADOS_CITA = (
        ('pendiente', 'Pendiente'),
        ('pasada', 'Pasada'),
    )


class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_clinica = models.CharField(max_length = 25, null=True, blank=True)
    lat = models.CharField(max_length = 50, null=True, blank=True)
    lon = models.CharField(max_length = 50, null=True, blank=True)
    pacientes_restantes = models.IntegerField(default=2)
    updated_at = models.DateTimeField(auto_now=True)

class Paciente(models.Model):
    nombre = models.CharField(max_length = 25)
    foto = models.ImageField(upload_to='images/', null=True, blank=True)
    cliente = models.ForeignKey(client, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    sexo = models.TextField(choices=SEXO,null=True, blank=True)
    raza = models.CharField(max_length=20, null=True, blank=True)
    peso = models.DecimalField(null=True, blank=True, validators=[non_negative_validator], decimal_places=2, max_digits=10)
    castrado = models.BooleanField(null=True,blank=True, default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"{self.nombre} que pertenece a {self.cliente}"

    def get_years(self):
        return date.today().year - self.fecha_nacimiento.year
    
class Citas(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    motivo = models.TextField()
    # examen_fisico = models.TextField()
    # diagnostico_preliminar = models.TextField()
    # patologia = models.CharField(max_length = 25)
    fecha_cita = models.DateField(null=True)
    hora = models.TimeField(null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)  


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(validators=[non_negative_validator], max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    promocionar_a = models.ManyToManyField(client, blank=True)
    descuento = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, validators=[non_negative_validator])
    activa = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)  

        

class Suscripcion(models.Model):
    name = models.CharField(max_length=25)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=5)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{price: .2f}".format(price = self.price/100)
