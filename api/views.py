from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect, HttpResponse, get_list_or_404, get_object_or_404
from app.models import client,Paciente
from app.models import Paciente, client, Product, Citas, UserInformation
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
import datetime
from pathlib import Path
from docxtpl import DocxTemplate
from django.core import serializers

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# Importar el rest FRAMEWORK

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

@csrf_exempt
def index(request):
    data = json.loads(request.body)
    user_code = data['code']

    # Realiza la consulta de la base de datos
    paciente = Paciente.objects.filter(cliente__codigo=user_code)
    productos = Product.objects.filter(Q(promocionar_a__codigo=user_code) & Q(activa=True))

    pacientes_serializer = PacienteSerializer(paciente, many=True)
    pacientes_data = pacientes_serializer.data

    productos_serializer = ProductSerializer(productos, many=True)
    productos_data = productos_serializer.data

    if paciente:
        response_data = {
                'msg': "OK",
                'pacientes': pacientes_data,
                'productos': productos_data,
        }
        return JsonResponse(response_data, status=200)
    else:
            # Devuelve una respuesta con estado 400 si no hay productos
        response_data = {
                'msg': "No se encontraron pacientes",
        }
    return JsonResponse(response_data, status=400)
    # except:
    #     response_data = {
    #        'msg': "Ha ocurrido un error",
    #     }
    #     return JsonResponse(response_data, status=400)

@csrf_exempt
def descargar(request):
    
    user = request.GET.get('code')
    paciente_id = request.GET.get('paciente')


    if paciente_id:
        paciente = Paciente.objects.filter(id=paciente_id).all()

    
    else:
        paciente = get_list_or_404(Paciente, cliente__codigo=user) 
    

    base_dir = Path(__file__).parent
    word_template_path = base_dir / "docxmedia/pacientetemplate.docx"
    today = datetime.date.today()
    doc = DocxTemplate(word_template_path)
    context = {
        "DATE": today,
        "pacientes": paciente,
    }

    for p in paciente:
        print(p.citas.all())
    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=paciente.docx'
    doc.save(response)

    return response