# Generated by Django 4.1.2 on 2022-12-14 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0007_pharmacistbiding_is_biding_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacistbiding',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
