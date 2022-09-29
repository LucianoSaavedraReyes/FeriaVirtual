# Generated by Django 3.1.2 on 2021-07-03 22:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.CharField(choices=[('1', 'Productor'), ('2', 'Cliente externo'), ('3', 'Cliente interno'), ('4', 'Transportista'), ('5', 'Consultor'), ('6', 'Administrador')], max_length=50, null=True)),
                ('imagen', models.ImageField(default='default.png', upload_to='Perfil')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fruta', models.CharField(choices=[('1', 'Aguacate '), ('2', 'Damasco'), ('3', 'Piña'), ('4', 'Arándano'), ('5', 'Plátano'), ('6', 'Cereza'), ('7', 'Ciruela'), ('8', 'Coco'), ('9', 'Durazno'), ('10', 'Frambuesa'), ('11', 'Frutilla '), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Melón'), ('16', 'Sandia '), ('17', 'Membrillo'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana'), ('21', 'Naranja')], max_length=50, null=True)),
                ('variedad', models.CharField(max_length=50, null=True)),
                ('cantidad_actual', models.IntegerField(default=0)),
                ('cantidad_necesaria', models.IntegerField(default=0)),
                ('contenido', models.TextField()),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('imagen', models.ImageField(null=True, upload_to='Posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fruta', models.CharField(choices=[('1', 'Aguacate '), ('2', 'Damasco'), ('3', 'Piña'), ('4', 'Arándano'), ('5', 'Plátano'), ('6', 'Cereza'), ('7', 'Ciruela'), ('8', 'Coco'), ('9', 'Durazno'), ('10', 'Frambuesa'), ('11', 'Frutilla '), ('12', 'Granada'), ('13', 'Limón'), ('14', 'Mandarina'), ('15', 'Melón'), ('16', 'Sandia '), ('17', 'Membrillo'), ('18', 'Mora'), ('19', 'Pera'), ('20', 'Manzana'), ('21', 'Naranja')], max_length=50, null=True)),
                ('variedad', models.CharField(max_length=50, null=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha_subida', models.DateTimeField(default=django.utils.timezone.now)),
                ('imagen', models.ImageField(null=True, upload_to='Productos')),
                ('precio', models.IntegerField(default=0)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Puja', to='feriavirtualapp.post')),
                ('productos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Productos', to='feriavirtualapp.producto')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Participante_de', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='relacion',
            index=models.Index(fields=['from_post', 'to_user'], name='feriavirtua_from_po_353ef8_idx'),
        ),
    ]