# Generated by Django 3.1.5 on 2021-01-15 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210113_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='bid',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
