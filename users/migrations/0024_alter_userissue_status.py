# Generated by Django 4.1.2 on 2022-12-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_userissue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userissue',
            name='status',
            field=models.CharField(choices=[('Initiated', 'Initiated'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Calceled', 'Calceled')], default='Initiated', max_length=30),
        ),
    ]