# Generated by Django 4.1.2 on 2022-12-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacist', '0009_winbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacistbiding',
            name='is_biding_win',
            field=models.CharField(choices=[('win', 'Win'), ('in transition', 'In transition'), ('loose', 'Loose')], default='in transition', max_length=20),
        ),
    ]