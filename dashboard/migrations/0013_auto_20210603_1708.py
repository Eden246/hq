# Generated by Django 3.2 on 2021-06-03 08:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_remove_client_license'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0012_alter_permission_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='image',
            field=models.ManyToManyField(blank=True, to='home.Image'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
