from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    nif = models.CharField(max_length=12)
    mail = models.EmailField(null=True)
    address = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=6)

class UserProfile(models.Model):
    ROL_USER = [
        ('USER','Usuario'),
        ('ADMIN_COMPANY','Administrador Compañia'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,null=False, blank=False)
    rol = models.CharField(max_length=20, choices=ROL_USER, default='USER')

class Board(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    deletion_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ['name', 'company']
    def __str__(self):
        return self.company.name+' - ' +self.name
    
class List(models.Model):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    
class Card(models.Model):
    name = models.CharField(max_length=255)
    lista = models.ForeignKey(List, on_delete=models.CASCADE)
