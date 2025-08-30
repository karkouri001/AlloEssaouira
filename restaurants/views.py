from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RestaurantSignupForm, LoginRestaurantForm, PlatForm
from django.shortcuts import get_object_or_404
from .models import Restaurant,Plat
from orders.models import Commande, CommandeItem
from clients.models import SignUpClient

def acceuil(request):
    return render(request,'acceuil.html')

def connexion(request):
    return render(request, 'connexion.html')

def login_restaurant(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                restaurant = Restaurant.objects.get(user=user)
                request.session['restaurant_id'] = restaurant.id
                request.session['restaurant_name'] = restaurant.nom
            except Restaurant.DoesNotExist:
                pass  

            return redirect('ajouter_plat')  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def ajouter_plat(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            plat = form.save(commit=False)
            plat.restaurant = request.user.restaurant  
            plat.save()
            return redirect('ajouter_plat')
    else:
        form = PlatForm()
    return render(request, 'ajouter_plat.html', {'form': form})

@login_required
def liste_restaurants(request):
    try:
        client = SignUpClient.objects.get(user=request.user)
    except SignUpClient.DoesNotExist:
        return redirect('LoginClient') 

    restaurants = Restaurant.objects.all()
    return render(request, 'liste_restaurants.html', {'restaurants': restaurants})


@login_required
def plats_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    plats = Plat.objects.filter(restaurant=restaurant)
    success = False

    if request.method == 'POST':
        adresse = request.POST.get('adresse')
        if adresse:
            client = SignUpClient.objects.get(user=request.user)
            commande = Commande.objects.create(
                adresse_livraison=adresse,
                client=client
            )
            for plat in plats:
                quantite = int(request.POST.get(f'quantite_{plat.id}', 0))
                if quantite > 0:
                    CommandeItem.objects.create(
                        commande=commande,
                        plat=plat,
                        quantite=quantite
                    )
            success = True

    return render(request, 'plats_restaurant.html', {
        'restaurant': restaurant,
        'plats': plats,
        'success': success
    })


@login_required
def modifier_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id, restaurant__user=request.user)

    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES, instance=plat)
        if form.is_valid():
            form.save()
            return redirect('liste_plats')  
    else:
        form = PlatForm(instance=plat)

    return render(request, 'modifier_plat.html', {'form': form})

@login_required
def supprimer_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id, restaurant__user=request.user)
    plat.delete()
    return redirect('liste_plats')

@login_required
def liste_plats(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('login_restaurant')

    plats = Plat.objects.filter(restaurant=restaurant)
    return render(request, 'liste_plats.html', {'plats': plats})



