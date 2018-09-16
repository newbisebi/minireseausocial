from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Statut, Commentaire
from .forms import CommentForm
import datetime


# Create your views here.

class ListeUtilisateurs(ListView):
    model = User
    context_object_name = "utilisateurs"
    template_name = "social/utilisateurs.html"
    paginate_by = 5


# class Profile(DetailView):
#     context_object_name = "profile"
#     model = User
#     template_name = "social/profile.html"
#     queryset = Statut.objects.filter(
#             Q(auteur.id = pk) | Q(destinataire.id = pk)
#         )

def profile(request, user_id):
    form = CommentForm(request.POST or None)

    if form.is_valid():
        print("FORM >>>>>>>>>>>>>>>", form.cleaned_data)
        texte = form.cleaned_data['texte']
        auteur = User.objects.get_or_create(username="visiteur·euse")[0]
        statut_id = form.cleaned_data['statut_id']
        statut = Statut.objects.get(id=statut_id)
        commentaire = Commentaire(texte=texte, auteur=auteur, statut=statut)
        commentaire.save()
        form = CommentForm()


    statuts = Statut.objects.filter(
            (Q(auteur_id = user_id) & Q(message__destinataire_id = None) ) #Statut posté par l'utilisateur sur son propre mur
            | Q(message__destinataire_id = user_id) #Statuts postés par d'autres utilisateurs son sur mur
        ).order_by('-date')
    username = User.objects.get(id=user_id).username
    return render(request, 'social/profile.html', locals())