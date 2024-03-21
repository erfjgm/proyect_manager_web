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
    creat_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_lists')
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='deleted_lists')
    deletion_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ['name', 'board']
    def __str__(self):
        return self.board.name+' - ' +self.name
    
class Card(models.Model):
    name = models.CharField(max_length=255)
    lista = models.ForeignKey(List, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateField(auto_now_add=True,blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    assigned_users = models.ManyToManyField(UserProfile, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    deletion_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ['name', 'lista']
    def __str__(self):
        return self.lista.board.name+' - '+ self.lista.name+' - '+self.name+' - '+str(self.delivery_date)
