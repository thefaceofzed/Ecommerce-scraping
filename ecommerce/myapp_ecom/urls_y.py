from django.urls import path


from .views import *

urlpatterns = [
    path('', shop_public, name='shop_public'),
    path('shop/', shop , name='shop'),

    path('add_user/', add_user , name='add_user'),
    path('indexAjo/', indexAjo , name='oo'),


    path('login/', user_login , name='ShowLoginPage'),
    path('scraping_jumia/', scraping_jumia, name='scraping_jumia'),

    path('panier/', panier, name='panier'),

    path('commande/', commande, name='commande'),

    path('update_article/', update_article, name='update_article'),

    path('traitement-commande/', traitementCommande, name="traitement_commande")


]
"""""path('', shop , name='shop'),"""""