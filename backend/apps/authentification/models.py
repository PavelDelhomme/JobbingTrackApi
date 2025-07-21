import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models

class UserManager(BaseUserManager):
    """Manager custom - mail comme identifiant unique."""
    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(id=uuid.uuid4(), email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault('is_staff', False)
        extra.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra)
    
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra)
    
class User(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur principal."""
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email


class UserRole(models.TextChoices):
    CLIENT = 'CLIENT', 'Client'
    ADMIN  = 'ADMIN',  'Admin'


class UserPermissions(models.Model):
    """Table 1-1 stockant le rôle principal de l’utilisateur."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permissions')
    role = models.CharField(max_length=6, choices=UserRole.choices, default=UserRole.CLIENT)

    def __str__(self):
        return f'{self.user.email} – {self.get_role_display()}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'password_reset_tokens'
        
    def __str__(self):
        return self.token