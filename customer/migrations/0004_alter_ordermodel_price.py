# Generated by Django 3.2 on 2021-05-12 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20210511_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
