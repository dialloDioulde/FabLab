# Generated by Django 2.2.6 on 2020-04-29 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('siteWeb', '0002_auto_20200410_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='loan',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='loaner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='siteWeb.Loaner'),
        ),
    ]
