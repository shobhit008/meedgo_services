# Generated by Django 4.1.2 on 2022-12-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_order_phamacist_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='addressbook',
            name='long',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
    ]
