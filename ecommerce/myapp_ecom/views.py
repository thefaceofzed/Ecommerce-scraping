import datetime
import json
import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from datetime import datetime
from .utile import commandeAnonyme, data_cookie, panier_cookie
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Client

import requests
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
import pandas as pd

def scraping_jumia(request):
    url = 'https://www.jumia.ma/smartphones/?page='

    columns = {'name': [], 'price': [], 'img_url': []}

    for page in range(1, 10):
        print('---', page, '---')
        r = requests.get(url + str(page))
        soup = BeautifulSoup(r.content, "html.parser")

        ancher = soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'}).find_all('article',
                                                                                      {'class': 'prd _fb col c-prd'})
        for pt in ancher:
            img = pt.find('a').find('div', {'class': 'img-c'}).find('img', {'class': 'img'})
            name = pt.find('a').find('div', {'class': 'info'}).find('h3', {'class': 'name'})
            price = pt.find('a').find('div', {'class': 'info'}).find('div', {'class': 'prc'})

            columns['name'].append(name.text)
            columns['price'].append(price.text)
            columns['img_url'].append(img.get('data-src'))

    data = pd.DataFrame(columns)
    data.to_json('data.json', orient='records', indent=4)

    with open('data.json', 'r') as f:
        dataj = json.load(f)

    for item in dataj:
        image = item['img_url']
        price = float(''.join(filter(str.isdigit, item['price'])))
        name = item['name']
        produit = Produit(name=name, price=price, image=image)
        produit.save()

    return render(request, 'shop/amazon_scraping.html')

@login_required(login_url='/login/')
def shop(request, *args, **kwargs):
    """ vue principale """

    produits = Produit.objects.all()
    data = data_cookie(request)
    nombre_article = data['nombre_article']

    context = {
        'produits': produits,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/index.html', context)

def shop_public(request, *args, **kwargs):
    """ vue principale """

    produits = Produit.objects.all()
    data = data_cookie(request)
    nombre_article = data['nombre_article']

    context = {
        'produits': produits,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/ma_page_publique.html', context)


def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(user=user)
            return redirect('shop')
    else:
        form = UserCreationForm()
    return render(request, 'add_user.html', {'form': form})


def ma_vue_protegee(request):
    # Code pour afficher la page réservée aux utilisateurs connectés
    return render(request, 'index.html')

def ma_vue_publique(request):
    # Code pour afficher la page publique
    return render(request, 'ma_page_publique.html')

def base(request):
    return render(request,"base.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    else:
        return render(request,'login.html')

def ShowLoginPage(request):
    return render(request,"login.html")



def indexAjo(request):
    return render(request,"indexAjo.html")



def panier(request, *args, **kwargs):
    """ panier """

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    """ Commande """

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles': articles,
        'commande': commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/commande.html', context)


def update_article(request, *args, **kwargs):
    data = json.loads(request.body)

    produit_id = data['produit_id']

    action = data['action']

    client = request.user.client

    produit = Produit.objects.get(id=produit_id)

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action == 'add':
        commande_article.quantite += 1

    if action == 'remove':
        commande_article.quantite -= 1

    commande_article.save()

    if commande_article.quantite <= 0:
        commande_article.delete()

    return JsonResponse("Article ajouté", safe=False)


def traitementCommande(request, *args, **kwargs):
    """ traitement,  validation de la com;ande  et verification de l'integrite des donnees(detection de fraude)"""

    STATUS_TRANSACTION = ['ACCEPTED', 'COMPLETED', 'SUCESS']

    transaction_id = datetime.now().timestamp()

    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)


    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = data['payment_info']['transaction_id']

    commande.total_trans = total

    if commande.get_panier_total == total:

        commande.complete = True
        commande.status = data['payment_info']['status']

    else:
        commande.status = "REFUSED"
        commande.save()

        return JsonResponse("Attention!!! Traitement Refuse Fraude detecte!", safe=False)

    commande.save()

    if not commande.status in STATUS_TRANSACTION:
        return JsonResponse("Désolé, le paiement a échoué, veuillez réessayer")

    if commande.produit_physique:
        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse=data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )

    return JsonResponse("Votre paiement a été effectué avec succès, vous recevrez votre commande dans un instant !",
                        safe=False)

