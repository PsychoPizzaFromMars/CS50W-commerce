# Generated by Django 3.1.5 on 2021-02-02 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20210126_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlisting',
            old_name='active',
            new_name='is_active',
        ),
    ]
