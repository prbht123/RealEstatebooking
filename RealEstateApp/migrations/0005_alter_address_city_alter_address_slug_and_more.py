# Generated by Django 4.0.4 on 2022-05-09 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RealEstateApp', '0004_rename_landmark_address_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='slug',
            field=models.SlugField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
