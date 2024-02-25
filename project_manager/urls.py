from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.exit, name='exit'), 
    path('list_boards/', views.list_boards, name='list_boards'),
    path('list_lists/', views.list_lists, name='list_lists'),
    path('list_cards/', views.list_cards, name='list_cards'),
]