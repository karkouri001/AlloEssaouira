from django.urls import path
from . import views

urlpatterns = [
    path('mes_commandes/', views.mes_commandes, name='mes_commandes'),
    path('commande/<int:id>/', views.commande_detail, name='commande_detail'),
    path('valider_commande/<int:plat_id>/', views.valider_commande, name='valider_commande'),
    path('confirmation_commande/',views.confirmation_commande, name='confirmation_commande'),
    path('recu/<int:commande_id>/', views.commande_recu, name='commande_recu'),

]