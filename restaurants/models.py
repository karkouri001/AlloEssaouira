from django.db import models

from django.contrib.auth.models import User

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=150, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    photo_restaurant = models.ImageField(upload_to='restaurants_photos/', null=True, blank=True)
    horaires = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.nom or (self.user.username if self.user else "Restaurant")


class Plat(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(upload_to='plats_photos/', null=True, blank=True)  
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='plats')

    def __str__(self):
        return f"{self.nom or 'Plat'} - {self.restaurant.nom if self.restaurant else 'Sans restaurant'}"
