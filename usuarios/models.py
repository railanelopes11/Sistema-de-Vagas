from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class TipoUsuario(models.TextChoices):
    EMPRESA = "empresa", "Empresa"
    CANDIDATO = "candidato", "Candidato"

class Escolaridade(models.TextChoices):
    ENSINO_FUNDAMENTAL = "ensino_fundamental", "Ensino Fundamental"
    ENSINO_MEDIO = "ensino_medio", "Ensino Médio"
    TECNÓLOGO = "tecnologo", "Tecnólogo"
    ENSINO_SUPERIOR = "ensino_superior", "Ensino Superior"
    POS_MBA_MESTRADO = "pos_mba_mestrado", "Pós/MBA/Mestrado"
    DOUTORADO = "doutorado", "Doutorado"

# Responsável por criar usuários e superusuários corretamente
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser fornecido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Modelo de usuário personalizado
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    tipo_usuario = models.CharField(max_length=20, choices=TipoUsuario.choices)    


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def __str__(self):
        return self.email
    
    def is_empresa(self):
        return self.tipo_usuario == TipoUsuario.EMPRESA

    def is_candidato(self):
        return self.tipo_usuario == TipoUsuario.CANDIDATO
    
