from django.urls import path, re_path
from django.contrib.auth.models import User

from . import views


#Le premier argument est l'url (chemin relatif) et le second est la vue renvoyée
urlpatterns = [
    re_path(r'^$', views.ListeUtilisateurs.as_view(), name = "social_utilisateurs"),
    # re_path(r'^utilisateur/(?P<pk>\d+)$', views.Profile.as_view(), name = "social_profile"),
    re_path(r'^utilisateur/(?P<user_id>\d+)$', views.profile, name="social_profile"),
]