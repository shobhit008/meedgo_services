# Generated by Django 4.1.2 on 2022-12-02 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customeuser_gender'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customeuser',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='customeuser',
            old_name='gender',
            new_name='user_type',
        ),
    ]
