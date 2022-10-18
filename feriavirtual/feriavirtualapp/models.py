from email.policy import default
from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import fields
from django.db.models.fields import related
from django.utils import timezone
PRODUCTOS =(
    ("1", "Cerezas "),
    ("2", "Uvas"),
    ("3", "Arándanos "),
    ("4", "Nueces"),
    ("5", "Manzana"),
    ("6", "Ciruela"),
    ("7", "Peras"),
    ("9", "Durazno"),
    ("11", "Frutilla"),
    ("12", "Granada"),
    ("13", "Limón"),
    ("14", "Mandarina"),
    ("15", "Naranja"),
    ("16", "Sandia "),
    ("17", "Melón"),
    ("18", "Mora"),
    ("19", "Pera"),
    ("20", "Manzana"),
    )

#ATENDIENDO TAMAÑO Y CALIBRE LA FRUTA SE PUEDE CALIFICAR EN:
CALIBRE =(
    ("1", "Segunda"),
    ("2", "Primera"),
    ("3", "Extra "),
)
TAMAÑO =(
    ("1", "Ligero "),
    ("2", "Liviano"),
    ("3", "Semi Liviano"),
    ("4", "Mediano"),
    ("5", "Semi esado"),
    ("6", "Pesado"),
    ("7", "Extra Pesado"),
    ("8", "Mega Pesado"),
    ("9", "Ultra Pesado"),
    ("10", "Extra Pesado"),
    ("11", "Giga Pesado"),
    ("12", "Super Pesado"),
    )
EstadoSolicitudCompra =(
    ("1", "Aprobado"),
    ("2", "Rechazado"),
    ("3", "Pendiente"),
    ("4", "Subasta Transporte"),
    ("5", "Esperando productos en bodega central"),
    ("6", "Revision de calidad"),
    ("7", "En camino"),
    ("8", "Destino"),
    )
class User(AbstractUser):
    ROLES =(
    ("1", "Productor"),
    ("2", "Cliente externo"),
    ("3", "Cliente interno"),
    ("4", "Transportista"),
    ("5", "Consultor"),
    ("6", "Administrador"),
    ("7", "Revisor de calidad"),
    )
    rol = models.CharField(max_length=50, choices = ROLES, null=True)
    imagen = models.ImageField(upload_to="Perfil",default='default.png')
    def __str__(self):
        return f'{self.username}'

class Post(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    calibre = models.CharField(max_length=50, choices = CALIBRE, null=True,default=1)
    cantidad_actual = models.IntegerField(default=0)
    cantidad_necesaria = models.IntegerField(default=0)
    contenido = models.TextField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ClienteSoli')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Posts", null=True)
    EstadoSolicitud = models.CharField(max_length=50, null=True, choices=EstadoSolicitudCompra, default='3')

    class Meta:
        ordering = ['-fecha_creacion']
    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()

class PostTransporte(models.Model):
    transportista = models.ForeignKey(User, on_delete=models.CASCADE,related_name='postTransporte')
    productor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ProductorT')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ClienteT')
    tamaño = models.CharField(max_length=50, choices = TAMAÑO, null=True)
    refrigeracion = models.BooleanField(default=False)
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    cantidad_actual = models.IntegerField(default=0)
    
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="Posts", null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-fecha_creacion']
    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()


    def __str__(self):
        return f'{self.transportista.username}: {self.productor.username}'
class Producto(models.Model):
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='producto')
    producto = models.CharField(max_length=50, choices = PRODUCTOS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    calibre = models.CharField(max_length=50,choices = CALIBRE, null=True)
    cantidad = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Productos", null=True)
    precio = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.autor.username}: {self.producto}: { self.variedad} :  { self.calibre}'

class ProcesoVenta(models.Model):
    from_post = models.ForeignKey(Post, related_name='Puja', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='Participante_de', on_delete=models.CASCADE)
    productos = models.ForeignKey(Producto, related_name='Productos', on_delete=models.CASCADE)
    cantidad_ingresada = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.from_post} to {self.to_user}'
    class Meta:
        indexes = [
            models.Index(fields=['from_post', 'to_user',]),
        ]
class Notificacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = fields.IntegerField(default=0)
    post = models.ForeignKey(Post, related_name='Post', on_delete=models.CASCADE)

class Contrato(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_termino = models.DateField(default=timezone.now)
    vigencia = models.BooleanField(default=False)
    
