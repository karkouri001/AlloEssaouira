from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_livreur, name='login_livreur'),
    path('after-login/', views.after_login_livreur, name='after_login_livreur'),
    path('logout/', views.logout_livreur, name='logout_livreur'),
    path('terminer/<int:livraison_id>/', views.terminer_livraison, name='terminer_livraison'),
    path('commandes-disponibles/', views.commandes_disponibles, name='commandes_disponibles'),
    path('accepter-commande/<int:commande_id>/', views.accepter_commande, name='accepter_commande'),
]
