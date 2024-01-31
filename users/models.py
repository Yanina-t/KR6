from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class User(AbstractUser):
    username = None
    full_name = models.CharField(max_length=35, **NULLABLE, verbose_name='full_name')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон')
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')
    is_moderator = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
