# Generated by Django 4.1.2 on 2022-12-12 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_rename_categoty_medicine_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prescription_image',
            field=models.FileField(blank=True, default='default.jpg', null=True, upload_to='prescription_pics'),
        ),
    ]
