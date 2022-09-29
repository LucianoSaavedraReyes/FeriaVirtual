
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, User, Post
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

class FormRegistroUsuario(UserCreationForm):
    ROLES =(
    ("1", "Productor"),
    ("2", "Cliente externo"),
    ("3", "Transportista"),
    ("4", "Consultor"), 
    ("5", "Administrador"),
    ("6", "Revisor de calidad"),
    )
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña',widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices = ROLES)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','rol']
        help_texts = {k:"" for k in fields}
class FormRegistroInterno(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        help_texts = {k:"" for k in fields}
class FormVenta(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('fruta','variedad','cantidad_necesaria','cliente','contenido', 'imagen',)


class FormPujarSubasta(forms.Form):
    cantidad = forms.IntegerField(help_text="Ingrese la cantidad que desea aportar para satisfacer el pedido.")

class FormProductos(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('fruta','variedad','cantidad','precio', 'imagen',)