from django.contrib import admin

# Register your models here.
from .models import Livreur,Livraison

admin.site.register(Livreur)
admin.site.register(Livraison)