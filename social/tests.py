from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profil

# Create your tests here.
class UserTests(TestCase):

    @classmethod
    def setUpTestData(cls): #Appelé au début de la suite de tests
       user = User.objects.create_user('Paul', 'maxime@test.com', 'm0td€p@ss€sup€rf0rt')

    def setUp(self): #appelé avant chaque test
        pass

    def test_creation_profile_with_user(self):
        """Check if a profile is created when a new user is created"""
        user = User.objects.get(username='Paul', email='maxime@test.com')
        profile = Profil.objects.filter(user=user)
        self.assertTrue(profile.exists())