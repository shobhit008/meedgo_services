# Generated by Django 4.1.2 on 2022-12-19 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_userissue_pharmacist'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phamacist_data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='phamacist_data', to=settings.AUTH_USER_MODEL),
        ),
    ]