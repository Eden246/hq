# Generated by Django 3.2 on 2021-06-04 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_alter_permission_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
