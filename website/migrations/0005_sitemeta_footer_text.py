# Generated by Django 3.2 on 2021-05-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_infocard_pagesection'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemeta',
            name='footer_text',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
