from django.db import models
from orders.models import Commande
from django.contrib.auth.models import User


class Livreur(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_livraison', 'En Livraison'),
        ('indisponible', 'Indisponible'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    nom = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cin = models.CharField(max_length=20, unique=True, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')

    def __str__(self):
        if self.user:
            return f"{self.prenom or ''} {self.nom or self.user.username}"
        return "Livreur sans compte"


class Livraison(models.Model):
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE)
    livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE)
    date_livraison = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=[
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
    ], default='en_cours')

    def __str__(self):
        return f"Livraison {self.commande.id} par {self.livreur.nom if self.livreur else 'Livreur inconnu'}"
