# Generated by Django 3.2 on 2021-05-25 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]
