from django import forms
from .models import Commentaire

class CommentForm(forms.Form):
    texte = forms.CharField(
        label='',
        max_length=1000,
        widget=forms.Textarea(attrs={'min-width':"100%", 'rows': "1", 'placeholder':'Ajouter un commentaire'}))

    statut_id = forms.CharField(widget=forms.HiddenInput())