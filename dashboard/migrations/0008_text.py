# Generated by Django 3.2 on 2021-06-01 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_permission_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=100)),
                ('second', models.CharField(max_length=100)),
                ('third', models.CharField(max_length=100)),
            ],
        ),
    ]
