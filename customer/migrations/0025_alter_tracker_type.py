# Generated by Django 3.2 on 2021-06-07 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_tracker_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='type',
            field=models.CharField(default='在庫追加', max_length=100),
        ),
    ]
