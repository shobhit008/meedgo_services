# Generated by Django 4.1.2 on 2022-12-06 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customeuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeuser',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]