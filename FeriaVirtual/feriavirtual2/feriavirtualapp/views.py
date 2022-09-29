from django.db.models.aggregates import Count
from django.db.models.expressions import Exists
from django.shortcuts import render
from django.utils import timezone
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
# Create your views here.
def post_list(request):
    return render(request, 'post_list.html', {})
def register(request):
    if request.method == 'POST':
        form = FormRegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')
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
def publicaciones(request):
    posts = Post.objects.all()
    
    context ={'posts':posts}
    return render(request, 'publicaciones.html',context)

def ingresarproductos(request):
    if request.method == 'POST':
        form = FormProductos(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            try:
                Producto.objects.get(autor=request.user, fruta=prod.fruta)
                existe = Producto.objects.get(autor=request.user, fruta=prod.fruta)
                var = form.cleaned_data['cantidad']
                existe.autor = request.user
                existe.fecha_subida = timezone.now()
                existe.imagen = request.FILES['imagen']
                existe.cantidad = existe.cantidad+var
                existe.save()
                messages.success(request, f'Frutas agregadas a tus {existe.fruta}.')
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

def subasta(request,pk):
    post = get_object_or_404(Post, pk=pk)

    try:
        prod = Producto.objects.get(autor=request.user, fruta=post.fruta)

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
                            messages.error(request, f'Esa cantidad de fruta supera la cantidad necesaria.')
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
        messages.error(request, f'No tienes ese tipo de fruta en tus productos.')
        return redirect('/')
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
def notificar(request):
    messages.success(request, f'Cliente notificado con exito!.')
    return render(request, 'notificado.html',) 
