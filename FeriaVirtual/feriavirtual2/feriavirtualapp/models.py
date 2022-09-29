from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import fields
from django.db.models.fields import related
from django.utils import timezone
FRUTAS =(
    ("1", "Aguacate "),
    ("2", "Damasco"),
    ("3", "Piña"),
    ("4", "Arándano"),
    ("5", "Plátano"),
    ("6", "Cereza"),
    ("7", "Ciruela"),
    ("8", "Coco"),
    ("9", "Durazno"),
    ("10", "Frambuesa"),
    ("11", "Frutilla "),
    ("12", "Granada"),
    ("13", "Limón"),
    ("14", "Mandarina"),
    ("15", "Melón"),
    ("16", "Sandia "),
    ("17", "Membrillo"),
    ("18", "Mora"),
    ("19", "Pera"),
    ("20", "Manzana"),
    
    ("21", "Naranja"),
    )
class User(AbstractUser):
    ROLES =(
    ("1", "Productor"),
    ("2", "Cliente externo"),
    ("3", "Cliente interno"),
    ("4", "Transportista"),
    ("5", "Consultor"),
    ("6", "Administrador"),
    ("6", "Revisor de calidad"),
    )
    rol = models.CharField(max_length=50, choices = ROLES, null=True)
    imagen = models.ImageField(upload_to="Perfil",default='default.png')
    def __str__(self):
        return f'{self.username}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    fruta = models.CharField(max_length=50, choices = FRUTAS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    cantidad_actual = models.IntegerField(default=0)
    cantidad_necesaria = models.IntegerField(default=0)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Cliente')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Posts", null=True)

    class Meta:
        ordering = ['-fecha_creacion']
    def publish(self):
        self.fecha_publicacion = timezone.now()
        self.save()
    def participantes(self):
        user_ids = Relacion.objects.filter(from_post=self)\
                            .values_list('to_user_id', flat= True)
        
        return User.objects.filter(id__in=user_ids)
    def productos(self):
        user_ids = Relacion.objects.filter(from_post=self)\
                            .values_list('to_user_id', flat= True)
        return Producto.objects.filter(autor__in=user_ids)

    def __str__(self):
        return f'{self.user.username}: {self.contenido}'

class Producto(models.Model):
    
    autor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='producto')
    fruta = models.CharField(max_length=50, choices = FRUTAS, null=True)
    variedad = models.CharField(max_length=50, null=True)
    cantidad = models.IntegerField(default=0)
    fecha_subida = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to="Productos", null=True)
    precio = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.autor.username}: {self.fruta}'

class Relacion(models.Model):
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