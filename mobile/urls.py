from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login_mobile"),
    path('bienvenida/', views.bienvenida, name="bienvenida"),
    path('logout/', views.logout, name="logout_mobile"),
    path('perfil/<int:id>', views.ver_perfil, name="perfil_mascota"),
    path('product_detail/<int:id>', views.product_detail, name="product_detail"),
    path('descargar/', views.descargar, name="descargar"),
    path('citas_cliente/', views.citas_cliente, name="citas_cliente"),
    path('clinicas/', views.clinicas, name="clinicas"),
    path('clinicas/perfil/<int:id>', views.perfil_veterinaria, name="perfil_veterinaria"),
    path('clinicas/perfil/coment/<int:id>', views.coment_perfil, name="coment_perfil"),
    path('veterinarias/', views.veterinarias, name="veterinarias"),

]



