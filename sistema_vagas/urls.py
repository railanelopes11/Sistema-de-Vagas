from django.contrib import admin    
from django.urls   import include, path

# Lista principal de URLs do projeto
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("usuarios.urls")),
    path("usuarios/", include("usuarios.urls")),
    path("vagas/", include("vagas.urls")),
]
