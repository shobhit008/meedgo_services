# Generated by Django 4.1.2 on 2022-12-19 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacist', '0008_pharmacistbiding_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('phamacist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner_pharmacist', to=settings.AUTH_USER_MODEL)),
                ('winBid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winBid', to='pharmacist.pharmacistbiding')),
            ],
        ),
    ]
