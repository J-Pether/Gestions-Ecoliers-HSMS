from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    adresse = models.TextField()

    photo = models.ImageField(upload_to="etudiants/", blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Cours(models.Model):
    code = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField()
    
    def __str__(self):
        return f"{self.code} - {self.nom}"

class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['etudiant', 'cours']
    
    def __str__(self):
        return f"{self.etudiant} - {self.cours}"

class Note(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=4, decimal_places=2)
    date_evaluation = models.DateField()
    
    def __str__(self):
        return f"{self.inscription} - {self.note}"