from django.db import migrations, models
import django.contrib.auth.models
import uuid

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # dépendance minimale
    ]
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff',  models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField( to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField( to='auth.Permission', blank=True)),
            ],
            options={'db_table': 'authentification_user'},
            managers=[('objects', django.contrib.auth.models.UserManager)],
        ),
        migrations.CreateModel(
            name='UserPermissions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=6)),
                ('user', models.OneToOneField(on_delete=models.CASCADE, to='authentification.User')),
            ],
        ),
    ]
