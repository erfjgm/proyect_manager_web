from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.exit, name='exit'), 
    path('list_boards/', views.list_boards, name='list_boards'),
    path('add_board/', views.add_board, name='add_board'),
    path('edit_board/', views.edit_board, name='edit_board'),
    path('delete_board/', views.delete_board, name='delete_board'),
    path('list_lists/', views.list_lists, name='list_lists'),
    path('add_list/', views.add_list, name='add_list'),
    path('edit_list/', views.edit_list, name='edit_list'),
    path('delete_list/', views.delete_list, name='delete_list'),
    path('list_cards/', views.list_cards, name='list_cards'),
    path('list_detail_card/', views.list_detail_card, name='list_detail_card'),
    path('add_card/', views.add_card, name='add_card'),
    path('edit_card/', views.edit_card, name='edit_card'),
    path('delete_card/', views.delete_card, name='delete_card'),
    path('list_users/', views.list_users, name='list_users'),
]