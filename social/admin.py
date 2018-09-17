from django.contrib import admin

# Register your models here.
from .models import Statut, Commentaire, Message, Profil


admin.site.register(Statut)

admin.site.register(Commentaire)
admin.site.register(Message)
admin.site.register(Profil)