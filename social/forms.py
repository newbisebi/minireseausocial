from django import forms
from .models import Commentaire, Profil, User

class CommentForm(forms.Form):
    texte = forms.CharField(
        label='',
        max_length=1000,
        widget=forms.Textarea(attrs={'min-width':"100%", 'rows': "1", 'placeholder':'Ajouter un commentaire'}))

    statut_id = forms.CharField(widget=forms.HiddenInput())

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(max_length=100, label="Mot de Passe", widget=forms.PasswordInput)
    confirm_pw = forms.CharField(max_length=100, label="Confirmez le mot de Passe", widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
    statut = forms.ChoiceField(choices=(('',''),('Non cadre','Non cadre'),('Cadre','Cadre')), initial='')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        confirm_pw = cleaned_data.get('confirm_pw')
        avatar = cleaned_data.get('avatar')
        statut = cleaned_data.get('statut')

        if password and password != confirm_pw:
            raise forms.ValidationError('Attention, les mots de passes ne coïncident pas')

        username_exists = User.objects.filter(username=username).all()
        if username_exists:
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris")

        return cleaned_data

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class NewStatutForm(forms.Form):
    texte = forms.CharField(
        label='',
        max_length=1000,
        widget=forms.Textarea(attrs={'min-width':"100%", 'rows': "1", 'placeholder':'Des choses intéressantes à dire ? '}))

