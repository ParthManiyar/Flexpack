from django.contrib import admin
from .models import User,Role,Box

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","first_name","last_name","email","role","provider")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('name','user')

