# Generated by Django 2.0.5 on 2018-09-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='statut',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
