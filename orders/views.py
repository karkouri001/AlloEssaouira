from django.shortcuts import render, redirect, get_object_or_404
from restaurants.models import Plat
from .models import Commande, CommandeItem
from .forms import CommandeItemForm
from django.contrib.auth.decorators import login_required
from clients.models import SignUpClient  


def valider_commande(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)

    if request.method == 'POST':
        form = CommandeItemForm(request.POST)
        if form.is_valid():
            try:
                client = SignUpClient.objects.get(user=request.user)
            except SignUpClient.DoesNotExist:
                return redirect('connexion')

            commande = Commande.objects.create(
                adresse_livraison="Adresse par défaut",
                client=client
            )
            item = form.save(commit=False)
            item.plat = plat
            item.commande = commande
            item.save()
            return redirect('confirmation_commande')
    else:
        form = CommandeItemForm()

    return render(request, 'valider_commande.html', {
        'plat': plat,
        'form': form
    })


@login_required
def mes_commandes(request):
    try:
        client = SignUpClient.objects.get(user=request.user)
    except SignUpClient.DoesNotExist:
        return redirect('LoginClient')  
    
    commandes = Commande.objects.filter(client=client).order_by('-date_commande')
    return render(request, 'mes_commandes.html', {'commandes': commandes})

@login_required
def commande_detail(request, id):
    commande = get_object_or_404(Commande, id=id)

    try:
        client = SignUpClient.objects.get(user=request.user)
    except SignUpClient.DoesNotExist:
        return redirect('LoginClient')

    if commande.client != client:
        return redirect('mes_commandes')  

    return render(request, 'commande_detail.html', {'commande': commande})

def confirmation_commande(request):
    return render(request, 'confirmation_commande.html')


@login_required
def commande_recu(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    items = CommandeItem.objects.filter(commande=commande)

    return render(request, 'commande_recu.html', {
        'commande': commande,
        'items': items
    })
  