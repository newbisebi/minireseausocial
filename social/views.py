from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from .models import Statut, Commentaire, Profil, Message
from .forms import CommentForm, RegistrationForm, ConnexionForm, NewStatutForm
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

def profile(request, profile_id):

    if request.method == "POST" and "nouveau_commentaire" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            texte = comment_form.cleaned_data['texte']
            statut_id = comment_form.cleaned_data['statut_id']
            statut = Statut.objects.get(id=statut_id)

            try:
                auteur = Profil.objects.get(user=request.user)
            except(ObjectDoesNotExist, TypeError): #typeerror si anonymous user ==> voir meilleur moyen de le tester
                visiteur = User.objects.get_or_create(username="visiteur·euse")[0]
                auteur = Profil.objects.get_or_create(user=visiteur, statut="Non cadre")[0]

            commentaire = Commentaire(texte=texte, auteur=auteur, statut=statut)
            commentaire.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()


    if request.method == "POST" and "nouveau_statut" in request.POST:
        message_form = NewStatutForm(request.POST)
        if message_form.is_valid():
            texte = message_form.cleaned_data['texte']
            active_user = request.user
            auteur = Profil.objects.get(user=active_user)
            if auteur.id == int(profile_id): #on vérifie si il poste sur son propre mur ou celui d'un autre
                statut = Statut(texte=texte, auteur=auteur)
                statut.save()
            else:
                destinataire = Profil.objects.get(id=profile_id)
                message = Message(texte=texte, auteur=auteur, destinataire=destinataire)
                message.save()

            message_form = NewStatutForm()
    else:
        message_form = NewStatutForm()

    statuts = Statut.objects.filter(
            (Q(auteur_id = profile_id) & Q(message__destinataire_id = None) ) #Statut posté par l'utilisateur sur son propre mur
            | Q(message__destinataire_id = profile_id) #Statuts postés par d'autres utilisateurs son sur mur
        ).order_by('-date')
    username = Profil.objects.get(id=profile_id).user.username
    avatar = Profil.objects.get(id=profile_id).avatar
    return render(request, 'social/profile.html', locals())

def new_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user = User(username=username)
            new_user.set_password(password)
            avatar = form.cleaned_data["avatar"]
            statut = form.cleaned_data["statut"]
            new_user.save()
            # Profil automatiquement créé par un signal
            new_profil = Profil.objects.get(user=new_user)
            new_profil.avatar = avatar
            new_profil.statut = statut
            new_profil.save()
            form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(request, 'social/registration.html', locals())


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'social/connexion.html', locals())


def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))