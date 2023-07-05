from django.contrib import admin

from app.models import Paciente, client, UserInformation, Suscripcion, Product, Citas


# Register your models here.
admin.site.register(client)
admin.site.register(UserInformation)
admin.site.register(Paciente)
admin.site.register(Suscripcion)
admin.site.register(Product)
admin.site.register(Citas)