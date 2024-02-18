from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Board, List, Card, UserProfile, Company

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UsuarioExtendido(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UsuarioExtendido)

# Registra los modelos en el panel de administración
admin.site.register(Company)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)
