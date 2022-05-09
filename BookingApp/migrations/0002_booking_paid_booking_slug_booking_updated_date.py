# Generated by Django 4.0.4 on 2022-05-09 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='slug',
            field=models.SlugField(default=3, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
