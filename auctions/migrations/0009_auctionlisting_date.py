# Generated by Django 3.1.5 on 2021-01-15 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210115_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
