# Generated by Django 3.2 on 2021-05-28 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_menuitem_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='video_url',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
