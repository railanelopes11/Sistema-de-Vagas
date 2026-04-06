from django.db import models
from usuarios.models import Escolaridade
from django.conf import settings
    
class FaixaSalarial(models.TextChoices):
    ATE_1000 = "até 1000", "Até R$ 1000"
    DE_1000_A_2000 = "de 1000 a 2000", "De R$ 1000 a R$ 2000"
    DE_2000_A_3000 = "de 2000 a 3000", "De R$ 2000 a R$ 3000"
    ACIMA_DE_3000 = "acima de 3000", "Acima de R$ 3000"

class Vaga(models.Model):
    nome_vaga = models.CharField(max_length=255)
    requisitos = models.TextField()
    faixa_salarial = models.CharField(max_length=20, choices=FaixaSalarial.choices)
    escolaridade_minima = models.CharField(max_length=30, choices=Escolaridade.choices)
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="vagas", on_delete=models.CASCADE,null=True, blank=True, default=None)
     
    def __str__(self):
        return self.nome_vaga  
    
class Candidatura(models.Model):
    vaga= models.ForeignKey(Vaga, related_name="candidaturas", on_delete=models.CASCADE)
    candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    pretensao_salarial = models.CharField(max_length=20)
    experiencia = models.TextField()
    ultima_escolaridade = models.CharField(max_length=20, choices=Escolaridade.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vaga', 'candidato'], name='unique_vaga_candidato')
        ]


    def __str__(self):
        return f"Candidatura de {self.candidato} para {self.vaga}"


   

    


