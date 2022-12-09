# Generated by Django 4.1.2 on 2022-12-09 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeuser',
            name='user_type',
            field=models.CharField(choices=[('Customer', 'customer'), ('Pharmacists', 'pharmacists'), ('Doctor', 'doctor'), ('Hospitals', 'hospitals')], default='Customer', max_length=15),
        ),
    ]
