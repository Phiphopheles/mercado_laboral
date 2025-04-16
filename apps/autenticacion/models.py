from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ADMIN = 'admin'
    GESTOR = 'gestor'
    COLABORADOR = 'colaborador'

    ROLES = [
        (ADMIN, 'Administrador'),
        (GESTOR, 'Gestor de Proyectos'),
        (COLABORADOR, 'Colaborador'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default=COLABORADOR)

    # Override groups and user_permissions with custom related_names
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario'
    )
