from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("lista/", views.listar_vagas, name="listar_vagas"),
    path("criar/", views.criar_vaga, name="criar_vaga"),
    path("minhas/", views.minhas_vagas, name="minhas_vagas"),
    path("editar/<int:vaga_id>/", views.editar_vaga, name="editar_vaga"),
    path("deletar/<int:vaga_id>/", views.deletar_vaga, name="deletar_vaga"),
    path("candidatar/<int:vaga_id>/", views.candidatar, name="candidatar"), 
    path ("detalhe_vaga/<int:vaga_id>/", views.detalhes_vaga, name="detalhes_vaga"),
    path("relatorio/", views.relatorio, name="relatorio"),
]

