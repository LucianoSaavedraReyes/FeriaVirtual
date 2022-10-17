from ast import Try
from datetime import datetime
from django.db.models.aggregates import Count
from django.db.models.expressions import Exists
from django.shortcuts import render
from django.utils import timezone
from requests import post
from .models import *
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.error.transbank_error import TransbankError
from django.contrib.auth import login
from operator import attrgetter



# Create your views here.
def listaContratos(request):
    cont = Contrato.objects.all()
    context ={'cont':cont}
    return render(request, 'lista-contratos.html', context)
def gestionContratos(request):
    return render(request, 'gestion-contratos.html', {})
def contratos(request):
    if request.method == 'POST':
        form = FormContratos(request.POST)
        if form.is_valid():
            cont = form.save(commit=False)
            cont.username = form.cleaned_data['usuario']
            existeuser = get_object_or_404(User, username=cont.username)
           
            
            try:
                existecont = Contrato.objects.get(usuario=existeuser)
                messages.error(request, f'Este productor ya tiene un contrato vigente.')
            except Contrato.DoesNotExist:    
                cont.fecha_inicio = form.cleaned_data['fecha_inicio']
                cont.fecha_termino = form.cleaned_data['fecha_termino']
                if cont.fecha_inicio > cont.fecha_termino:
                    messages.error(request, f'La fecha de inicio no puede ser mayor a la de termino del contrato')
                else:
                    cont.vigencia = True
                    form.save()
                    messages.success(request, f'Contrato para productor {cont.username} creado')
                    return redirect('contratos')
    else:
        form = FormContratos()
    context = { 'form': form }
    return render(request, 'contratos.html', context)

def register(request):
    if request.method == 'POST':
        form = FormRegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('/register')
    else:
        form = FormRegistroUsuario()
    context = { 'form': form }
    return render(request, 'register.html',context)
def registerinterno(request):
    if request.method == 'POST':
        form = FormRegistroInterno(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
    else:
        form = FormRegistroInterno()
    context = { 'form': form }
    return render(request, 'register-interno.html',context)    

def seguimiento(request):
    return render(request, 'seguimiento.html',{})

def ingresarproductos(request):
    if request.method == 'POST':
        form = FormProductos(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            try:
                Producto.objects.get(autor=request.user, producto=prod.producto)
                existe = Producto.objects.get(autor=request.user, producto=prod.producto)
                var = form.cleaned_data['cantidad']
                existe.autor = request.user
                existe.fecha_subida = timezone.now()
                existe.imagen = request.FILES['imagen']
                existe.cantidad = existe.cantidad+var
                existe.save()
                messages.success(request, f'Productos agregados a tus {existe.producto}.')
                pass
                return redirect('/')
                
            except Producto.DoesNotExist:
                prod.autor = request.user
                prod.fecha_subida = timezone.now()
                prod.imagen = request.FILES['imagen']
                prod.save()
                messages.success(request, f'Producto agregado.')
                return redirect('/')
    else:
        form = FormProductos()
    context = { 'form': form }
    return render(request, 'ingresar-productos.html',context)

def misproductos(request):
    prod = Producto.objects.filter(autor=request.user)
    context ={'prod':prod}
    return render(request, 'misproductos.html',context)
def venta(request):
    if request.method == 'POST':
        form = FormVenta(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.cliente = form.cleaned_data['cliente']
            post.user = request.user
            post.fecha_creacion = timezone.now()
            post.imagen = request.FILES['imagen']
            post.save()
            messages.success(request, f'Venta iniciada!')
            return redirect('/')
    else:
        form = FormVenta()
    context = { 'form': form }
    return render(request, 'iniciar-venta.html',context)
'''
def subasta(request,pk):
    post = get_object_or_404(Post, pk=pk)

    try:
        prod = Producto.objects.get(autor=request.user, producto=post.producto)

        if request.method == "POST":
            form = FormPujarSubasta(request.POST)
            if form.is_valid():
                if prod.cantidad > 0 :
                    var = form.cleaned_data['cantidad']
                    
                    post.cantidad_actual = post.cantidad_actual+var
                    
                    prod.cantidad = prod.cantidad-var
                    if var > prod.cantidad:
                        messages.error(request, f'No tienes la cantidad suficiente para participar en la subasta .')
                    else:
                        if post.cantidad_actual > post.cantidad_necesaria:
                            messages.error(request, f'Esa cantidad de productos supera la cantidad necesaria.')
                            return redirect('/')
                        else:
                            current_user = request.user
                            to_user = current_user
                            to_user_id = to_user
                            try:
                                rel = Relacion.objects.get(from_post=post, to_user=to_user_id)
                                cantactual =rel.cantidad_ingresada
                                total = cantactual+var
                                rel.cantidad_ingresada = total
                                rel.save()
                                prod.save()
                                post.save()
                                messages.success(request, f'Productos agregados a la subasta!')
                                return redirect('/')
                                
                            except:
                                rel = Relacion(from_post=post, to_user=to_user_id, productos=prod, cantidad_ingresada=var)
                                rel.save()
                                messages.success(request, f'Ahora estás participando en la subasta')
                                prod.save()
                                post.save()
                                messages.success(request, f'Productos agregados a la subasta!')
                                return redirect('/')
                    return redirect('/')
                else:
                    messages.error(request, f'No tienes la cantidad suficiente para participar en la subasta.')
                    return redirect('/') 
        else:
            form = FormPujarSubasta()
            resta = post.cantidad_necesaria - post.cantidad_actual 
            context ={'post':post , 'form':form, 'resta':resta,}
            return render(request, 'subasta.html', context)    
    except Producto.DoesNotExist:
        messages.error(request, f'No tienes ese tipo de producto en tus productos.')
        return redirect('/')
'''
def pagar(request,total,pk):
    total = total   
    buy_order = str(pk)
    session_id = request.user.username
    return_url = 'http://127.0.0.1:8000/terminar/'
    noti=Notificacion.objects.get(pk=pk)
    amount = total
    try:
        response = Transaction().create(buy_order, session_id, amount, return_url)
        context ={'total':total,"response":response,'noti':noti}
        print(amount)
        return render(request, 'pagar.html', context) 
    except TransbankError as e:
        print(e.message)
        print(e.message)
        error =e.message
        context ={'total':total,"error":error,}
        return render(request, 'pagar.html', context) 
'''
def pagarsubasta(request,pk):
    post = Post.objects.get(pk=pk)
    parts = post.participantes()
    prods = post.productos()
    rel = Relacion.objects.filter(from_post=post).values_list('cantidad_ingresada', flat= True)
    rela = Relacion.objects.filter(from_post=post)
    precio = 0
    for re in rela :
        precio = precio + re.productos.precio
        
    total = precio*post.cantidad_actual
    try:
        noti = Notificacion.objects.get(usuario=post.cliente)
        noti.total = total
        noti.post = post
        noti.save()
    except:
        noti = Notificacion(usuario=post.cliente,total=total, post=post)
        noti.save()
    
    context ={'post':post, 'parts':parts, 'prods':prods, 'rel':rel, 'total': total,}
    
    return render(request, 'pagar-subasta.html', context) 
'''
def notificacion(request):
    try:
        notis=Notificacion.objects.filter(usuario=request.user)
        messages.success(request, f'Tienes notificaciones de pago pendientes.')
        context={'notis':notis}
    except:
        messages.error(request, f'No tienes notificaciones actualmente.')
    context={'notis':notis}
    return render(request, 'notificacion.html',context) 

def terminar(request):
    token = request.POST.get("token_ws")
    try:
        response = Transaction().commit(token) 
        user = User.objects.get(username=response.session_id)
        login(request, user)
        noti = Notificacion.objects.get(pk=response.buy_order)
        post = noti.post
        post.delete()
        noti.delete()
        messages.success(request, f'Pago exitoso.')
        return render(request, 'terminar.html',{"token": token,"response": response})
    except TransbankError as e:
        messages.error(request, f'Error en la transaccion de pago.')
        error =e.message
        print(e.message)
        print(token)
        return render(request, 'terminar.html', {"error":error})   
def notificar(request,pk):
    post = Post.objects.get(pk=pk)
    postT = PostTransporte.objects.create()
    #postT.transportista =
    
    messages.success(request, f'El cliente ha sido notificado y se ha iniciado una subasta de transporte')
    return render(request, 'notificado.html',) 


def Solicitud(request):

    if request.method == 'POST':
        form = FormVenta(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.usuario = request.user
            post.fecha_creacion = timezone.now()
            post.imagen = request.FILES['imagen']
            post.save()
            messages.success(request, f'Venta iniciada!')
            return redirect('/')
    else:
        form = FormVenta()
    context = { 'form': form }
    return render(request, 'Solicitud.html',context)
def solicitudes(request):
    soli = Post.objects.all()
    context ={'soli':soli,}
    return render(request, 'Solicitudes.html', context)
def modificarSolicitud (request, pk):
    SolicitudPK = Post.objects.get(pk = pk)
    if request.method == 'POST':
        form = FormSolicitudEstado(request.POST, instance = SolicitudPK)
        if form.is_valid():
            SolicitudPK = form.save(commit=False)
            SolicitudPK = Post.objects.get(pk = pk)
            topProductores = User.objects.filter(rol='1')
            cantidadnecesaria= SolicitudPK.cantidad_necesaria
            productonecesario = SolicitudPK.producto
            calibrenecesario = SolicitudPK.calibre
            try:
                for productor in topProductores:
                    topProductos = []
                    try:
                        producto1 = Producto.objects.get(autor=productor , producto=productonecesario, calibre=calibrenecesario)
                        if producto1.cantidad >= cantidadnecesaria:
                            topProductos.append(producto1)
                        else:
                            print('Ningun productor tiene los productos suficientes para participar')
                    except Producto.DoesNotExist:
                        print("Producto no existe")
                try:
                    min_precio = min(topProductos, key=attrgetter('precio'))
                    min_precio = min_precio.precio
                except:
                    print("no hay nada ahi")
                try:
                    for ganador in topProductos:
                        if ganador.precio == min_precio:
                            productoganador = ganador     
                            productorganador = User.objects.get(username=productoganador.autor.username)
                            #posiblidad de bloque pl sql, cuando el producto llege a 0,borrar la fila completa del producto
                            
                            productoganador.cantidad = productoganador.cantidad - cantidadnecesaria
                            productoganador.save()
                            print(cantidadnecesaria)
                            #cantidad actual ya no seria necesaria
                            SolicitudPK.cantidad_actual = cantidadnecesaria
                            SolicitudPK.EstadoSolicitud = form.cleaned_data['EstadoSolicitud']
                except Producto.MultipleObjectsReturned:   
                    prodganadores: topProductos.objects.filter(precio=min_precio)
                    cantidadP = prodganadores.count
                    
            except Producto.DoesNotExist :   
                SolicitudPK.EstadoSolicitud = '3'
                messages.error(request, f'En este momento no hay productores que puedan satisfacer el pedido')
                
            SolicitudPK.save()
            return redirect('/Solicitudes')
    else:
        form = FormSolicitudEstado(instance=SolicitudPK)   
        context ={'form':form,}
        return render(request, 'modificarsoli.html', context)
