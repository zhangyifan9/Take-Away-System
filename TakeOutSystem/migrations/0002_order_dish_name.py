# Generated by Django 3.2 on 2021-11-22 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TakeOutSystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='dish_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
