from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('lista-contratos/', views.listaContratos, name='listaContratos'),
    path('gestion-contratos/', views.gestionContratos, name='gestionContratos'),
    path('contratos/', views.contratos, name='contratos'),
    path('register/', views.register, name='register'),
    path('registerinterno/', views.registerinterno, name='register-interno'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('', views.seguimiento, name='seguimiento'),
    path('ingresar-productos/', views.ingresarproductos, name='ingresar-productos'),
    path('mis-productos/', views.misproductos, name='mis-productos'),
    path('venta/', views.venta, name='venta'),
    
    #path('subasta/<int:pk>/', views.subasta, name='subasta'),
    
    #path('pagarsubasta/<int:pk>/', views.pagarsubasta, name='pagarsubasta'),
    path('terminar/', views.terminar, name='terminar'),
    path('pagar/<int:total>/<int:pk>', views.pagar, name='pagar'),
    path('notificacion/', views.notificacion, name='notificacion'),
    path('notificar/<int:pk>/', views.notificar, name='notificar'),
    path('Solicitud/', views.Solicitud, name='Solicitud'),
    path('Solicitudes/', views.solicitudes, name='Solicitudes'),
    path('modificarsoli/<int:pk>/', views.modificarSolicitud, name="modificarSolicitud"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
