from django.db import models
from restaurants.models import Plat
from clients.models import SignUpClient  


class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de livraison'),
        ('livree', 'Livrée'),
    ]

    client = models.ForeignKey(SignUpClient, on_delete=models.CASCADE, null=True, blank=True)
    adresse_livraison = models.CharField(max_length=255, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default="en_attente")

    
    def __str__(self):
        return f"Commande #{self.id} - {self.get_statut_display()}"

class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='items')
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.plat.nom} (Commande #{self.commande.id})"
