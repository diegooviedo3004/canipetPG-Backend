from django.shortcuts import get_object_or_404, render, redirect   
from django.http import HttpResponseNotFound, HttpResponse
from django.contrib import messages
from datetime import datetime


# Ordering
from datetime import datetime, timedelta
from django.db.models import Sum

# AUTH
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
# Forms
from .forms import ClientForm, PacienteForm, CitasForm, ProductForm
from .models import (Paciente, client, UserInformation, Citas, Suscripcion, Product)
from django.core.mail import send_mail

#Email
from django.conf import settings 
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, send_mail
from werkzeug.security import generate_password_hash

# Decorators
from .helpers import datos_ya_ingresados

# Stripe
import stripe
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required(login_url='login_view')
@datos_ya_ingresados
def index(request):
    return render(request, 'app.html', {
        "citas": Citas.objects.filter(user=request.user).count(),
        "pacientes_restantes" : UserInformation.objects.filter(user=request.user).first().pacientes_restantes,
    })

def home(request):
    return render(request, 'landingP.html')

@login_required(login_url='login_view')
@datos_ya_ingresados
def clientes(request):
    return render(request, 'clientes/index.html', {
        "data" : client.objects.filter(user=request.user).all() 
    })

@login_required(login_url='login_view')
@datos_ya_ingresados
def citas(request):
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    citas = Citas.objects.filter(user=request.user).all(),
    for cita in citas:
        print(cita)
    return render(request, 'citas/index.html', {
        "data" : Citas.objects.filter(user=request.user).all(), 
        "current_time": current_time,
        "current_date": current_date
    })

@login_required(login_url='login_view')
@datos_ya_ingresados
def crear_citas(request):
    form = CitasForm(request.POST or None)
    form.fields['paciente'].queryset = Paciente.objects.filter(cliente__user = request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('citas')
    context = {
        "form" : form
    }
    return render(request, 'citas/create.html', context)

@login_required(login_url='login_view')
@datos_ya_ingresados
def pacientes(request):
    return render(request, 'pacientes/index.html', {
        "data" : Paciente.objects.filter(cliente__user=request.user).all() 
    })


@login_required(login_url='login_view')
@datos_ya_ingresados
def client_profile(request, pk):
    try:
        obj = client.objects.get(id=pk)
        mascotas = obj.paciente_set.all()
    except:
        return HttpResponseNotFound("Not found")

    if request.user != obj.user:
        return HttpResponseNotFound("Not found")

    return render(request, 'clientes/profile.html', {
        'client' : obj,
        'mascotas': mascotas
    })

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login_view')
@datos_ya_ingresados
def crear_paciente(request):
    form = PacienteForm(request.POST or None, request.FILES or None)
    form.fields['cliente'].queryset = client.objects.filter(user = request.user)
    if request.method == "POST":
        if form.is_valid():
            information = UserInformation.objects.filter(user=request.user).first()
            if information.pacientes_restantes >= 1:
                form.save()
                information.pacientes_restantes -= 1
                information.save()
                return redirect('pacientes')
            else:
                messages.error(request, 'No cuentas con más pacientes disponibles. Compra más en el apartado "Comprar pacientes"')
                return redirect('pacientes')

    return render(request, 'pacientes/create.html', {
        'form' : form
    })

@login_required(login_url='login_view')
@datos_ya_ingresados
def editar_paciente(request, pk):
    try:
        paciente = Paciente.objects.get(id=pk)
    except:
        return HttpResponseNotFound("Not found")

    form = PacienteForm(instance=paciente)

    if request.user != paciente.cliente.user:
        return HttpResponseNotFound("Not allowed to be here")

    form.fields['cliente'].queryset = client.objects.filter(user = request.user)
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES or None, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    return render(request, 'pacientes/create.html', {
        'form' : form
    })


@login_required(login_url='login_view')
@datos_ya_ingresados
def editar_cita(request, pk):
    try:
        cita = Citas.objects.get(id=pk)
    except:
        return HttpResponseNotFound("Not found")

    form = CitasForm(instance=cita)

    if request.user != cita.user:
        return HttpResponseNotFound("Not allowed to be here")

    form.fields['paciente'].queryset = Paciente.objects.filter(cliente__user = request.user)
    if request.method == "POST":
        form = CitasForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('citas')
    return render(request, 'pacientes/create.html', {
        'form' : form
    })

@login_required(login_url='login_view')
@datos_ya_ingresados
def create_user(request):
    form = ClientForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            if client.objects.filter(cedula=cedula).exists():
                messages.error(request, "Introduzca una cédula no existente")
                return redirect(to="create_user")
            form.instance.user = request.user
            form.save()
            return redirect('clientes')
    context = {
        "form" : form
    }
    return render(request, 'clientes/create.html', context)

@login_required(login_url='login_view')
@datos_ya_ingresados
def editar_cliente(request, pk):
    try:
        cliente = client.objects.get(id=pk)
    except:
        return HttpResponseNotFound("Not found")

    form = ClientForm(instance=cliente)

    if request.user != cliente.user:
        return HttpResponseNotFound("Not allowed to be here")

    if request.method == "POST":
        form = ClientForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')
    return render(request, 'clientes/create.html', {
        'form' : form
    })

def login_page(request):
    page = 'Login'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' or password == '':
            messages.error(request, 'Introduzca datos')
            return redirect(to='login_view')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to='app')
        else:
            messages.error(request, 'Activa tu correo o ingrese correctamente sus credenciales')
            return redirect(to='login_view')

    return render(request, 'login_register.html', context)

def register_page(request):
    page = 'Register'
    context = {'page': page}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, 'Datos incorrectos o usuario registrado')
                return redirect(to="register")
            elif User.objects.filter(email=email).exists():
                messages.error(
                    request, 'Datos incorrectos o usuario registrado')
                return redirect(to="register")
            else:
        
                cifrado = generate_password_hash(username)
                cifrado = cifrado[15:]
                send_mail(email, username, cifrado)

                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=cifrado, last_name= "veterinario", is_active=False)
                messages.success(request, 'Se ha creado el usuario de forma satisfactoria, confirme su correo electronico')

                
                return redirect(to='login_view')
    else:
        return render(request, 'login_register.html', context)


def send_mail(mail, username, cifrado):

    context = {"url": f"{settings.YOUR_DOMAIN}/register/{cifrado}/", "username": username}
    template = get_template("correo.html")
    content = template.render(context)
    email = EmailMultiAlternatives(
        "Verifica tu correo para empezar a usar Canipet",
        "Canipet",
        settings.EMAIL_HOST_USER,
        [mail]
    )
    email.attach_alternative(content, "text/html")
    email.send()       

def confirmacion_correo(request, hash): 
    try:
        user = User.objects.filter(first_name=hash).first()
        user.is_active = True
        user.save()
        messages.success(request, "Ha confirmado su correo correctamente, ya posee el acceso para iniciar sesiòn")
        return redirect("app")
    except:
        return HttpResponseNotFound("NotFound")
     
def page_not_found_view(request, exception):
    return render(request, "error404.html", status=404)

@login_required(login_url = "login_view")
def step_form(request):
    if request.method == "GET":
        return render(request, "stepForms.html")
    else:
        nombre_vet = request.POST['nombre_veterinaria']
        lat = request.POST['lat']
        lon = request.POST['lng']
        user = UserInformation(user=request.user, nombre_clinica=nombre_vet, lat=lat, lon=lon)
        user.save()
        return redirect('app')

# Stripe views

def checkout_view(request, pk):
    if request.method == "POST":
        try:
            product = Suscripcion.objects.get(id=pk)
            YOUR_DOMAIN = settings.YOUR_DOMAIN
            checkout_session = stripe.checkout.Session.create(
                success_url= YOUR_DOMAIN + "/app/",
                cancel_url= YOUR_DOMAIN + "/app/",
                line_items=[
                    {
                        "price_data" : {
                            "currency" : 'usd',
                            "product_data": {
                                "name" : product.name,
                            },
                            "unit_amount" : product.price
                        },
                        "quantity" : 1,
                    },
                ],
                metadata = {
                    "product_id" : product.id,
                    "user_id" : request.user.id,
                    "quantity" : product.quantity
                },
                mode="payment",
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except:
            return redirect('home')


@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event["data"]["object"]
        
        product_id = session["metadata"]["product_id"]
        user_id = session["metadata"]["user_id"]
        quantity = session["metadata"]["quantity"]


        user = User.objects.get(id=user_id)
        informacion = UserInformation.objects.filter(user=user).first()
        informacion.pacientes_restantes += int(quantity)
        informacion.save()

    return HttpResponse(status=200)

# Products y promociones
@login_required(login_url='login_view')
@datos_ya_ingresados
def crear_producto(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    form.fields['promocionar_a'].queryset = client.objects.filter(user = request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('productos')
    context = {
        "form" : form
    }
    return render(request, 'pacientes/create.html', context)

@login_required(login_url='login_view')
@datos_ya_ingresados
def productos(request):
    return render(request, 'products/index.html', {
        "data" : Product.objects.filter(user=request.user).all() 
    })

@login_required(login_url='login_view')
@datos_ya_ingresados
def editar_producto(request, pk):
    try:
        producto = Product.objects.get(id=pk)
    except:
        return HttpResponseNotFound("Not found")

    form = ProductForm(instance=producto)

    if request.user != producto.user:
        return HttpResponseNotFound("Not allowed to be here")

    form.fields['promocionar_a'].queryset = client.objects.filter(user = request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    return render(request, 'pacientes/create.html', {
        'form' : form
    })



def pricing(request):
    return render(request, "pricing.html", {
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })