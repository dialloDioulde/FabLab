# Generated by Django 2.2.6 on 2020-04-30 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('siteWeb', '0008_auto_20200430_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loaner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='siteWeb.Loaner'),
        ),
    ]
