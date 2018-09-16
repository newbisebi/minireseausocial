from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Statut, Commentaire, Profil
from .forms import CommentForm, RegistrationForm
import datetime


# Create your views here.

class ListeUtilisateurs(ListView):
    model = Profil
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
        texte = form.cleaned_data['texte']
        visiteur = User.objects.get_or_create(username="visiteur·euse")[0]
        profil_visiteur = Profil.objects.get_or_create(user=visiteur, statut="Non cadre")[0]
        statut_id = form.cleaned_data['statut_id']
        statut = Statut.objects.get(id=statut_id)
        commentaire = Commentaire(texte=texte, auteur=profil_visiteur, statut=statut)
        commentaire.save()
        form = CommentForm()


    statuts = Statut.objects.filter(
            (Q(auteur_id = user_id) & Q(message__destinataire_id = None) ) #Statut posté par l'utilisateur sur son propre mur
            | Q(message__destinataire_id = user_id) #Statuts postés par d'autres utilisateurs son sur mur
        ).order_by('-date')
    username = Profil.objects.get(id=user_id).user.username
    avatar = Profil.objects.get(id=user_id).avatar
    return render(request, 'social/profile.html', locals())

def new_user(request):
    form = RegistrationForm(request.POST or None, request.FILES)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        new_user = User(username=username, password=password)
        avatar = form.cleaned_data["avatar"]
        print("AVATAR : ", avatar)
        statut = form.cleaned_data["statut"]
        new_user.save()
        new_profil = Profil(user=new_user, avatar=avatar, statut=statut)
        new_profil.save()


    return render(request, 'social/registration.html', locals())