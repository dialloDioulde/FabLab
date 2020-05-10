# Generated by Django 3.0.5 on 2020-05-10 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loaner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('establishment', models.CharField(max_length=250)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_type', models.CharField(choices=[('generic', 'generic'), ('unique', 'unique')], default='generic', max_length=250)),
                ('name_type', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('creation_date_type', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('one_click_purchasing', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('barcode', models.CharField(max_length=50)),
                ('creation_date_mat', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('material_picture', models.ImageField(blank=True, default='None/no-img.jpg', null=True, upload_to='media/')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteWeb.Type')),
            ],
        ),
        migrations.CreateModel(
            name='LoanMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('creation_date_loan_mat', models.DateTimeField(auto_now_add=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteWeb.Material')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('returned', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('creation_date_loan', models.DateTimeField(default=django.utils.timezone.now)),
                ('expected_return_date', models.DateField(blank=True, null=True)),
                ('return_date', models.DateField(null=True)),
                ('loaner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='siteWeb.Loaner')),
                ('materials', models.ManyToManyField(to='siteWeb.LoanMaterial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
