# Generated by Django 3.2 on 2021-11-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TakeOutSystem', '0003_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='special_offer',
            field=models.IntegerField(default=0),
        ),
    ]
