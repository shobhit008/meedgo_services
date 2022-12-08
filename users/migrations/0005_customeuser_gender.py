# Generated by Django 4.1.2 on 2022-12-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customeuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], default='M', max_length=10),
        ),
    ]
