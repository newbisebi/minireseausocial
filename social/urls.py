from django.urls import path, re_path
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings

from . import views


#Le premier argument est l'url (chemin relatif) et le second est la vue renvoyée
urlpatterns = [
    re_path(r'^$', views.ListeUtilisateurs.as_view(), name = "social_utilisateurs"),
    # re_path(r'^utilisateur/(?P<pk>\d+)$', views.Profile.as_view(), name = "social_profile"),
    re_path(r'^utilisateur/(?P<profile_id>\d+)$', views.profile, name="social_profile"),
    re_path(r'^registration$', views.new_user, name = 'registration'),
    re_path(r'^connexion$', views.connexion, name='connexion'),
    re_path(r'^deconnexion$', views.deconnexion, name='deconnexion'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
