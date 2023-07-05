from django.shortcuts import render, redirect, HttpResponse, get_list_or_404
from app.models import client,Paciente
from app.models import Paciente, client, Product, Citas, UserInformation
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout 
import datetime
from pathlib import Path
from docxtpl import DocxTemplate

#Decorators
from .helpers import session_required

# Create your views here.

@session_required
def index(request):
    try:
        user = request.session['code']
        paciente = Paciente.objects.filter(cliente__codigo=user)
        
        productos = Product.objects.filter(
            Q(promocionar_a__codigo = user) & Q(activa=True))
        if productos:
                  return render(request, "mobile/page-home.html", {
            'productos': productos,
            'user': productos[0].user, 
            'pacientes': paciente, 
            'cliente': paciente[0].cliente,
            })
        else:
            return render(request, "mobile/page-home.html", {
            'pacientes': paciente, 
            'cliente': paciente[0].cliente,
        
      

        })
    except:
        messages.error(request, "Su veterinario no ha registrado sus mascotas, aún no puedes utilizar CaniPet.")
        return redirect("login_mobile")

def login(request):
    logout(request)
    if request.method == "POST":
        codigo = request.POST["codigo"]
        if not codigo:
            messages.error(request, "Rellene el campo de Código.")
            return redirect("login_mobile")
        try:
            user = client.objects.get(codigo=codigo)
            request.session['code'] = codigo
            return redirect(to="index")
        except:
            messages.error(request, "Código no coincide.")
            return redirect("login_mobile")
    else:
        return render(request, "mobile/page-login.html")

def bienvenida(request):
    return render(request, "mobile/bienvenida.html")

def logout(request):
    request.session['code'] = None
    return redirect("login_mobile")

@session_required
def ver_perfil(request, id):
    user = request.session['code']
    try:
        paciente = Paciente.objects.filter(
            Q(cliente__codigo=user) & Q(id=id)
            )[0]

        return render(request, "mobile/page-user-profile.html", {
            'paciente': paciente
        })
    except:
        return redirect("index")

@session_required
def product_detail(request, id):
    try:
        product = Product.objects.filter(
            Q(promocionar_a__codigo = request.session["code"]) & Q(id=id)
        ).first()

        productos = Product.objects.filter(
            Q(promocionar_a__codigo = request.session["code"]) & Q(activa=True)).exclude(id=id)

        return render(request, "mobile/page-product.html", {
        'product': product,
        'productos': productos
        })
    except:
        return redirect(to="index")

@session_required
def descargar(request):

    user = request.session['code']
    paciente = get_list_or_404(Paciente, cliente__codigo=user) 
    citas = Citas.objects.filter(
        Q(paciente__cliente__codigo=user) & Q(activa=True)).order_by("-fecha_cita")
    
    base_dir = Path(__file__).parent
    word_template_path = base_dir / "docxmedia/pacientetemplate.docx"
    today = datetime.date.today()
    doc = DocxTemplate(word_template_path)
    context = {
    "DATE": today,
    "pacientes": paciente,
    "citas": citas, 
    }
    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=paciente.docx'
    doc.save(response)

    return response


@session_required
def citas_cliente(request):
    user = request.session["code"]
    citas = Citas.objects.filter(
        Q(paciente__cliente__codigo=user) & Q(activa=True)).order_by("-fecha_cita")
    
    
    return render(request, "mobile/citas.html", {
        'citas': citas
    })


@session_required
def clinicas(request):
    user = request.session["code"]
    clinicas = UserInformation.objects.all()


    return render(request, "mobile/clinicas.html", {
        'clinicas': clinicas
    })


@session_required
def perfil_veterinaria(request, id):
    clinicas = UserInformation.objects.filter(id = id)[0]
    Client2 = client.objects.filter(codigo=request.session["code"])[0]
    #print(clinicas)
     
    return render(request, "mobile/perfil_veterinario.html", {
        'clinicas': clinicas,
        'Client': Client2,
        
    })

@session_required
def coment_perfil(request):
    if request.method == 'POST':
        pass
    else:
        return HttpResponseNotFound('404')

@session_required
def veterinarias(request):
    if request.method == 'POST':
        pass
    else: 
        clinicas = UserInformation.objects.all()
      
        return render(request, "mobile/veterinarias.html", {
            "clinicas": clinicas,
        })
