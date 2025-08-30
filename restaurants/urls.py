from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_restaurants, name='liste_restaurants'),
    path('connexion/',views.connexion, name='connexion'),
    path('login/', views.login_restaurant, name='login_restaurant'),
    path('ajouter_plat/', views.ajouter_plat, name='ajouter_plat'),
    path('plats/<int:restaurant_id>/', views.plats_restaurant, name='plats_restaurant'),
    path('liste_plats/', views.liste_plats, name='liste_plats'),
    path('modifier_plat/<int:plat_id>/', views.modifier_plat, name='modifier_plat'),
    path('supprimer_plat/<int:plat_id>/', views.supprimer_plat, name='supprimer_plat'),

    
]
