# Generated by Django 3.0.5 on 2020-05-10 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteWeb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='unavailable',
            field=models.BooleanField(default=False),
        ),
    ]