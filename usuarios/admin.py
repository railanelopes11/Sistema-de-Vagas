from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('tipo_usuario', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_staff', 'is_active')}),
        ('Tipo de Usuário', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'tipo_usuario')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)   

admin.site.register(Usuario, UsuarioAdmin)  