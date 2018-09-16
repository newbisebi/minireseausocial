from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Statut(models.Model):
    texte = models.TextField()
    date = models.DateTimeField(verbose_name="Date de parution",
                                auto_now_add=True, auto_now=False)
    auteur = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name = "auteur")

class Message(Statut):
    destinataire = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name = "destinataire")

class Commentaire(models.Model):
    texte = models.TextField()
    date = models.DateTimeField(verbose_name="Date de parution",
                                auto_now_add=True, auto_now=False)
    auteur = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name = "commentateur")
    statut = models.ForeignKey('Statut', on_delete=models.CASCADE, related_name = "commentaire")
