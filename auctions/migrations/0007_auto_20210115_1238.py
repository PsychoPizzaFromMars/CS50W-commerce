# Generated by Django 3.1.5 on 2021-01-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210115_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='item_image',
            field=models.URLField(blank=True),
        ),
    ]
