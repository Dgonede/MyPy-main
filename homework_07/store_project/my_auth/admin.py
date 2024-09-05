from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StoreUser

class StoreUserAdmin(UserAdmin):
    pass

admin.site.register(StoreUser, StoreUserAdmin)