from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login_view"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_page, name="register"),
    path('app/', views.index, name="app"),
    path('app/clients/create/', views.create_user, name="create_user"),
    path('app/clients/', views.clientes, name="clientes"),
    path('app/clients/edit/<str:pk>/', views.editar_cliente, name="editar_cliente"),
    path('app/patients/', views.pacientes, name="pacientes"),
    path('app/appointments/', views.citas, name="citas"),
    path('app/appointments/create/', views.crear_citas, name="crear_citas"),
    path('app/appointments/edit/<str:pk>/', views.editar_cita, name="editar_cita"),
    path('app/clients/<int:pk>/', views.client_profile, name="client_profile"),
    path('app/patient/create/', views.crear_paciente, name="crear_paciente"),
    path('app/patient/edit/<str:pk>/', views.editar_paciente, name="editar_paciente"),
    path('register/<str:hash>/', views.confirmacion_correo, name="confirmacion_correo"),
    path('stepform/', views.step_form, name="step_form"),
    # Stripe urls
    path('app/pricing/checkout-session/<pk>/', views.checkout_view, name="create-checkout-session"),
    path('app/pricing/webhooks/stripe/', views.webhook_view, name="stripe-webhook"),

    # Product urls
    path('app/products/create/', views.crear_producto, name="crear_producto"),
    path('app/products/', views.productos, name="productos"),
    path('app/products/edit/<str:pk>/', views.editar_producto, name="editar_producto"),
    path('app/pricing/', views.pricing, name="pricing"),

    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)









