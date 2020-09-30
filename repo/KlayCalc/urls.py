from django.urls import path

from . import views

urlpatterns = [
    path('', views.root, name='root'),

    path('index/', views.index, name='index'),

    path('account/', views.account, name='account_noData'),
    path('account/<str:account_id>', views.account, name='account'),
    
    path('donate/', views.donate, name='donate'),

    # Ajax
    path('checkDonateAddr/', views.checkDonateAddr, name='checkDonateAddr')
]
