# Generated by Django 4.0.4 on 2022-05-09 09:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('RealEstateApp', '0005_alter_address_city_alter_address_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
