from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import Signal
from django.dispatch import receiver

# Create your models here.

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    statut = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Statut(models.Model):
    texte = models.TextField()
    date = models.DateTimeField(verbose_name="Date de parution",
                                auto_now_add=True, auto_now=False)
    auteur = models.ForeignKey(Profil,
        on_delete=models.CASCADE,
        related_name = "auteur")

    def __str__(self):
        return f"Message posté par {self.auteur.user.username} - {self.texte}"

class Message(Statut):
    destinataire = models.ForeignKey(Profil,
        on_delete=models.CASCADE,
        related_name = "destinataire")

class Commentaire(models.Model):
    texte = models.TextField()
    date = models.DateTimeField(verbose_name="Date de parution",
                                auto_now_add=True, auto_now=False)
    auteur = models.ForeignKey(Profil,
        on_delete=models.CASCADE,
        related_name = "commentateur")
    statut = models.ForeignKey('Statut', on_delete=models.CASCADE, related_name = "commentaire")




#SIGNAUX
@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, **kwargs):
    new_profile = Profil(user=instance)
    new_profile.save()