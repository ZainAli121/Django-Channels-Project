from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
import uuid
from django.utils import timezone

# Create your models here.
class CutomUserManager(UserManager):
    def _create_user(self, name ,email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be valid')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, name=None ,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, name ,password, **extra_fields)
    
    def create_superuser(self, name=None ,email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, name ,password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    AGENT = 'agent'
    MANAGER = 'manager'

    ROLE_CHOICES = (
        (AGENT, 'Agent'),
        (MANAGER, 'Manager'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)
    password = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=AGENT)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=True, null=True)

    objects = CutomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.username
