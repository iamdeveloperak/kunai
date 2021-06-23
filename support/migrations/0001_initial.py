# Generated by Django 3.2 on 2021-06-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=2000)),
            ],
            options={
                'db_table': 'support',
            },
        ),
    ]