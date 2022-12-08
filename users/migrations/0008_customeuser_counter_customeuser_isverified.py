# Generated by Django 4.1.2 on 2022-12-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customeuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customeuser',
            name='isVerified',
            field=models.BooleanField(default=False),
        ),
    ]