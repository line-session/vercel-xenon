from django.db import models

# Create your models here.
class pharmacien(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50)
    nom = models.CharField(max_length=10)
    prenom = models.CharField(max_length=30)
    password = models.CharField(max_length=70)
    class Meta:
        app_label='main'

class medicament(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=20)
    code = models.CharField(max_length=10)    
    prix = models.IntegerField()
    description = models.CharField(max_length=255)
    dateExpiration = models.DateField()
    stockDisponible = models.IntegerField()
    class meta:
        app_label='main'
