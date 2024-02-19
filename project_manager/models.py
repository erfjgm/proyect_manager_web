from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=12)
    mail = models.EmailField(null=True)
    address = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=6)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=False, blank=False)

class Board(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
class List(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    
class Card(models.Model):
    name = models.CharField(max_length=255)
    lista = models.ForeignKey(List, on_delete=models.CASCADE)
